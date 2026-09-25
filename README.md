# Banking Lab

A small OOP banking system (`BankAccount`, `Customer`) with logging, a custom
exception type, and a pytest test suite.

## Project layout

```
.
├── pyproject.toml
├── src/
│   ├── bank_account.py
│   ├── customer.py
│   ├── exceptions.py
│   ├── logger.py
│   └── banking.py      # interactive menu / entry point
└── test/
    ├── conftest.py
    ├── test_bank_account.py
    ├── test_customer.py
    ├── test_exceptions.py
    └── test_logger.py
```

## Requirements

- [uv](https://docs.astral.sh/uv/) — no manual virtualenv or `pip install` needed,
  `uv run` resolves and installs dependencies automatically.

## Running the tests

```bash
uv run pytest
```

With a coverage report:

```bash
uv run pytest --cov=src --cov-report=term-missing
```

## Running the app

```bash
uv run src/banking.py
```

Launches the interactive menu: add customers, open accounts, deposit,
withdraw, transfer, and check balances.

## Configuration

Logging is controlled via environment variables (see `src/logger.py`), which
can also be set in a `.env` file at the project root:

| Variable    | Default        | Purpose                          |
|-------------|----------------|-----------------------------------|
| `LOG_LEVEL` | `INFO`         | Minimum log level shown/written  |
| `LOG_FILE`  | `banking.log`  | Log file path                    |