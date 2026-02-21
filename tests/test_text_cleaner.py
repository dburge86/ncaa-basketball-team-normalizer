"""Unit tests for TextCleaner."""

import pytest
from ncaa_d1_team_normalizer.text_cleaner import TextCleaner
from ncaa_d1_team_normalizer.exceptions import InvalidInputError


class TestTextCleaner:
    """Tests for TextCleaner class."""

    def test_clean_basic(self):
        """Test basic cleaning."""
        assert TextCleaner.clean("Duke") == "duke"
        assert TextCleaner.clean("  Duke  ") == "duke"
        assert TextCleaner.clean("DUKE") == "duke"

    def test_clean_with_university(self):
        """Test removal of 'university' suffix."""
        assert TextCleaner.clean("Duke University") == "duke"
        assert TextCleaner.clean("University of Connecticut") == "connecticut"
        assert TextCleaner.clean("University of North Carolina") == "north carolina"

    def test_clean_with_mascot(self):
        """Test removal of mascot names."""
        assert TextCleaner.clean("Duke Blue Devils") == "duke"
        assert TextCleaner.clean("North Carolina Tar Heels") == "north carolina"
        assert TextCleaner.clean("Kentucky Wildcats") == "kentucky"

    def test_clean_with_punctuation(self):
        """Test punctuation removal."""
        assert TextCleaner.clean("St. John's") == "st johns"
        assert TextCleaner.clean("Texas A&M") == "texas a m"
        assert TextCleaner.clean("Saint Mary's") == "saint marys"

    def test_clean_multiple_spaces(self):
        """Test whitespace normalization."""
        assert TextCleaner.clean("Duke   Blue   Devils") == "duke"
        assert TextCleaner.clean("North  Carolina") == "north carolina"

    def test_clean_invalid_input(self):
        """Test invalid input handling."""
        with pytest.raises(InvalidInputError, match="cannot be None"):
            TextCleaner.clean(None)

        with pytest.raises(InvalidInputError, match="must be a string"):
            TextCleaner.clean(123)

        with pytest.raises(InvalidInputError, match="cannot be empty"):
            TextCleaner.clean("")

        with pytest.raises(InvalidInputError, match="cannot be empty"):
            TextCleaner.clean("   ")

    def test_remove_punctuation(self):
        """Test punctuation removal method."""
        # Note: periods become spaces, whitespace normalization happens later
        assert TextCleaner.remove_punctuation("St. John's") == "St  Johns"
        assert TextCleaner.remove_punctuation("Texas A&M") == "Texas A M"
        result = TextCleaner.remove_punctuation("test!@#$%")
        assert "test" in result  # Punctuation removed, spaces remain

    def test_remove_suffixes(self):
        """Test suffix removal method."""
        assert TextCleaner.remove_suffixes("duke university") == "duke"
        assert TextCleaner.remove_suffixes("duke blue devils") == "duke"
        assert TextCleaner.remove_suffixes("university of kentucky") == "kentucky"
        assert TextCleaner.remove_suffixes("mens basketball") == ""

    def test_normalize_whitespace(self):
        """Test whitespace normalization method."""
        assert TextCleaner.normalize_whitespace("duke  blue") == "duke blue"
        assert TextCleaner.normalize_whitespace("  duke  ") == "duke"
        assert TextCleaner.normalize_whitespace("a   b   c") == "a b c"

    def test_edge_cases(self):
        """Test edge cases for cleaning."""
        # Men's basketball suffix
        assert TextCleaner.clean("Duke Men's Basketball") == "duke"

        # College suffix - removed as suffix
        assert TextCleaner.clean("Boston College") == "boston"

        # State University - should preserve "State" when it's part of the team name
        assert TextCleaner.clean("Michigan State University") == "michigan state"
