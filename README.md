# Personal Finance Manager — Design Patterns Project

This project is a hands-on exercise in applying Object-Oriented Design Patterns to build a simplified personal finance manager.
You will implement and extend starter code to add functionality such as tracking transactions, adapting external data, observing balance changes, and ensuring proper architectural patterns.

## Getting Started

### Dependencies
Python 3.15.2

### Installation

1. Clone the repo:

```
bash
git clone https://github.com/udacity/cd14600-project-starter.git
cd cd14600-project-starter/starter
```

2. Run the Program (from the `starter` folder):
```
python main.py
```

## Testing

This project uses Python's built-in unittest framework.

Run the tests from the `starter` folder.

To run all tests:

```
python -m unittest discover -v
```

To run a single test file:
```
python -m unittest balance.test_balance_observer
```

To run a single test:
```
python -m unittest balance.test_balance.TestBalance.test_summary
```

### Break Down Tests

- balance/test_balance.py → Verifies the Singleton Balance class (accessor and direct construction return one object that keeps its state), plus applying and summarising transactions.
- balance/test_balance_observer.py → Validates low-balance alerts (including exactly at the threshold, and when the alert and recovery callbacks fire) and the printed output of the print observer.
- pattern/test_singleton.py → Verifies the Singleton base class and metaclass.
- test_main.py → Runs the demo and checks the balance is printed after every transaction, the warning appears when the balance dips below 50, and recovery is announced later.
- balance/test_balance_ledger_observer.py → Checks that processed and reversed transactions are recorded in the Ledger.
- transaction/test_transaction.py → Covers creating, printing and comparing transactions.
- transaction/test_transaction_adapter.py → Ensures external income data is correctly adapted into Transaction objects.
- transaction/test_transaction_processor.py → Checks the invoker runs commands in order and can undo the last one.
- transaction/test_budget_group.py → Checks the budget group enum, the Transaction budget group field, and fictitious spending in every group.
- command/test_commands.py → Verifies Apply, Unapply and Import, including undo.
- ledger/test_ledger.py → Verifies the Singleton Ledger.
- budget/test_budget_processor.py → Checks budget groups are applied to ledger transactions and totalled.
- budget/test_budget_planner.py → Verifies the 50/30/20 and zero-based strategies and swapping them in the planner.

## Project Structure

```
starter/
  main.py                  Entry point: processes transactions and prints budgets
  pattern/                 Reusable pattern building blocks (Singleton, Observer)
  transaction/             Transaction, categories, budget groups, adapter, processor
  balance/                 Balance singleton and its observers
  command/                 Command pattern: Command, Apply, Unapply, Import
  ledger/                  Ledger singleton that stores processed transactions
  budget/                  Budget processor, planner and budget strategies
```

## Design Patterns Used

| Pattern | Where | Role |
| --- | --- | --- |
| Singleton | `Balance`, `Ledger` (via `SingletonMeta` in `pattern/singleton.py`) | One shared balance and one shared ledger, even when the class is constructed directly |
| Adapter | `TransactionAdapter` | Converts `ExternalFreelanceIncome` into a `Transaction` |
| Observer | `Balance` notifies `PrintObserver`, `LowBalanceAlertObserver`, `BalanceLedgerObserver` | React to balance changes |
| Command | `Apply`, `Unapply`, `Import` extend `Command`; `TransactionProcessor` is the invoker; `Balance` is the receiver | Run and undo transactions |
| Strategy | `BudgetPlanner` with `FiftyThirtyTwentyStrategy` and `ZeroBasedStrategy` | Interchangeable ways to build a budget |

### How it fits together

1. `TransactionProcessor` executes `Apply`, `Unapply` and `Import` commands against `Balance`.
2. `Balance` updates the net balance and notifies its observers. `BalanceLedgerObserver` stores each transaction in the `Ledger`, flagging reversals from `Unapply` or undo.
3. `BudgetProcessor` reads the `Ledger`, assigns a `BudgetGroup` to each expense by matching keywords in its detail, and totals income and spending.
4. `BudgetPlanner` uses a strategy to print a budget from those totals:
   - **50/30/20** splits income into 50% needs (housing, groceries, utilities, minimum debt payments), 30% wants (dining out, travel, hobbies, subscriptions) and 20% savings and debt (emergency funds, retirement, extra debt payments).
   - **Zero-based** allocates every dollar of income across the specific budget groups until nothing is left unallocated.

## Project Instructions

1. Implement Singleton Balance Class – Ensure only one balance object exists throughout the app.
2. Complete Transaction Class – Handle income and expense transactions.
3. Implement Adapter Pattern – Adapt external freelance income data into internal Transaction objects.
4. Implement Observer Pattern – Create a low balance observer that triggers an alert when funds drop too low.
5. Add Unit Tests – Write tests for all implemented functionality.
6. Choose and Implement a Fourth Pattern – Pick one additional design pattern (e.g., Strategy, Command, Decorator, etc.) and integrate it into your project.
7. Provide a Reflection – Add a short write-up in your repo (README or separate file) explaining your design choices.

## Reflection

- **Command for transactions:** Wrapping apply, unapply and import as commands lets the processor undo work and keeps `main.py` free of balance logic.
- **Observer for the ledger:** The balance does not know about the ledger. The ledger observer records transactions, so reporting can be added without changing `Balance`.
- **Reversal flag:** Observers are told when a transaction is reversed, so the ledger records a reversal and does not look like a duplicate transaction.
- **Strategy for budgets:** New budgeting methods can be added as new strategies without changing `BudgetPlanner`.
- **Keyword classification:** Budget groups are assigned by matching keywords in the transaction detail. This is simple, but unmatched or oddly worded transactions end up as uncategorised. Setting `budget_group` explicitly always takes priority.
- **Known limitations:** Amounts are floats, not `Decimal`. `Unapply` does not check that a transaction was applied first. There is no redo.

### GoF design patterns used

Singleton, Adapter, Observer, Command and Strategy.

### How each improved the design

- **Singleton:** `Balance` and `Ledger` each have one shared instance, so every part of the program sees the same balance and the same record of transactions. A metaclass enforces this, so `Balance()` and `Balance.get_instance()` return the same object and `__init__` never runs twice to reset state.
- **Adapter:** `TransactionAdapter` keeps the external freelance format out of the core code. `Balance` only ever handles `Transaction` objects.
- **Observer:** `Balance` does not know who is listening. Printing, low-balance alerts and ledger recording are separate observers that can be added or removed without changing `Balance`.
- **Command:** Apply, unapply and import are objects with `execute()` and `undo()`. The processor can run them, keep a history and undo the last one, and `main.py` no longer contains balance logic.
- **Strategy:** The 50/30/20 and zero-based budgets share one interface, so `BudgetPlanner` can switch between them and a new method is a new class, not an edit to existing code.

### Trade-offs encountered

- **Circular imports:** Observers need `Balance` for type hints, and `Balance` needs the observer base class. I moved the base class to `pattern/observer.py` and imported `Balance` only under `TYPE_CHECKING`.
- **Singleton and tests:** A shared instance keeps state between tests, so tests reset the `Balance` and `Ledger` first. It also made observers pile up on `Balance`, which the tests clear with `clear_observers()`.
- **Reversals:** Unapply and undo notify observers too. Passing a `reversal` flag stopped the ledger from recording a duplicate, but it changed the observer `update` signature for every observer.
- **More classes:** Command and Strategy add several small files and some indirection for a small program. In return each class has one job and is easy to test.
- **Simple budget rules:** Keyword matching and fixed default percentages are easy to follow and change, but they are less accurate than explicit budget groups or user-set amounts.

## Built With

* [Python](https://www.python.org/) – Main programming language
* [unittest](https://docs.python.org/3/library/unittest.html) – Testing framework
* [PEP8](https://peps.python.org/pep-0008/) – Style guide for Python code

## License

[License](LICENSE.txt)
