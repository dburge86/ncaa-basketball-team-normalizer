# NCAA D1 Men's Basketball Team Name Normalizer

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A production-ready Python package that normalizes NCAA Division I Men's Basketball team names to ESPN's canonical format. Solves the problem of inconsistent team naming across different data sources (sportsbooks, scrapers, APIs).

> **⚠️ Python Version Requirement**: This package requires **Python 3.11 or 3.12**. Python 3.14 is not yet supported due to a dependency issue with `sportsdataverse`.

## Problem Statement

Sports data comes in various formats:
- "UConn", "Connecticut", "UCONN Huskies", "University of Connecticut Men's Basketball" all refer to the same team
- Classic edge cases cause failures: UConn/Connecticut, Penn/Penn State, Miami (FL)/Miami (OH)
- Manual mapping is error-prone and doesn't scale

This package provides reliable normalization with >95% accuracy for common variants.

## Features

- **Multi-step matching pipeline**: Exact match → Alias lookup → Fuzzy matching
- **Handles edge cases**: UConn/Connecticut, Penn/Penn State, Miami disambiguation, punctuation variants
- **High performance**: Singleton pattern with 24-hour cache, batch processing support
- **Confidence scoring**: Track match quality and method for downstream validation
- **Flexible error handling**: Configurable behavior for unmatched teams
- **Type-safe**: Full type hints for modern Python development

## Installation

**Requirements**: Python 3.11 or 3.12

```bash
# Ensure you're using Python 3.11 or 3.12
python3.11 -m venv venv
# or
python3.12 -m venv venv

source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install ncaa_d1_team_normalizer
```

For development:

```bash
git clone https://github.com/dburge86/ncaa-basketball-team-normalizer.git
cd ncaa-basketball-team-normalizer

# Create venv with Python 3.11 or 3.12
python3.11 -m venv venv
source venv/bin/activate

pip install -e ".[dev]"
```

## Quick Start

### Basic Usage

```python
from ncaa_d1_team_normalizer import normalize_team

# Simple normalization
result = normalize_team("UConn")
print(result)
# {
#     'canonical_name': 'Connecticut',
#     'espn_id': '41',
#     'abbreviation': 'CONN',
#     'confidence': 100.0,
#     'match_method': 'alias'
# }

# Handles various formats
normalize_team("UCONN HUSKIES")  # → Connecticut
normalize_team("University of Connecticut")  # → Connecticut
normalize_team("Penn")  # → Pennsylvania (not Penn State!)
normalize_team("Miami FL")  # → Miami (FL)
```

### Advanced Usage

```python
from ncaa_d1_team_normalizer import TeamNormalizer, UnknownTeamError

# Initialize with custom configuration
normalizer = TeamNormalizer(
    fuzzy_threshold=85,  # Minimum similarity score (0-100)
    raise_on_no_match=True  # Raise exception instead of returning None
)

# Normalize a single team
try:
    result = normalizer.normalize("Dook")  # Typo
    print(f"Matched: {result['canonical_name']}")  # Duke
    print(f"Confidence: {result['confidence']}")  # ~90% (fuzzy match)
except UnknownTeamError as e:
    print(f"No match found: {e.team_name}")

# Batch processing (efficient for multiple teams)
teams = ["Duke", "UNC", "Kentucky", "Kansas", "UConn"]
results = normalizer.normalize_batch(teams)

for team, result in zip(teams, results):
    if result:
        print(f"{team} → {result['canonical_name']}")

# Get all available teams
all_teams = normalizer.get_all_teams()
print(f"Total teams: {len(all_teams)}")
```

## Edge Cases Handled

### Team Name Disambiguation

```python
# Penn vs Penn State
normalize_team("Penn")  # → Pennsylvania
normalize_team("Penn State")  # → Penn State

# Miami variants
normalize_team("Miami FL")  # → Miami (FL)
normalize_team("Miami OH")  # → Miami (OH)
normalize_team("The U")  # → Miami (FL)
```

### Common Abbreviations

```python
normalize_team("UConn")  # → Connecticut
normalize_team("UMass")  # → Massachusetts
normalize_team("Ole Miss")  # → Mississippi
normalize_team("UNC")  # → North Carolina
normalize_team("NC State")  # → NC State
normalize_team("Nova")  # → Villanova
```

### Punctuation Variants

```python
normalize_team("St. John's")  # → St. John's (NY)
normalize_team("St Johns")  # → St. John's (NY)
normalize_team("Texas A&M")  # → Texas A&M
normalize_team("Texas A and M")  # → Texas A&M
```

### Suffix Removal

```python
normalize_team("Duke Blue Devils")  # → Duke
normalize_team("University of North Carolina")  # → North Carolina
normalize_team("Kentucky Wildcats")  # → Kentucky
normalize_team("Duke Men's Basketball")  # → Duke
```

## API Reference

### `normalize_team(team_name, fuzzy_threshold=85, raise_on_no_match=False)`

Convenience function for quick one-off normalization.

**Parameters:**
- `team_name` (str): Team name to normalize
- `fuzzy_threshold` (int): Minimum fuzzy match score (0-100)
- `raise_on_no_match` (bool): If True, raise `UnknownTeamError` when no match found

**Returns:**
- Dictionary with canonical team info, or None if no match found

**Raises:**
- `InvalidInputError`: If input validation fails
- `UnknownTeamError`: If `raise_on_no_match=True` and no match found

### `TeamNormalizer`

Main class for team normalization.

#### `__init__(fuzzy_threshold=85, raise_on_no_match=False)`

Initialize the normalizer with custom configuration.

#### `normalize(team_name: str) -> dict | None`

Normalize a single team name.

**Returns:**
```python
{
    'canonical_name': str,  # ESPN canonical name
    'espn_id': str,  # ESPN team ID
    'abbreviation': str,  # Team abbreviation
    'confidence': float,  # Match confidence (0-100)
    'match_method': str  # 'exact', 'alias', or 'fuzzy'
}
```

#### `normalize_batch(team_names: list[str]) -> list[dict | None]`

Normalize multiple teams efficiently.

#### `get_all_teams() -> list[dict]`

Get list of all available Division I teams.

## How It Works

### Multi-Step Matching Pipeline

1. **Input Validation**: Check for None, empty, or non-string input
2. **Text Cleaning**: Lowercase, remove punctuation, strip suffixes/mascots
3. **Exact Match**: Compare against ESPN canonical names
4. **Alias Lookup**: Check hardcoded dictionary of common variants
5. **Fuzzy Match**: Use RapidFuzz for similarity matching (configurable threshold)

### Data Source

Team data is fetched from ESPN via the `sportsdataverse` package, ensuring up-to-date and accurate information.

### Caching Strategy

- **Singleton pattern**: Single shared instance prevents redundant API calls
- **24-hour TTL**: Cached data expires after 24 hours
- **Lazy loading**: Data fetched only when first needed
- **Manual refresh**: Use `load_teams(force_refresh=True)` to bypass cache

## Testing

Run the test suite:

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests with coverage
pytest tests/ -v --cov=ncaa_d1_team_normalizer --cov-report=term-missing

# Run specific test file
pytest tests/test_integration.py -v

# Run edge case tests only
pytest tests/test_integration.py::TestEdgeCases -v
```

## Performance

- **Batch processing**: ~500 teams per second
- **Cache hit**: < 1ms per lookup
- **Cold start**: ~2-3 seconds (ESPN data fetch)
- **Memory footprint**: ~10MB (cached team data)

## Exceptions

### `TeamNormalizerError`

Base exception for all normalizer errors.

### `UnknownTeamError`

Raised when no match is found (only if `raise_on_no_match=True`).

```python
normalizer = TeamNormalizer(raise_on_no_match=True)
try:
    normalizer.normalize("Fake University")
except UnknownTeamError as e:
    print(f"Team not found: {e.team_name}")
```

### `DataLoadError`

Raised when ESPN data cannot be loaded.

### `InvalidInputError`

Raised when input validation fails (None, empty string, wrong type).

## Use Cases

### Sports Betting Data Aggregation

```python
from ncaa_d1_team_normalizer import TeamNormalizer

normalizer = TeamNormalizer()

# Normalize teams from different sportsbooks
draftkings_teams = ["UCONN", "Duke Blue Devils", "UNC"]
fanduel_teams = ["Connecticut", "Duke", "North Carolina"]

# Consolidate to common format
dk_normalized = normalizer.normalize_batch(draftkings_teams)
fd_normalized = normalizer.normalize_batch(fanduel_teams)

# Now you can match and compare odds across books
```

### Web Scraping

```python
# Handle various naming conventions from scraped data
scraped_names = [
    "University of Connecticut Men's Basketball",
    "Penn State Nittany Lions",
    "Miami (FL) Hurricanes"
]

results = normalizer.normalize_batch(scraped_names)
canonical_names = [r['canonical_name'] for r in results if r]
```

### Data Pipeline Integration

```python
import pandas as pd

# Normalize team names in a DataFrame
df = pd.DataFrame({
    'team': ['UConn', 'Duke', 'UNC', 'Kentucky'],
    'score': [75, 82, 69, 91]
})

normalizer = TeamNormalizer()
df['canonical_team'] = df['team'].apply(
    lambda x: normalizer.normalize(x)['canonical_name']
    if normalizer.normalize(x) else None
)
df['espn_id'] = df['team'].apply(
    lambda x: normalizer.normalize(x)['espn_id']
    if normalizer.normalize(x) else None
)
```

## Contributing

Contributions are welcome! Areas for improvement:

1. **Alias expansion**: Add more team name variants to `aliases.py`
2. **Performance optimization**: Improve fuzzy matching speed
3. **Additional sports**: Extend to women's basketball, football, etc.
4. **CLI tool**: Add command-line interface for quick lookups

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Data provided by [sportsdataverse](https://github.com/sportsdataverse/sportsdataverse-py)
- Fuzzy matching powered by [RapidFuzz](https://github.com/maxbachmann/RapidFuzz)

## Support

- **Issues**: https://github.com/dburge86/ncaa-basketball-team-normalizer/issues
- **Documentation**: https://github.com/dburge86/ncaa-basketball-team-normalizer

## Changelog

### 0.1.0 (2026-02-21)

- Initial release
- Multi-step matching pipeline (exact, alias, fuzzy)
- Comprehensive edge case handling
- Batch processing support
- >90% test coverage
