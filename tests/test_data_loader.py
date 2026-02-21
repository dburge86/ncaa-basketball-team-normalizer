"""Unit tests for ESPNDataLoader."""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import pandas as pd

from ncaa_d1_team_normalizer.data_loader import ESPNDataLoader
from ncaa_d1_team_normalizer.exceptions import DataLoadError


class TestESPNDataLoader:
    """Tests for ESPNDataLoader class."""

    def setup_method(self):
        """Clear cache before each test."""
        loader = ESPNDataLoader()
        loader.clear_cache()

    def test_singleton_pattern(self):
        """Test that ESPNDataLoader is a singleton."""
        loader1 = ESPNDataLoader()
        loader2 = ESPNDataLoader()
        assert loader1 is loader2

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_load_teams_success(self, mock_espn):
        """Test successful team data loading."""
        # Mock ESPN data
        mock_data = pd.DataFrame([
            {
                'display_name': 'Duke',
                'id': 150,
                'abbreviation': 'DUKE',
                'location': 'Durham',
                'nickname': 'Blue Devils',
                'name': 'Duke Blue Devils',
            },
            {
                'display_name': 'North Carolina',
                'id': 153,
                'abbreviation': 'UNC',
                'location': 'Chapel Hill',
                'nickname': 'Tar Heels',
                'name': 'North Carolina Tar Heels',
            },
        ])
        mock_espn.return_value = mock_data

        loader = ESPNDataLoader()
        loader.load_teams()

        # Verify data was loaded
        lookup = loader.get_team_lookup_dict()
        assert 'by_name' in lookup
        assert 'duke' in lookup['by_name']
        assert 'north carolina' in lookup['by_name']
        assert lookup['by_name']['duke']['team_id'] == '150'

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_load_teams_empty_response(self, mock_espn):
        """Test handling of empty ESPN response."""
        mock_espn.return_value = pd.DataFrame()

        loader = ESPNDataLoader()
        with pytest.raises(DataLoadError, match="empty team data"):
            loader.load_teams()

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_load_teams_retry_logic(self, mock_espn):
        """Test retry logic on failure."""
        # Fail first 2 attempts, succeed on 3rd
        mock_espn.side_effect = [
            Exception("Network error"),
            Exception("Network error"),
            pd.DataFrame([{
                'display_name': 'Duke',
                'id': 150,
                'abbreviation': 'DUKE',
                'location': 'Durham',
                'nickname': 'Blue Devils',
                'name': 'Duke',
            }])
        ]

        loader = ESPNDataLoader()
        loader.load_teams(max_retries=3)

        # Should succeed after retries
        assert loader._teams_data is not None

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_load_teams_max_retries_exceeded(self, mock_espn):
        """Test failure after max retries."""
        mock_espn.side_effect = Exception("Network error")

        loader = ESPNDataLoader()
        with pytest.raises(DataLoadError, match="Failed to load ESPN data"):
            loader.load_teams(max_retries=2)

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_cache_validity(self, mock_espn):
        """Test cache TTL logic."""
        mock_data = pd.DataFrame([{
            'display_name': 'Duke',
            'id': 150,
            'abbreviation': 'DUKE',
            'location': 'Durham',
            'nickname': 'Blue Devils',
            'name': 'Duke',
        }])
        mock_espn.return_value = mock_data

        loader = ESPNDataLoader()
        loader.load_teams()

        # Should use cache on second call
        call_count_after_first = mock_espn.call_count
        loader.get_team_lookup_dict()
        assert mock_espn.call_count == call_count_after_first

        # Manually expire cache
        loader._last_load_time = datetime.now() - timedelta(hours=25)
        loader.get_team_lookup_dict()
        assert mock_espn.call_count > call_count_after_first

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_force_refresh(self, mock_espn):
        """Test force refresh bypasses cache."""
        mock_data = pd.DataFrame([{
            'display_name': 'Duke',
            'id': 150,
            'abbreviation': 'DUKE',
            'location': 'Durham',
            'nickname': 'Blue Devils',
            'name': 'Duke',
        }])
        mock_espn.return_value = mock_data

        loader = ESPNDataLoader()
        loader.load_teams()
        call_count = mock_espn.call_count

        # Force refresh should reload
        loader.load_teams(force_refresh=True)
        assert mock_espn.call_count > call_count

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_lookup_dict_structure(self, mock_espn):
        """Test structure of lookup dictionary."""
        mock_data = pd.DataFrame([{
            'display_name': 'Duke',
            'id': 150,
            'abbreviation': 'DUKE',
            'location': 'Durham',
            'nickname': 'Blue Devils',
            'name': 'Duke Blue Devils',
        }])
        mock_espn.return_value = mock_data

        loader = ESPNDataLoader()
        lookup = loader.get_team_lookup_dict()

        assert 'by_name' in lookup
        assert 'by_abbrev' in lookup
        assert 'by_id' in lookup
        assert 'all_names' in lookup

        assert 'duke' in lookup['by_name']
        assert 'duke' in lookup['by_abbrev']
        assert '150' in lookup['by_id']
        assert 'duke' in lookup['all_names']
