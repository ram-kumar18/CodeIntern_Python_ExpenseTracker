import csv
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = "expenses.csv"


def init_csv():
    """Create CSV file with header if it doesn't exist."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "category", "description", "amount"])


def add_expense():
    print("\n--- Add Expense ---")
    date_str = input("Enter date (YYYY-MM-DD) or leave blank for today: ").strip()
    if not date_str:
        date_str = datetime.today().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("❌ Invalid date format.")
            return

    category = input("Enter category (e.g., Food, Transport, Bills): ").strip()
    description = input("Enter description: ").strip()
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("❌ Invalid amount.")
        return

    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date_str, category, description, amount])

    print("✅ Expense added successfully!")


def load_data():
    if not os.path.exists(DATA_FILE):
        init_csv()
    return pd.read_csv(DATA_FILE, parse_dates=["date"])


def summary(period="D"):
    """Show summary by day (D), week (W), or month (M)."""
    df = load_data()
    if df.empty:
        print("No expenses to summarize.")
        return

    df.set_index("date", inplace=True)
    grouped = df["amount"].resample(period).sum()

    print("\n--- Summary ---")
    for index, value in grouped.items():
        if period == "D":
            label = index.strftime("%Y-%m-%d")
        elif period == "W":
            label = f"Week {index.strftime('%Y-%m-%d')}"
        else:  # month
            label = index.strftime("%Y-%m")
        print(f"{label}: ₹{value:.2f}")


def top_categories():
    df = load_data()
    if df.empty:
        print("No expenses to analyze.")
        return

    grouped = df.groupby("category")["amount"].sum().sort_values(ascending=False)

    print("\n--- Top Spending Categories ---")
    for cat, amt in grouped.items():
        print(f"{cat}: ₹{amt:.2f}")


def plot_expenses(kind="bar"):
    df = load_data()
    if df.empty:
        print("No expenses to plot.")
        return

    grouped = df.groupby("category")["amount"].sum().sort_values(ascending=False)

    print("\nOpening chart window...")
    if kind == "pie":
        grouped.plot(kind="pie", autopct="%1.1f%%")
        plt.title("Expenses by Category")
        plt.ylabel("")
    else:
        grouped.plot(kind="bar")
        plt.title("Expenses by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Amount")
    plt.tight_layout()
    plt.show()


def menu():
    init_csv()
    while True:
        print("\n===== Personal Expense Tracker =====")
        print("1. Add Expense")
        print("2. Daily Summary")
        print("3. Weekly Summary")
        print("4. Monthly Summary")
        print("5. Top Spending Categories")
        print("6. Show Bar Chart by Category")
        print("7. Show Pie Chart by Category")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            summary("D")
        elif choice == "3":
            summary("W")
        elif choice == "4":
            summary("M")
        elif choice == "5":
            top_categories()
        elif choice == "6":
            plot_expenses("bar")
        elif choice == "7":
            plot_expenses("pie")
        elif choice == "8":
            print("👋 Exiting Expense Tracker...")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    menu()
