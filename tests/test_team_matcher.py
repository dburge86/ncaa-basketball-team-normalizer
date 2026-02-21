"""Unit tests for TeamNormalizer."""

import pytest
from unittest.mock import patch, MagicMock
import pandas as pd

from ncaa_d1_team_normalizer.team_matcher import TeamNormalizer
from ncaa_d1_team_normalizer.exceptions import UnknownTeamError, InvalidInputError


@pytest.fixture
def mock_espn_data():
    """Fixture providing mock ESPN data."""
    return pd.DataFrame([
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
        {
            'display_name': 'Connecticut',
            'id': 41,
            'abbreviation': 'CONN',
            'location': 'Storrs',
            'nickname': 'Huskies',
            'name': 'Connecticut Huskies',
        },
        {
            'display_name': 'Pennsylvania',
            'id': 219,
            'abbreviation': 'PENN',
            'location': 'Philadelphia',
            'nickname': 'Quakers',
            'name': 'Pennsylvania Quakers',
        },
        {
            'display_name': 'Penn State',
            'id': 213,
            'abbreviation': 'PSU',
            'location': 'University Park',
            'nickname': 'Nittany Lions',
            'name': 'Penn State Nittany Lions',
        },
        {
            'display_name': 'Miami (FL)',
            'id': 2390,
            'abbreviation': 'MIA',
            'location': 'Coral Gables',
            'nickname': 'Hurricanes',
            'name': 'Miami Hurricanes',
        },
    ])


class TestTeamNormalizer:
    """Tests for TeamNormalizer class."""

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_exact_match(self, mock_espn, mock_espn_data):
        """Test exact matching."""
        mock_espn.return_value = mock_espn_data

        normalizer = TeamNormalizer()
        result = normalizer.normalize('Duke')

        assert result is not None
        assert result['canonical_name'] == 'Duke'
        assert result['espn_id'] == '150'
        assert result['confidence'] == 100.0
        assert result['match_method'] == 'exact'

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_case_insensitive(self, mock_espn, mock_espn_data):
        """Test case insensitive matching."""
        mock_espn.return_value = mock_espn_data

        normalizer = TeamNormalizer()

        result1 = normalizer.normalize('DUKE')
        result2 = normalizer.normalize('duke')
        result3 = normalizer.normalize('Duke')

        assert result1['canonical_name'] == 'Duke'
        assert result2['canonical_name'] == 'Duke'
        assert result3['canonical_name'] == 'Duke'

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_alias_match(self, mock_espn, mock_espn_data):
        """Test alias matching."""
        mock_espn.return_value = mock_espn_data

        normalizer = TeamNormalizer()

        # UConn -> Connecticut
        result = normalizer.normalize('UConn')
        assert result is not None
        assert result['canonical_name'] == 'Connecticut'
        assert result['match_method'] == 'alias'
        assert result['confidence'] == 100.0

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_fuzzy_match(self, mock_espn, mock_espn_data):
        """Test fuzzy matching."""
        mock_espn.return_value = mock_espn_data

        normalizer = TeamNormalizer(fuzzy_threshold=80)

        # Typo: Dook -> Duke
        result = normalizer.normalize('Dook')
        assert result is not None
        assert result['canonical_name'] == 'Duke'
        assert result['match_method'] == 'fuzzy'
        assert result['confidence'] < 100.0

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_no_match_returns_none(self, mock_espn, mock_espn_data):
        """Test that no match returns None by default."""
        mock_espn.return_value = mock_espn_data

        normalizer = TeamNormalizer(raise_on_no_match=False)
        result = normalizer.normalize('Fake University')
        assert result is None

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_no_match_raises_error(self, mock_espn, mock_espn_data):
        """Test that no match raises error when configured."""
        mock_espn.return_value = mock_espn_data

        normalizer = TeamNormalizer(raise_on_no_match=True)
        with pytest.raises(UnknownTeamError, match="Fake University"):
            normalizer.normalize('Fake University')

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_invalid_input(self, mock_espn, mock_espn_data):
        """Test invalid input handling."""
        mock_espn.return_value = mock_espn_data

        normalizer = TeamNormalizer()

        with pytest.raises(InvalidInputError, match="cannot be None"):
            normalizer.normalize(None)

        with pytest.raises(InvalidInputError, match="must be a string"):
            normalizer.normalize(123)

        with pytest.raises(InvalidInputError, match="cannot be empty"):
            normalizer.normalize("")

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_batch_processing(self, mock_espn, mock_espn_data):
        """Test batch normalization."""
        mock_espn.return_value = mock_espn_data

        normalizer = TeamNormalizer()
        teams = ['Duke', 'UConn', 'North Carolina']
        results = normalizer.normalize_batch(teams)

        assert len(results) == 3
        assert results[0]['canonical_name'] == 'Duke'
        assert results[1]['canonical_name'] == 'Connecticut'
        assert results[2]['canonical_name'] == 'North Carolina'

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_penn_disambiguation(self, mock_espn, mock_espn_data):
        """Test Penn vs Penn State disambiguation."""
        mock_espn.return_value = mock_espn_data

        normalizer = TeamNormalizer()

        result_penn = normalizer.normalize('Penn')
        assert result_penn['canonical_name'] == 'Pennsylvania'

        result_penn_state = normalizer.normalize('Penn State')
        assert result_penn_state['canonical_name'] == 'Penn State'

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_whitespace_handling(self, mock_espn, mock_espn_data):
        """Test whitespace handling."""
        mock_espn.return_value = mock_espn_data

        normalizer = TeamNormalizer()

        result = normalizer.normalize('  Duke  ')
        assert result['canonical_name'] == 'Duke'

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_get_all_teams(self, mock_espn, mock_espn_data):
        """Test getting all teams."""
        mock_espn.return_value = mock_espn_data

        normalizer = TeamNormalizer()
        all_teams = normalizer.get_all_teams()

        assert len(all_teams) > 0
        assert all(isinstance(team, dict) for team in all_teams)
        assert all('canonical_name' in team for team in all_teams)
        assert all('espn_id' in team for team in all_teams)
