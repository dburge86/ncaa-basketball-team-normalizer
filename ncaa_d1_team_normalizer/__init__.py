"""NCAA D1 Men's Basketball Team Name Normalization Module."""

from .team_matcher import TeamNormalizer
from .exceptions import (
    TeamNormalizerError,
    UnknownTeamError,
    DataLoadError,
    InvalidInputError,
)

__version__ = "0.1.0"

__all__ = [
    "TeamNormalizer",
    "TeamNormalizerError",
    "UnknownTeamError",
    "DataLoadError",
    "InvalidInputError",
    "normalize_team",
]


def normalize_team(team_name: str, fuzzy_threshold: int = 85, raise_on_no_match: bool = False):
    """
    Convenience function for quick one-off team normalization.

    Args:
        team_name: Team name to normalize
        fuzzy_threshold: Minimum fuzzy match score (0-100)
        raise_on_no_match: If True, raise UnknownTeamError when no match found

    Returns:
        Dictionary with canonical team info, or None if no match found

    Raises:
        UnknownTeamError: If raise_on_no_match=True and no match found
        InvalidInputError: If input validation fails
    """
    normalizer = TeamNormalizer(fuzzy_threshold=fuzzy_threshold, raise_on_no_match=raise_on_no_match)
    return normalizer.normalize(team_name)
