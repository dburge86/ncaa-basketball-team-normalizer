"""Core team name matching logic."""

from typing import Dict, List, Optional

from rapidfuzz import process, fuzz

from .data_loader import ESPNDataLoader
from .text_cleaner import TextCleaner
from .aliases import TEAM_ALIASES
from .exceptions import UnknownTeamError, InvalidInputError


class TeamNormalizer:
    """
    Main class for normalizing team names to ESPN canonical format.

    Implements multi-step matching pipeline:
    1. Input validation
    2. Text cleaning
    3. Exact match
    4. Alias lookup
    5. Fuzzy match
    """

    def __init__(self, fuzzy_threshold: int = 85, raise_on_no_match: bool = False):
        """
        Initialize the normalizer.

        Args:
            fuzzy_threshold: Minimum fuzzy match score (0-100)
            raise_on_no_match: If True, raise UnknownTeamError when no match found
        """
        self.fuzzy_threshold = fuzzy_threshold
        self.raise_on_no_match = raise_on_no_match

        # Load ESPN data (lazy loaded by data loader)
        self._data_loader = ESPNDataLoader()
        self._team_data = None

    def _ensure_data_loaded(self):
        """Ensure team data is loaded."""
        if self._team_data is None:
            self._team_data = self._data_loader.get_team_lookup_dict()

    def normalize(self, team_name: str) -> Optional[Dict]:
        """
        Normalize a team name to ESPN canonical format.

        Args:
            team_name: Team name to normalize

        Returns:
            Dictionary with canonical team info and match metadata, or None

        Raises:
            InvalidInputError: If input validation fails
            UnknownTeamError: If raise_on_no_match=True and no match found
        """
        # Step 1: Validate input
        if team_name is None:
            raise InvalidInputError("Team name cannot be None")
        if not isinstance(team_name, str):
            raise InvalidInputError(f"Team name must be a string, got {type(team_name).__name__}")
        if not team_name.strip():
            raise InvalidInputError("Team name cannot be empty")

        # Ensure data is loaded
        self._ensure_data_loaded()

        # Step 2: Clean input
        try:
            cleaned_name = TextCleaner.clean(team_name)
        except InvalidInputError:
            raise  # Re-raise validation errors

        # Step 3: Try exact match
        result = self._exact_match(cleaned_name)
        if result:
            return result

        # Step 4: Try alias lookup
        result = self._alias_match(cleaned_name)
        if result:
            return result

        # Step 5: Try fuzzy match
        result = self._fuzzy_match(cleaned_name)
        if result:
            return result

        # Step 6: No match found
        if self.raise_on_no_match:
            raise UnknownTeamError(team_name)
        return None

    def _exact_match(self, cleaned_name: str) -> Optional[Dict]:
        """
        Try exact match against canonical names.

        Args:
            cleaned_name: Cleaned team name

        Returns:
            Match result or None
        """
        by_name = self._team_data['by_name']

        if cleaned_name in by_name:
            team_info = by_name[cleaned_name]
            return {
                'canonical_name': team_info['display_name'],
                'espn_id': team_info['team_id'],
                'abbreviation': team_info['abbreviation'],
                'confidence': 100.0,
                'match_method': 'exact',
            }

        return None

    def _alias_match(self, cleaned_name: str) -> Optional[Dict]:
        """
        Try alias dictionary lookup.

        Args:
            cleaned_name: Cleaned team name

        Returns:
            Match result or None
        """
        if cleaned_name in TEAM_ALIASES:
            canonical_name = TEAM_ALIASES[cleaned_name]

            # Look up the canonical name in our data
            by_name = self._team_data['by_name']

            # Clean the canonical name for lookup
            try:
                cleaned_canonical = TextCleaner.clean(canonical_name)
            except InvalidInputError:
                return None

            if cleaned_canonical in by_name:
                team_info = by_name[cleaned_canonical]
                return {
                    'canonical_name': team_info['display_name'],
                    'espn_id': team_info['team_id'],
                    'abbreviation': team_info['abbreviation'],
                    'confidence': 100.0,
                    'match_method': 'alias',
                }

        return None

    def _fuzzy_match(self, cleaned_name: str) -> Optional[Dict]:
        """
        Try fuzzy matching with rapidfuzz.

        Args:
            cleaned_name: Cleaned team name

        Returns:
            Match result or None
        """
        all_names = self._team_data['all_names']
        by_name = self._team_data['by_name']

        # Use rapidfuzz to find best match
        result = process.extractOne(
            cleaned_name,
            all_names,
            scorer=fuzz.ratio,
            score_cutoff=self.fuzzy_threshold
        )

        if result:
            matched_name, score, _ = result
            team_info = by_name[matched_name]

            return {
                'canonical_name': team_info['display_name'],
                'espn_id': team_info['team_id'],
                'abbreviation': team_info['abbreviation'],
                'confidence': float(score),
                'match_method': 'fuzzy',
            }

        return None

    def normalize_batch(self, team_names: List[str]) -> List[Optional[Dict]]:
        """
        Normalize multiple team names efficiently.

        Args:
            team_names: List of team names to normalize

        Returns:
            List of match results (same order as input)
        """
        return [self.normalize(name) for name in team_names]

    def get_all_teams(self) -> List[Dict]:
        """
        Get list of all available teams.

        Returns:
            List of all team info dictionaries
        """
        self._ensure_data_loaded()
        by_name = self._team_data['by_name']

        teams = []
        for team_info in by_name.values():
            teams.append({
                'canonical_name': team_info['display_name'],
                'espn_id': team_info['team_id'],
                'abbreviation': team_info['abbreviation'],
            })

        return teams
