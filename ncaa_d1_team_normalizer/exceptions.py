"""Custom exceptions for NCAA D1 Team Normalizer."""


class TeamNormalizerError(Exception):
    """Base exception for all team normalizer errors."""
    pass


class UnknownTeamError(TeamNormalizerError):
    """Raised when no match is found for a team name."""

    def __init__(self, team_name: str):
        self.team_name = team_name
        super().__init__(f"No match found for team: {team_name}")


class DataLoadError(TeamNormalizerError):
    """Raised when ESPN data cannot be loaded."""
    pass


class InvalidInputError(TeamNormalizerError):
    """Raised when input validation fails."""

    def __init__(self, message: str):
        super().__init__(f"Invalid input: {message}")
