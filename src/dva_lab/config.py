"""Configuration management for the DVA Lab client and remote repository access."""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

from .exceptions import ConfigurationError

CONFIG_DIR = Path.home() / ".dva_lab"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_USERNAME = "AnandChowdari"
DEFAULT_REPOSITORY = "dva-lab"
DEFAULT_BRANCH = "main"
DEFAULT_TIMEOUT = 10.0


class Config:
    """Holds configuration state for DVA Lab remote GitHub synchronization."""

    def __init__(
        self,
        username: Optional[str] = None,
        repository: Optional[str] = None,
        branch: Optional[str] = None,
        cache_dir: Optional[Path] = None,
        timeout: float = DEFAULT_TIMEOUT,
        offline_fallback: bool = True,
    ):
        self._username = username
        self._repository = repository
        self._branch = branch
        self.cache_dir = cache_dir or (CONFIG_DIR / "cache")
        self.timeout = timeout
        self.offline_fallback = offline_fallback

    @property
    def username(self) -> str:
        """Get the configured GitHub username."""
        # 1. In-memory setting
        if self._username:
            return self._username

        # 2. Environment variable
        env_user = os.environ.get("DVA_GITHUB_USER")
        if env_user:
            return env_user

        # 3. Persistent config file
        file_config = self._load_file_config()
        if "username" in file_config and file_config["username"]:
            return file_config["username"]

        return DEFAULT_USERNAME

    @username.setter
    def username(self, val: Optional[str]) -> None:
        self._username = val

    @property
    def repository(self) -> str:
        """Get the configured GitHub repository name."""
        return self.get_repository()

    @repository.setter
    def repository(self, val: Optional[str]) -> None:
        self._repository = val

    @property
    def branch(self) -> str:
        """Get the configured Git branch name."""
        return self.get_branch()

    @branch.setter
    def branch(self, val: Optional[str]) -> None:
        self._branch = val

    def get_repository(self) -> str:
        """Get configured repository name with environment/file fallbacks."""
        if self._repository:
            return self._repository
        env_repo = os.environ.get("DVA_GITHUB_REPO")
        if env_repo:
            return env_repo
        file_config = self._load_file_config()
        return file_config.get("repository", DEFAULT_REPOSITORY)

    def get_branch(self) -> str:
        """Get configured branch name with environment/file fallbacks."""
        if self._branch:
            return self._branch
        env_branch = os.environ.get("DVA_GITHUB_BRANCH")
        if env_branch:
            return env_branch
        file_config = self._load_file_config()
        return file_config.get("branch", DEFAULT_BRANCH)

    def get_timeout(self) -> float:
        """Get network timeout in seconds."""
        env_timeout = os.environ.get("DVA_TIMEOUT")
        if env_timeout:
            try:
                return float(env_timeout)
            except ValueError:
                pass
        return self.timeout

    def get_raw_url(self, path: str) -> str:
        """Construct raw GitHub URL (via raw.githubusercontent.com) for a relative path."""
        user = self.username
        repo = self.get_repository()
        branch = self.get_branch()
        clean_path = path.lstrip("/")
        return f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{clean_path}"

    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as a dictionary."""
        return {
            "username": self.username,
            "repository": self.get_repository(),
            "branch": self.get_branch(),
            "timeout": self.get_timeout(),
            "cache_dir": str(self.cache_dir),
            "offline_fallback": self.offline_fallback,
        }

    def _load_file_config(self) -> Dict[str, Any]:
        """Load stored configuration from disk if available."""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_to_file(self) -> None:
        """Save active configuration to ~/.dva_lab/config.json."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        data = {
            "username": self.username,
            "repository": self.repository,
            "branch": self.branch,
            "timeout": self.timeout,
            "offline_fallback": self.offline_fallback,
        }
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


# Global singleton instance
_GLOBAL_CONFIG = Config()


def get_config() -> Config:
    """Return the active global configuration."""
    return _GLOBAL_CONFIG


def configure(
    username: Optional[str] = None,
    repository: Optional[str] = None,
    branch: Optional[str] = None,
    timeout: Optional[float] = None,
    offline_fallback: Optional[bool] = None,
    persist: bool = False,
) -> Config:
    """Configure the DVA Lab client for GitHub code retrieval.

    Args:
        username: GitHub username/organization owning the repository (e.g. 'AnandChowdari').
        repository: Name of the repository (e.g. 'dva-lab').
        branch: Git branch name (defaults to 'main').
        timeout: Network timeout in seconds (defaults to 10.0).
        offline_fallback: If True, falls back to bundled local code if offline or error.
        persist: If True, writes settings to ~/.dva_lab/config.json.

    Returns:
        The updated Config instance.
    """
    if username is not None:
        _GLOBAL_CONFIG.username = username
    if repository is not None:
        _GLOBAL_CONFIG.repository = repository
    if branch is not None:
        _GLOBAL_CONFIG.branch = branch
    if timeout is not None:
        _GLOBAL_CONFIG.timeout = timeout
    if offline_fallback is not None:
        _GLOBAL_CONFIG.offline_fallback = offline_fallback

    if persist:
        _GLOBAL_CONFIG.save_to_file()

    return _GLOBAL_CONFIG


def reset_config() -> None:
    """Reset configuration to defaults (primarily useful for testing)."""
    global _GLOBAL_CONFIG
    _GLOBAL_CONFIG = Config()
