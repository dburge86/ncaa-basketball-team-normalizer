"""
Demo script showing how the NCAA D1 Team Normalizer works.

NOTE: This requires Python 3.11 or 3.12 due to sportsdataverse dependency.

Run with: python demo.py
"""

from ncaa_d1_team_normalizer import TeamNormalizer, normalize_team, UnknownTeamError


def main():
    print("=" * 60)
    print("NCAA D1 Men's Basketball Team Name Normalizer - Demo")
    print("=" * 60)
    print()

    # Example 1: Simple normalization
    print("Example 1: Simple Normalization")
    print("-" * 40)
    result = normalize_team("Duke")
    print(f"Input: 'Duke'")
    print(f"Result: {result}")
    print()

    # Example 2: Alias matching (UConn → Connecticut)
    print("Example 2: Alias Matching")
    print("-" * 40)
    result = normalize_team("UConn")
    print(f"Input: 'UConn'")
    print(f"Result: {result}")
    print()

    # Example 3: Suffix removal
    print("Example 3: Suffix Removal")
    print("-" * 40)
    result = normalize_team("University of Connecticut Men's Basketball")
    print(f"Input: 'University of Connecticut Men's Basketball'")
    print(f"Result: {result}")
    print()

    # Example 4: Penn vs Penn State disambiguation
    print("Example 4: Disambiguation")
    print("-" * 40)
    result1 = normalize_team("Penn")
    result2 = normalize_team("Penn State")
    print(f"Input: 'Penn' → {result1['canonical_name']}")
    print(f"Input: 'Penn State' → {result2['canonical_name']}")
    print()

    # Example 5: Fuzzy matching
    print("Example 5: Fuzzy Matching (typo)")
    print("-" * 40)
    result = normalize_team("Dook", fuzzy_threshold=80)
    print(f"Input: 'Dook' (typo)")
    print(f"Result: {result}")
    print(f"Confidence: {result['confidence']:.1f}%")
    print()

    # Example 6: Batch processing
    print("Example 6: Batch Processing")
    print("-" * 40)
    normalizer = TeamNormalizer()
    teams = ["Duke", "UNC", "Kentucky", "Kansas", "UConn"]
    results = normalizer.normalize_batch(teams)

    print("Batch input:", teams)
    print("\nResults:")
    for team, result in zip(teams, results):
        if result:
            print(f"  {team:15} → {result['canonical_name']}")
    print()

    # Example 7: Error handling
    print("Example 7: Error Handling")
    print("-" * 40)

    # Lenient mode (default)
    result = normalize_team("Fake University")
    print(f"Lenient mode - 'Fake University': {result}")

    # Strict mode
    try:
        strict_normalizer = TeamNormalizer(raise_on_no_match=True)
        strict_normalizer.normalize("Fake University")
    except UnknownTeamError as e:
        print(f"Strict mode - 'Fake University': Raised {type(e).__name__}")
    print()

    # Example 8: Get all teams
    print("Example 8: Get All Available Teams")
    print("-" * 40)
    all_teams = normalizer.get_all_teams()
    print(f"Total D1 teams available: {len(all_teams)}")
    print(f"\nFirst 5 teams:")
    for team in all_teams[:5]:
        print(f"  - {team['canonical_name']} ({team['abbreviation']})")
    print()

    print("=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError running demo: {e}")
        print("\nNOTE: This requires Python 3.11 or 3.12 due to sportsdataverse dependency.")
        print("Create a new venv with: python3.11 -m venv venv")
