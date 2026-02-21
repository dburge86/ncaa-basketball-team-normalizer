"""Functional tests using real ESPN data (requires network access)."""

import pytest

from ncaa_d1_team_normalizer import TeamNormalizer, normalize_team


@pytest.mark.functional
class TestFunctionalWithRealData:
    """
    Functional tests that use real ESPN data.

    Run with: pytest -v -m functional

    These tests require network access and may be slower.
    """

    def test_normalize_duke(self):
        """Test normalizing Duke."""
        result = normalize_team("Duke")
        assert result is not None
        assert result['canonical_name'] == 'Duke'
        assert result['match_method'] == 'exact'
        assert result['confidence'] == 100.0

    def test_normalize_uconn(self):
        """Test UConn alias."""
        result = normalize_team("UConn")
        assert result is not None
        assert result['canonical_name'] == 'Connecticut'
        assert result['match_method'] in ['alias', 'exact', 'fuzzy']

    def test_normalize_typo(self):
        """Test fuzzy matching with typo."""
        result = normalize_team("Dook", fuzzy_threshold=80)
        assert result is not None
        # Should match Duke
        assert 'Duke' in result['canonical_name']
        assert result['match_method'] == 'fuzzy'
        assert result['confidence'] < 100

    def test_batch_processing(self):
        """Test batch normalization."""
        normalizer = TeamNormalizer()
        teams = ["Duke", "UConn", "North Carolina"]
        results = normalizer.normalize_batch(teams)

        assert len(results) == 3
        assert all(r is not None for r in results)

    def test_get_all_teams(self):
        """Test getting all teams."""
        normalizer = TeamNormalizer()
        all_teams = normalizer.get_all_teams()

        # Should have a reasonable number of D1 teams
        assert len(all_teams) > 300  # D1 has 350+ teams
        assert len(all_teams) < 400

        # Check structure
        for team in all_teams[:5]:  # Check first 5
            assert 'canonical_name' in team
            assert 'espn_id' in team
            assert 'abbreviation' in team
