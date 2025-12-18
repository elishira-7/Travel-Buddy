from database import load_data
from utils import budget_friendly, safety_friendly, nightlife_friendly

df = load_data()

def get_user_input():

    # ===== NEW LINE 1 =====
    region_input = input("Regions (comma-separated, e.g., Europe,Asia): ").strip()

    # ===== NEW LINE 2 =====
    regions = [r.strip() for r in region_input.split(',') if r.strip()]

    max_budget = input("Max daily cost USD: ").strip()
    max_budget = float(max_budget) if max_budget else None

    nightlife = input("Nightlife? (yes/no): ").strip().lower()
    nightlife = nightlife if nightlife in ["yes", "no"] else None

    min_safety = input("Minimum safety index (0-100): ").strip()
    min_safety = float(min_safety) if min_safety else None

    # ===== NEW LINE 3 =====
    available_columns = ["Country", "Region", "LGBTQFriendly", "AvgDailyCostUSD", "SafetyIndex"]

    # ===== NEW LINE 4 =====
    print("Available columns to display:", available_columns)

    # ===== NEW LINE 5 =====
    cols_input = input("Enter columns to display (comma-separated, leave blank for defaults): ").strip()

    # ===== NEW LINE 6 =====
    if cols_input:
        selected_columns = [
            c.strip() for c in cols_input.split(",")
            if c.strip() in available_columns
        ]
    else:
        selected_columns = ["Country", "Region", "LGBTQFriendly"]

    return regions, max_budget, nightlife, min_safety, selected_columns


def apply_filters(df):

    regions, max_budget, nightlife, min_safety, selected_columns = get_user_input()
    filtered = df.copy()

    # ===== NEW LINE 7 =====
    if regions:
        filtered = filtered[
            filtered["Region"].str.lower().isin(
                [r.lower() for r in regions]
            )
        ]

    if max_budget is not None:
        filtered = budget_friendly(filtered, max_budget)

    if nightlife == "yes":
        filtered = nightlife_friendly(filtered)

    if min_safety is not None:
        filtered = safety_friendly(filtered, min_safety)

    # ===== NEW LINE 8 =====
    filtered = filtered[selected_columns]

    # ===== NEW LINE 9 =====
    print(filtered.head(10).to_string(index=False))


def main_menu():
    while True:
        print("\n1. Apply filters")
        print("2. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            apply_filters(df)
        elif choice == "2":
            break


if __name__ == "__main__":
    main_menu()
