

# Budget

Splits after-tax income into three broad buckets: 50% Needs (housing, groceries, utilities, minimum debt payments), 30% Wants (dining out, travel, hobbies, subscriptions), and 20% Savings & Debt (emergency funds, retirement, extra debt payments)

Starts with your monthly take-home pay (or lowest expected income if variable) and allocates every dollar across specific categories until nothing is left unassigned.


1. Refactor main.py and take move transaction handling to a seprate class called TransactionProcessor

2. Create commands Apply
These should extend the class Command and follow the GOF pattern for Command processing

Invoker
    TransactionProcessor

Receiver
    Balance

Commands
    Apply
    Unapply
    Import
