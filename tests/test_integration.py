"""Integration tests for edge cases and end-to-end scenarios."""

import pytest
from unittest.mock import patch
import pandas as pd

from ncaa_d1_team_normalizer import TeamNormalizer, normalize_team
from ncaa_d1_team_normalizer.exceptions import UnknownTeamError


@pytest.fixture
def comprehensive_espn_data():
    """Fixture with comprehensive team data for edge case testing."""
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
            'display_name': 'Connecticut',
            'id': 41,
            'abbreviation': 'CONN',
            'location': 'Storrs',
            'nickname': 'Huskies',
            'name': 'Connecticut Huskies',
        },
        {
            'display_name': 'Massachusetts',
            'id': 113,
            'abbreviation': 'UMASS',
            'location': 'Amherst',
            'nickname': 'Minutemen',
            'name': 'UMass Minutemen',
        },
        {
            'display_name': 'Mississippi',
            'id': 145,
            'abbreviation': 'MISS',
            'location': 'Oxford',
            'nickname': 'Rebels',
            'name': 'Ole Miss Rebels',
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
        {
            'display_name': 'Miami (OH)',
            'id': 193,
            'abbreviation': 'MU',
            'location': 'Oxford',
            'nickname': 'RedHawks',
            'name': 'Miami (OH) RedHawks',
        },
        {
            'display_name': "St. John's (NY)",
            'id': 2599,
            'abbreviation': 'SJU',
            'location': 'Queens',
            'nickname': 'Red Storm',
            'name': "St. John's Red Storm",
        },
        {
            'display_name': "Saint Mary's (CA)",
            'id': 2608,
            'abbreviation': 'SMC',
            'location': 'Moraga',
            'nickname': 'Gaels',
            'name': "Saint Mary's Gaels",
        },
        {
            'display_name': 'Texas A&M',
            'id': 245,
            'abbreviation': 'A&M',
            'location': 'College Station',
            'nickname': 'Aggies',
            'name': 'Texas A&M Aggies',
        },
        {
            'display_name': 'Michigan State',
            'id': 127,
            'abbreviation': 'MSU',
            'location': 'East Lansing',
            'nickname': 'Spartans',
            'name': 'Michigan State Spartans',
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
            'display_name': 'NC State',
            'id': 152,
            'abbreviation': 'NCSU',
            'location': 'Raleigh',
            'nickname': 'Wolfpack',
            'name': 'NC State Wolfpack',
        },
        {
            'display_name': 'Villanova',
            'id': 222,
            'abbreviation': 'NOVA',
            'location': 'Villanova',
            'nickname': 'Wildcats',
            'name': 'Villanova Wildcats',
        },
        {
            'display_name': 'Syracuse',
            'id': 183,
            'abbreviation': 'SYR',
            'location': 'Syracuse',
            'nickname': 'Orange',
            'name': 'Syracuse Orange',
        },
    ])


class TestEdgeCases:
    """Test all specified edge cases from requirements."""

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    @pytest.mark.parametrize("input_name,expected_canonical", [
        # UConn edge case
        ("UConn", "Connecticut"),
        ("uconn", "Connecticut"),
        ("UCONN", "Connecticut"),

        # UMass edge case
        ("UMass", "Massachusetts"),
        ("umass", "Massachusetts"),
        ("UMASS", "Massachusetts"),

        # Ole Miss edge case
        ("Ole Miss", "Mississippi"),
        ("ole miss", "Mississippi"),
        ("OLE MISS", "Mississippi"),

        # Penn vs Penn State disambiguation
        ("Penn", "Pennsylvania"),
        ("penn", "Pennsylvania"),
        ("PENN", "Pennsylvania"),
        ("Penn State", "Penn State"),
        ("penn state", "Penn State"),
        ("PENN STATE", "Penn State"),

        # Miami disambiguation
        ("Miami (FL)", "Miami (FL)"),
        ("Miami FL", "Miami (FL)"),
        ("miami fl", "Miami (FL)"),
        ("Miami Florida", "Miami (FL)"),
        ("Miami (OH)", "Miami (OH)"),
        ("Miami OH", "Miami (OH)"),
        ("miami oh", "Miami (OH)"),
        ("Miami Ohio", "Miami (OH)"),

        # St. John's variants
        ("St Johns", "St. John's (NY)"),
        ("St. John's", "St. John's (NY)"),
        ("Saint Johns", "St. John's (NY)"),
        ("st johns", "St. John's (NY)"),

        # Saint Mary's variants
        ("St Marys", "Saint Mary's (CA)"),
        ("Saint Marys", "Saint Mary's (CA)"),
        ("st marys", "Saint Mary's (CA)"),

        # Texas A&M variants
        ("Texas A&M", "Texas A&M"),
        ("Texas A and M", "Texas A&M"),
        ("Texas AM", "Texas A&M"),
        ("texas a m", "Texas A&M"),

        # Michigan State variants
        ("Mich St", "Michigan State"),
        ("Michigan St.", "Michigan State"),
        ("Michigan St", "Michigan State"),
        ("Michigan State", "Michigan State"),
        ("mich state", "Michigan State"),

        # UNC/NC State
        ("UNC", "North Carolina"),
        ("unc", "North Carolina"),
        ("NC State", "NC State"),
        ("nc state", "NC State"),

        # Common nicknames
        ("Nova", "Villanova"),
        ("nova", "Villanova"),
        ("Cuse", "Syracuse"),
        ("cuse", "Syracuse"),
    ])
    def test_edge_cases(self, mock_espn, comprehensive_espn_data, input_name, expected_canonical):
        """Test all specified edge cases."""
        mock_espn.return_value = comprehensive_espn_data

        normalizer = TeamNormalizer()
        result = normalizer.normalize(input_name)

        assert result is not None, f"Failed to match: {input_name}"
        assert result['canonical_name'] == expected_canonical, \
            f"Expected {expected_canonical}, got {result['canonical_name']} for input {input_name}"

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    @pytest.mark.parametrize("input_name,expected_canonical", [
        # Mascot removal
        ("Duke Blue Devils", "Duke"),
        ("North Carolina Tar Heels", "North Carolina"),
        ("Connecticut Huskies", "Connecticut"),

        # Suffix removal
        ("Duke University", "Duke"),
        ("University of Connecticut", "Connecticut"),
        ("University of North Carolina", "North Carolina"),

        # Men's Basketball suffix
        ("Duke Men's Basketball", "Duke"),
        ("Connecticut Mens Basketball", "Connecticut"),
    ])
    def test_suffix_and_mascot_removal(self, mock_espn, comprehensive_espn_data, input_name, expected_canonical):
        """Test removal of mascots and suffixes."""
        mock_espn.return_value = comprehensive_espn_data

        normalizer = TeamNormalizer()
        result = normalizer.normalize(input_name)

        assert result is not None
        assert result['canonical_name'] == expected_canonical

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_whitespace_handling(self, mock_espn, comprehensive_espn_data):
        """Test proper handling of whitespace."""
        mock_espn.return_value = comprehensive_espn_data

        normalizer = TeamNormalizer()

        test_cases = [
            "  Duke  ",
            "Duke   ",
            "   Duke",
            "Duke",
        ]

        for test_case in test_cases:
            result = normalizer.normalize(test_case)
            assert result['canonical_name'] == 'Duke'

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_fuzzy_matching_typos(self, mock_espn, comprehensive_espn_data):
        """Test fuzzy matching handles typos."""
        mock_espn.return_value = comprehensive_espn_data

        normalizer = TeamNormalizer(fuzzy_threshold=80)

        # Common typos
        result = normalizer.normalize("Dook")
        assert result['canonical_name'] == 'Duke'
        assert result['match_method'] == 'fuzzy'
        assert result['confidence'] < 100

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_confidence_scoring(self, mock_espn, comprehensive_espn_data):
        """Test confidence scoring across match types."""
        mock_espn.return_value = comprehensive_espn_data

        normalizer = TeamNormalizer()

        # Exact match should be 100%
        exact_result = normalizer.normalize("Duke")
        assert exact_result['confidence'] == 100.0

        # Alias match should be 100%
        alias_result = normalizer.normalize("UConn")
        assert alias_result['confidence'] == 100.0

        # Fuzzy match should be < 100%
        fuzzy_result = normalizer.normalize("Dook")
        assert fuzzy_result['confidence'] < 100.0

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_convenience_function(self, mock_espn, comprehensive_espn_data):
        """Test the convenience normalize_team function."""
        mock_espn.return_value = comprehensive_espn_data

        result = normalize_team("UConn")
        assert result is not None
        assert result['canonical_name'] == 'Connecticut'

        # Test with raise_on_no_match
        with pytest.raises(UnknownTeamError):
            normalize_team("Fake University", raise_on_no_match=True)

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_batch_processing_performance(self, mock_espn, comprehensive_espn_data):
        """Test batch processing works correctly."""
        mock_espn.return_value = comprehensive_espn_data

        normalizer = TeamNormalizer()

        teams = ["Duke", "UConn", "UNC", "Penn State", "Miami FL"] * 20
        results = normalizer.normalize_batch(teams)

        assert len(results) == len(teams)
        assert all(r is not None for r in results)

        # Verify correct mappings
        assert results[0]['canonical_name'] == 'Duke'
        assert results[1]['canonical_name'] == 'Connecticut'
        assert results[2]['canonical_name'] == 'North Carolina'
        assert results[3]['canonical_name'] == 'Penn State'
        assert results[4]['canonical_name'] == 'Miami (FL)'

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_match_method_tracking(self, mock_espn, comprehensive_espn_data):
        """Test that match method is correctly tracked."""
        mock_espn.return_value = comprehensive_espn_data

        normalizer = TeamNormalizer()

        # Exact match
        exact = normalizer.normalize("Duke")
        assert exact['match_method'] == 'exact'

        # Alias match
        alias = normalizer.normalize("UConn")
        assert alias['match_method'] == 'alias'

        # Fuzzy match
        fuzzy = normalizer.normalize("Dook")
        assert fuzzy['match_method'] == 'fuzzy'


class TestEndToEnd:
    """End-to-end integration tests."""

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_complete_workflow(self, mock_espn, comprehensive_espn_data):
        """Test complete normalization workflow."""
        mock_espn.return_value = comprehensive_espn_data

        # Initialize normalizer
        normalizer = TeamNormalizer(fuzzy_threshold=85, raise_on_no_match=False)

        # Test various inputs
        test_cases = [
            ("UCONN HUSKIES", "Connecticut"),
            ("University of Connecticut Men's Basketball", "Connecticut"),
            ("Penn", "Pennsylvania"),
            ("Penn State Nittany Lions", "Penn State"),
            ("Miami Hurricanes", "Miami (FL)"),
            ("The U", "Miami (FL)"),
            ("St. John's Red Storm", "St. John's (NY)"),
        ]

        for input_name, expected in test_cases:
            result = normalizer.normalize(input_name)
            assert result is not None, f"Failed to match: {input_name}"
            assert result['canonical_name'] == expected, \
                f"Expected {expected}, got {result['canonical_name']} for {input_name}"
            assert 'espn_id' in result
            assert 'abbreviation' in result
            assert 'confidence' in result
            assert 'match_method' in result

    @patch('sportsdataverse.mbb.espn_mbb_teams')
    def test_error_handling_workflow(self, mock_espn, comprehensive_espn_data):
        """Test error handling in complete workflow."""
        mock_espn.return_value = comprehensive_espn_data

        # Test with raise_on_no_match=False (default)
        normalizer_lenient = TeamNormalizer()
        result = normalizer_lenient.normalize("Completely Fake Team XYZ")
        assert result is None

        # Test with raise_on_no_match=True
        normalizer_strict = TeamNormalizer(raise_on_no_match=True)
        with pytest.raises(UnknownTeamError) as exc_info:
            normalizer_strict.normalize("Completely Fake Team XYZ")
        assert "Completely Fake Team XYZ" in str(exc_info.value)
