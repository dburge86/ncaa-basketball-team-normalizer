"""Text cleaning utilities for team name normalization."""

import re
from typing import Optional

from .exceptions import InvalidInputError


class TextCleaner:
    """Static methods for cleaning and normalizing team name text."""

    # Common suffixes to remove (lowercase)
    # Note: Do NOT include "state university" as it would incorrectly remove "State"
    # from teams like "Michigan State University"
    SUFFIXES_TO_REMOVE = [
        'university',
        'college',
        'mens basketball',
        "men's basketball",
        'mens',
        "men's",
        'basketball',

        # Mascots (common ones)
        'wildcats',
        'bulldogs',
        'tigers',
        'bears',
        'eagles',
        'panthers',
        'lions',
        'hawks',
        'cougars',
        'huskies',
        'spartans',
        'blue devils',
        'tar heels',
        'jayhawks',
        'orange',
        'cardinals',
        'trojans',
        'bruins',
        'wolverines',
        'buckeyes',
        'fighting irish',
        'crimson tide',
        'hoosiers',
        'terrapins',
        'terps',
        'cavaliers',
        'hokies',
        'demon deacons',
        'hurricane',
        'hurricanes',
        'seminoles',
        'gators',
        'aggies',
        'longhorns',
        'sooners',
        'cyclones',
        'mountaineers',
        'scarlet knights',
        'golden gophers',
        'cornhuskers',
        'badgers',
        'nittany lions',
        'boilermakers',
        'hawkeyes',
        'wildcats',
        'rebels',
        'commodores',
        'razorbacks',
        'volunteers',
        'vols',
        'gamecocks',
        'red storm',
        'friars',
        'musketeers',
        'pirates',
        'raiders',
        'rams',
        'ramblers',
        'peacocks',
        'golden eagles',
        'blue jays',
        'hoya',
        'hoyas',
        'redmen',
    ]

    @staticmethod
    def clean(text: str) -> str:
        """
        Full cleaning pipeline for team names.

        Args:
            text: Raw team name string

        Returns:
            Cleaned string ready for matching

        Raises:
            InvalidInputError: If input is None, empty, or not a string
        """
        # Validate input
        if text is None:
            raise InvalidInputError("Team name cannot be None")
        if not isinstance(text, str):
            raise InvalidInputError(f"Team name must be a string, got {type(text).__name__}")
        if not text.strip():
            raise InvalidInputError("Team name cannot be empty")

        # Apply cleaning steps
        cleaned = text.strip()
        cleaned = cleaned.lower()
        cleaned = TextCleaner.remove_punctuation(cleaned)
        cleaned = TextCleaner.remove_suffixes(cleaned)
        cleaned = TextCleaner.normalize_whitespace(cleaned)

        return cleaned

    @staticmethod
    def remove_punctuation(text: str) -> str:
        """
        Remove punctuation while preserving apostrophes and hyphens in context.

        Examples:
            "St. John's" -> "St Johns" (period removed, apostrophe handled)
            "Texas A&M" -> "Texas A M" (ampersand to space)
        """
        # Replace ampersands with space
        text = text.replace('&', ' ')

        # Remove periods and other punctuation except apostrophes and hyphens
        # We'll handle apostrophes specially
        text = re.sub(r'[^\w\s\'-]', ' ', text)

        # Remove apostrophes (St. John's -> St Johns)
        text = text.replace("'", "")

        return text

    @staticmethod
    def remove_suffixes(text: str) -> str:
        """
        Remove common suffixes like 'university', 'college', mascot names.

        Examples:
            "duke university" -> "duke"
            "duke blue devils" -> "duke"
        """
        words = text.split()

        # Remove "of" connector phrases (University of X -> X)
        if 'of' in words:
            try:
                of_index = words.index('of')
                # If pattern is "University of X", keep everything after "of"
                if of_index > 0 and words[of_index - 1] in ['university', 'college']:
                    words = words[of_index + 1:]
            except ValueError:
                pass

        # Remove suffixes from the end
        # Sort suffixes by length (longest first) to handle multi-word suffixes
        sorted_suffixes = sorted(TextCleaner.SUFFIXES_TO_REMOVE, key=len, reverse=True)

        text = ' '.join(words)

        for suffix in sorted_suffixes:
            # Remove suffix if it appears at the end
            pattern = r'\b' + re.escape(suffix) + r'\b\s*$'
            text = re.sub(pattern, '', text)

        return text.strip()

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """
        Normalize multiple spaces to single space and strip.

        Examples:
            "duke  blue" -> "duke blue"
            "  duke  " -> "duke"
        """
        return re.sub(r'\s+', ' ', text).strip()
