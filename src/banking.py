import random
import string
from datetime import date

from bank_account import BankAccount
from customer import Customer
from exceptions import InsufficientFundsError
from logger import Logger


def find_customer(customers: list, user_id: int):
    return next((c for c in customers if c.user_id == user_id), None)


def find_account(customer: Customer, account_number: str):
    return next(
        (acc for acc in customer.accounts if acc.account_number == account_number), None
    )


def prompt_customer_id() -> int:
    return int(input("Customer Id: ").strip())


def generate_unique_account_number(customers: list) -> str:
    existing = {acc.account_number for c in customers for acc in c.accounts}
    while True:
        candidate = "".join(random.choices(string.digits, k=10))
        if candidate not in existing:
            return candidate


def menu(customers: list):
    logger = Logger().get_logger
    while True:
        print("""
                1. Add customer
                2. Add account to customer
                3. Deposit
                4. Withdraw
                5. Transfer
                6. View total balance
                0. Exit
                """)
        choice = input("Choose an option: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            try:
                name = input("Customer Name: ").strip()
                year = int(input("Enter the birth year: "))
                month = int(input("Enter the birth month: "))
                day = int(input("Enter the birth day: "))
                birth_date = date(year, month, day)
                c = Customer(name=name, birth_date=birth_date)
                customers.append(c)
                print(f"Customer created with id {c.user_id}")
            except ValueError as e:
                print(f"Could not create customer: {e}")
                logger.error(e)

        elif choice == "2":
            while True:
                print("""
                1. Savings Account
                2. Checking Account
                3. Return
                """)
                account_choice = input("Choose an option: ").strip()

                if account_choice == "3":
                    break
                elif account_choice in ("1", "2"):
                    try:
                        user_id = prompt_customer_id()
                    except ValueError:
                        print("Invalid Customer Id.")
                        continue

                    customer = find_customer(customers, user_id)
                    if not customer:
                        print(f"Customer not found: {user_id}")
                        continue

                    account_number = generate_unique_account_number(customers)
                    try:
                        if account_choice == "1":
                            acc = BankAccount.create_savings(
                                account_number=account_number
                            )
                        else:
                            acc = BankAccount(account_number=account_number)
                        customer.add_account(acc)
                        print(f"Account created: {acc.account_number}")
                    except (ValueError, InsufficientFundsError) as e:
                        print(f"Could not create account: {e}")
                        logger.error(e)
                else:
                    print("Invalid option")

        elif choice == "3":
            try:
                user_id = prompt_customer_id()
            except ValueError:
                print("Invalid Customer Id.")
                continue
            customer = find_customer(customers, user_id)
            if not customer:
                print(f"Customer not found: {user_id}")
                continue

            acc_number = input("Account Id: ").strip()
            account = find_account(customer, acc_number)
            if not account:
                print(f"Account not found: {acc_number}")
                continue

            try:
                amount = float(input("Deposit amount: ").strip())
                account.deposit(amount)
                print(f"New balance: {account.balance}")
            except ValueError as e:
                print(f"Deposit failed: {e}")
                logger.error(e)

        elif choice == "4":
            try:
                user_id = prompt_customer_id()
            except ValueError:
                print("Invalid Customer Id.")
                continue
            customer = find_customer(customers, user_id)
            if not customer:
                print(f"Customer not found: {user_id}")
                continue

            acc_number = input("Account Id: ").strip()
            account = find_account(customer, acc_number)
            if not account:
                print(f"Account not found: {acc_number}")
                continue

            try:
                amount = float(input("Withdraw amount: ").strip())
                account.withdraw(amount)
                print(f"New balance: {account.balance}")
            except (ValueError, InsufficientFundsError) as e:
                print(f"Withdraw failed: {e}")
                logger.error(e)

        elif choice == "5":
            try:
                user_id = prompt_customer_id()
            except ValueError:
                print("Invalid Customer Id.")
                continue
            customer = find_customer(customers, user_id)
            if not customer:
                print(f"Customer not found: {user_id}")
                continue

            src_acc_number = input("Source account Id: ").strip()
            src_acc = find_account(customer, src_acc_number)

            dst_acc_number = input("Destination account Id: ").strip()
            dst_acc = find_account(customer, dst_acc_number)

            if not src_acc or not dst_acc:
                print("Source or destination account not found.")
                continue

            try:
                amount = float(input("Transfer amount: ").strip())
                customer.transfer(src_acc, dst_acc, amount)
                print(
                    f"Transfer complete. Source balance: {src_acc.balance}, destination balance: {dst_acc.balance}"
                )
            except (ValueError, InsufficientFundsError) as e:
                print(f"Transfer failed: {e}")
                logger.error(e)

        elif choice == "6":
            try:
                user_id = prompt_customer_id()
            except ValueError:
                print("Invalid Customer Id.")
                continue
            customer = find_customer(customers, user_id)
            if customer:
                print(f"Total Balance: {customer.get_total_balance()}")
            else:
                print(f"{user_id} is not a valid Customer Id")

        else:
            print("Invalid option")


if __name__ == "__main__":
    customers = []
    menu(customers)
