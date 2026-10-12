"""Custom exceptions for the dva-lab package."""


class DVALabError(Exception):
    """Base exception for all DVA Lab errors."""
    pass


class ExperimentNotFoundError(ValueError, DVALabError):
    """Raised when an experiment ID cannot be found locally or remotely."""

    def __init__(self, exp_id):
        self.exp_id = exp_id
        super().__init__(
            f"Experiment '{exp_id}' not found. "
            f"Available experiments are integers from 1 to 12. "
            f"Call list_experiments() to see the full catalog."
        )


class RepositoryNotFoundError(DVALabError):
    """Raised when the remote GitHub repository is not found (HTTP 404)."""

    def __init__(self, username: str, repository: str, branch: str = "main"):
        self.username = username
        self.repository = repository
        self.branch = branch
        super().__init__(
            f"Remote repository not found: https://github.com/{username}/{repository} "
            f"(branch: '{branch}'). Please verify your username and repository configuration "
            f"using dva_lab.configure(username='...', repository='...')."
        )


class RemoteFetchError(DVALabError):
    """Raised when fetching code or metadata from GitHub over HTTPS fails."""

    def __init__(self, url: str, reason: str):
        self.url = url
        self.reason = reason
        super().__init__(
            f"Failed to fetch remote asset from GitHub over HTTPS: {url}. Reason: {reason}"
        )


class ConfigurationError(DVALabError):
    """Raised when the DVA Lab client configuration is invalid."""
    pass


class ExecutionEnvironmentError(DVALabError):
    """Raised when an experiment cannot be executed in the current environment."""
    pass
