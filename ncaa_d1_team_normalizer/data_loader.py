"""ESPN data loading and caching."""

import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from .exceptions import DataLoadError
from .text_cleaner import TextCleaner


class ESPNDataLoader:
    """
    Singleton class for loading and caching ESPN team data.

    Implements lazy loading with 24-hour TTL cache.
    """

    _instance: Optional['ESPNDataLoader'] = None
    _teams_data: Optional[Dict] = None
    _last_load_time: Optional[datetime] = None
    _cache_ttl_hours: int = 24

    def __new__(cls):
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize loader (only runs once due to singleton)."""
        pass

    def _is_cache_valid(self) -> bool:
        """Check if cached data is still valid."""
        if self._last_load_time is None or self._teams_data is None:
            return False

        cache_age = datetime.now() - self._last_load_time
        return cache_age < timedelta(hours=self._cache_ttl_hours)

    def load_teams(self, force_refresh: bool = False, max_retries: int = 3) -> None:
        """
        Load team data from ESPN via sportsdataverse.

        Args:
            force_refresh: If True, bypass cache and reload data
            max_retries: Number of retry attempts on failure

        Raises:
            DataLoadError: If data cannot be loaded after retries
        """
        # Return early if cache is valid and not forcing refresh
        if not force_refresh and self._is_cache_valid():
            return

        # Try loading with retries
        last_error = None
        for attempt in range(max_retries):
            try:
                # Import here to avoid loading on module import
                from sportsdataverse.mbb import espn_mbb_teams

                # Load Division I teams (groups=50 is D1)
                teams_df = espn_mbb_teams(groups=50)

                if teams_df is None or teams_df.empty:
                    raise DataLoadError("ESPN returned empty team data")

                # Store raw data and timestamp
                self._raw_data = teams_df
                self._last_load_time = datetime.now()

                # Build optimized lookup structure
                self._teams_data = self._build_lookup_dict(teams_df)

                return  # Success!

            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    # Wait before retry (exponential backoff)
                    time.sleep(2 ** attempt)
                    continue
                else:
                    # Final attempt failed
                    raise DataLoadError(f"Failed to load ESPN data after {max_retries} attempts: {str(e)}")

    def _build_lookup_dict(self, teams_df) -> Dict:
        """
        Build optimized lookup structure from raw ESPN data.

        Returns:
            {
                'by_name': {cleaned_name: team_info},
                'by_abbrev': {abbreviation: team_info},
                'by_id': {espn_id: team_info},
                'all_names': [list of cleaned names for fuzzy matching]
            }
        """
        by_name = {}
        by_abbrev = {}
        by_id = {}
        all_names = []

        for _, row in teams_df.iterrows():
            # Extract team info
            display_name = row.get('display_name', row.get('name', ''))
            team_id = row.get('id', row.get('team_id', ''))
            abbreviation = row.get('abbreviation', '')

            if not display_name:
                continue  # Skip teams without names

            team_info = {
                'display_name': display_name,
                'team_id': str(team_id),
                'abbreviation': abbreviation,
                'location': row.get('location', ''),
                'nickname': row.get('nickname', ''),
                'full_name': row.get('name', display_name),
            }

            # Clean the display name for matching
            try:
                cleaned_name = TextCleaner.clean(display_name)

                # Add to lookups
                by_name[cleaned_name] = team_info
                by_id[str(team_id)] = team_info
                all_names.append(cleaned_name)

                if abbreviation:
                    by_abbrev[abbreviation.lower()] = team_info

            except Exception:
                # Skip teams that fail cleaning
                continue

        return {
            'by_name': by_name,
            'by_abbrev': by_abbrev,
            'by_id': by_id,
            'all_names': all_names,
        }

    def get_team_lookup_dict(self) -> Dict:
        """
        Get the optimized team lookup dictionary.

        Lazy loads data on first call.

        Returns:
            Dictionary with by_name, by_abbrev, by_id, and all_names keys

        Raises:
            DataLoadError: If data cannot be loaded
        """
        # Lazy load on first access
        if self._teams_data is None or not self._is_cache_valid():
            self.load_teams()

        return self._teams_data

    def clear_cache(self) -> None:
        """Clear cached data (useful for testing)."""
        self._teams_data = None
        self._last_load_time = None
        self._raw_data = None
