from enum import Enum


class BudgetGroup(Enum):
    """Budget groups, split 50/30/20 into needs, wants, and savings & debt."""

    # Needs (50%)
    HOUSING = "Housing"
    GROCERIES = "Groceries"
    UTILITIES = "Utilities"
    MINIMUM_DEBT_PAYMENTS = "Minimum debt payments"

    # Wants (30%)
    DINING_OUT = "Dining out"
    TRAVEL = "Travel"
    HOBBIES = "Hobbies"
    SUBSCRIPTIONS = "Subscriptions"

    # Savings & debt (20%)
    EMERGENCY_FUNDS = "Emergency funds"
    RETIREMENT = "Retirement"
    EXTRA_DEBT_PAYMENTS = "Extra debt payments"
