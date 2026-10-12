"""Tests for configuration, GitHub client, and remote retrieval functionality."""

import os
import pytest
from unittest.mock import patch, MagicMock

import dva_lab
from dva_lab.config import Config, configure, get_config, reset_config, DEFAULT_USERNAME, DEFAULT_REPOSITORY
from dva_lab.client import GitHubClient, get_client
from dva_lab.exceptions import (
    ExperimentNotFoundError,
    RepositoryNotFoundError,
    RemoteFetchError,
)


@pytest.fixture(autouse=True)
def clean_config():
    """Ensure clean configuration state for each test."""
    reset_config()
    yield
    reset_config()


def test_default_config():
    """Verify default repository configuration values."""
    cfg = get_config()
    assert cfg.username == DEFAULT_USERNAME
    assert cfg.repository == DEFAULT_REPOSITORY
    assert cfg.branch == "main"
    assert cfg.offline_fallback is True


def test_configure_updates_state():
    """Verify configure() updates the singleton config instance."""
    configure(username="TestUser", repository="custom-repo", branch="dev", timeout=5.0)
    cfg = get_config()
    assert cfg.username == "TestUser"
    assert cfg.repository == "custom-repo"
    assert cfg.branch == "dev"
    assert cfg.timeout == 5.0

    reset_config()
    cfg_reset = get_config()
    assert cfg_reset.username == DEFAULT_USERNAME


def test_config_env_vars():
    """Verify environment variables override defaults."""
    with patch.dict(os.environ, {"DVA_GITHUB_USER": "EnvUser", "DVA_GITHUB_REPO": "env-repo"}):
        cfg = Config()
        assert cfg.username == "EnvUser"
        assert cfg.repository == "env-repo"


def test_get_raw_url():
    """Verify raw GitHub URL generation."""
    cfg = get_config()
    url = cfg.get_raw_url("codes/01_olap.sql")
    assert url == f"https://raw.githubusercontent.com/{DEFAULT_USERNAME}/{DEFAULT_REPOSITORY}/main/codes/01_olap.sql"


def test_resolve_experiment_variations():
    """Verify resolve_experiment handles integers, strings, and zero-padded strings."""
    client = get_client()
    key, entry = client.resolve_experiment(1)
    assert int(key) == 1
    assert "OLAP" in entry["title"]

    key_str, entry_str = client.resolve_experiment("1")
    assert int(key_str) == 1

    key_pad, entry_pad = client.resolve_experiment("01")
    assert int(key_pad) == 1

    with pytest.raises(ExperimentNotFoundError):
        client.resolve_experiment(99)


def test_get_code_remote_fallback():
    """Verify get_code seamlessly falls back to bundled code if remote fails."""
    # Point to nonexistent repo
    configure(username="nonexistent-user-99999", repository="nonexistent-repo-99999")
    # By default offline_fallback is True, so get_code(1) should return bundled code
    code = dva_lab.get_code(1)
    assert "sales_cube" in code

    # When offline_fallback is False, should raise error
    configure(offline_fallback=False)
    with pytest.raises(Exception):
        dva_lab.get_code(1, refresh=True)


def test_search_experiments():
    """Verify search returns matching experiments."""
    bar_results = dva_lab.search("bar")
    assert len(bar_results) >= 2  # Exp 3 & Exp 4

    sql_results = dva_lab.search("olap")
    assert len(sql_results) >= 2  # Exp 1 & Exp 2

    dax_results = dva_lab.search("dax")
    assert len(dax_results) >= 2  # Exp 11 & Exp 12


def test_get_info():
    """Verify get_info retrieves experiment metadata."""
    info = dva_lab.get_info(3)
    assert info["id"] == 3
    assert "Bar" in info["title"]
    assert "matplotlib" in str(info.get("tags") or info.get("dependencies"))
