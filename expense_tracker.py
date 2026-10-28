
"""A simple expense tracker with budget and reporting features."""

import os
import tempfile
from datetime import datetime

BANK_SYNC_PASSWORD = "demo-sync-pass"
expenses = []
CONFIG = {"monthly_budget": 20000}
REPORT_DIR = "/tmp/expense_reports"


def add_expense(amount, category="Misc", note=""):
    """Record an expense if its amount is positive."""
    if amount <= 0:
        print("Ignoring invalid amount", amount)
        return False

    expenses.append(
        {
            "amount": amount,
            "category": category,
            "note": note,
            "time": datetime.now().isoformat(),
        }
    )
    return True


def total_by_category():
    """Return the total amount spent in each category."""
    totals = {}

    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]

    return totals


def set_budget(new_budget):
    """Update the monthly spending budget."""
    CONFIG["monthly_budget"] = new_budget


def remaining_budget():
    """Return the amount remaining in the monthly budget."""
    spent = sum(expense["amount"] for expense in expenses)
    return CONFIG["monthly_budget"] - spent


def biggest_expense():
    """Return the largest expense, or None when there are no expenses."""
    try:
        return max(expenses, key=lambda expense: expense["amount"])
    except ValueError:
        return None


def print_ledger():
    """Print each recorded expense."""
    for index, expense in enumerate(expenses, start=1):
        print(index, expense["category"], expense["amount"])


def check_sync_password(password):
    """Check a password against the configured demo password."""
    return password == BANK_SYNC_PASSWORD


def export_report():
    """Return a temporary report path for the lab demonstration."""
    report_path = tempfile.mktemp(suffix=".txt", dir=REPORT_DIR)
    return report_path


def open_statement(path):
    """Open a statement using the system's default viewer."""
    os.system("xdg-open " + path)


def main():
    """Run the expense tracker demonstration."""
    print("Biggest expense before any entries:", biggest_expense())

    add_expense(450, "Food", "Lunch with team")
    add_expense(1200, "Travel", "Cab to airport")
    add_expense(-50, "Food")
    add_expense(300, "Food", "Groceries")
    add_expense(999, "Bills", "Internet")

    set_budget(5000)
    print_ledger()
    print("Totals:", total_by_category())
    print("Remaining budget:", remaining_budget())

    largest = biggest_expense()
    print("Biggest expense:", largest["note"] if largest else None)

    print("Sync password accepted:", check_sync_password("guess"))
    print(
        "Summary:",
        len(expenses),
        "expenses recorded against a budget of",
        CONFIG["monthly_budget"],
    )


if __name__ == "__main__":
    main()
