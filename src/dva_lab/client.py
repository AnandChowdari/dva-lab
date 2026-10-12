"""HTTP client and caching layer for fetching experiments from GitHub over HTTPS."""

import hashlib
import json
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, Union

from .config import Config, get_config
from .exceptions import (
    RepositoryNotFoundError,
    RemoteFetchError,
    ExperimentNotFoundError,
)

USER_AGENT = "dva-lab-Python-Client/0.2.0"
INDEX_CACHE_TTL = 300.0  # 5 minutes in-memory cache TTL


class GitHubClient:
    """Handles communication with GitHub raw content and manages intelligent caching."""

    def __init__(self, config: Optional[Config] = None):
        self._config = config
        self._index_cache: Optional[Dict[str, Any]] = None
        self._index_fetched_at: float = 0.0

    @property
    def config(self) -> Config:
        return self._config or get_config()

    def fetch_url(self, url: str) -> str:
        """Fetch raw text content from a given URL with timeout and custom headers."""
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "text/plain, application/json, */*",
        }
        req = urllib.request.Request(url, headers=headers)
        timeout = self.config.get_timeout()

        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                content_bytes = response.read()
                return content_bytes.decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise RepositoryNotFoundError(
                    username=self.config.username,
                    repository=self.config.repository,
                    branch=self.config.branch,
                ) from e
            raise RemoteFetchError(url, f"HTTP Error {e.code}: {e.reason}") from e
        except urllib.error.URLError as e:
            raise RemoteFetchError(url, f"Network connection failed: {e.reason}") from e
        except Exception as e:
            raise RemoteFetchError(url, f"Unexpected error: {str(e)}") from e

    def _get_bundled_index(self) -> Dict[str, Any]:
        """Load bundled fallback index.json from package installation directory."""
        pkg_dir = Path(__file__).resolve().parent
        bundled_path = pkg_dir / "index.json"
        if bundled_path.exists():
            try:
                with open(bundled_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

        # Try root repo index.json if running in dev/repo mode
        root_path = pkg_dir.parent.parent / "index.json"
        if root_path.exists():
            try:
                with open(root_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

        return {}

    def fetch_index(self, refresh: bool = False) -> Dict[str, Any]:
        """Fetch catalog index.json from GitHub over HTTPS, with caching and offline fallback."""
        now = time.time()
        if (
            not refresh
            and self._index_cache is not None
            and (now - self._index_fetched_at) < INDEX_CACHE_TTL
        ):
            return self._index_cache

        # Check local disk cache
        cache_file = self.config.cache_dir / f"index_{self.config.username}_{self.config.repository}.json"
        if not refresh and cache_file.exists():
            try:
                mtime = cache_file.stat().st_mtime
                if (now - mtime) < INDEX_CACHE_TTL:
                    with open(cache_file, "r", encoding="utf-8") as f:
                        self._index_cache = json.load(f)
                        self._index_fetched_at = now
                        return self._index_cache
            except Exception:
                pass

        url = self.config.get_raw_url("index.json")
        try:
            raw_text = self.fetch_url(url)
            data = json.loads(raw_text)
            self._index_cache = data
            self._index_fetched_at = now

            # Save to disk cache
            try:
                self.config.cache_dir.mkdir(parents=True, exist_ok=True)
                with open(cache_file, "w", encoding="utf-8") as f:
                    f.write(raw_text)
            except Exception:
                pass

            return data
        except Exception as exc:
            # If offline fallback is enabled, load bundled index
            if self.config.offline_fallback:
                bundled = self._get_bundled_index()
                if bundled:
                    self._index_cache = bundled
                    self._index_fetched_at = now
                    return bundled
            raise exc

    def _cache_path_for(self, file_path: str) -> Path:
        """Compute disk cache path for a given remote file."""
        user = self.config.username
        repo = self.config.repository
        branch = self.config.branch
        key = f"{user}/{repo}/{branch}/{file_path}"
        digest = hashlib.md5(key.encode("utf-8")).hexdigest()
        ext = Path(file_path).suffix or ".txt"
        return self.config.cache_dir / f"{digest}{ext}"

    def fetch_code(self, file_path: str, refresh: bool = False, cache: bool = True) -> str:
        """Fetch code file from GitHub over HTTPS."""
        cache_path = self._cache_path_for(file_path)

        if cache and not refresh and cache_path.exists():
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                pass

        url = self.config.get_raw_url(file_path)
        content = self.fetch_url(url)

        if cache:
            try:
                self.config.cache_dir.mkdir(parents=True, exist_ok=True)
                with open(cache_path, "w", encoding="utf-8") as f:
                    f.write(content)
            except Exception:
                pass

        return content

    def resolve_experiment(
        self,
        exp_id: Union[int, str],
        refresh: bool = False,
    ) -> Tuple[str, Dict[str, Any]]:
        """Resolve experiment entry from index by ID (e.g. 1, '1', '01').

        Returns:
            Tuple of (matched_key, metadata_dict).
        """
        index = self.fetch_index(refresh=refresh)
        str_id = str(exp_id).strip()

        # 1. Exact match
        if str_id in index:
            return str_id, index[str_id]

        # 2. Integer equivalence match
        try:
            int_id = int(str_id)
            padded2 = f"{int_id:02d}"
            if padded2 in index:
                return padded2, index[padded2]

            padded3 = f"{int_id:03d}"
            if padded3 in index:
                return padded3, index[padded3]

            for k, entry in index.items():
                try:
                    if int(k) == int_id:
                        return k, entry
                except (ValueError, TypeError):
                    continue
        except ValueError:
            pass

        raise ExperimentNotFoundError(exp_id)


# Global client singleton
_GLOBAL_CLIENT = GitHubClient()


def get_client() -> GitHubClient:
    """Return the active global GitHub client."""
    return _GLOBAL_CLIENT
