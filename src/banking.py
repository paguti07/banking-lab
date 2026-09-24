from datetime import date
from customer import Customer
from logger import Logger
from bank_account import BankAccount
import random
import string

def menu(customers: list):
    logger = Logger().logger
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
                year = int(input('Enter the birth year: '))
                month = int(input('Enter the birth month: '))
                day = int(input('Enter the birth day: '))
                birth_date = date(year, month, day)
                c = Customer(name = name, birth_date=birth_date)
                customers.append(c)
            except ValueError as e:
                print("Invalid date. Please enter valid year, month, and day values.")
                logger.error(e)

        elif choice == "2":
            while True:
                print("""
                1. Savings Account
                2. Checking Account
                3. Return
                """)
                random_account = ''.join(random.choices(string.digits, k=10))
                account_choise = input("Choose an option: ").strip()
                if account_choise == "1":
                    user_id = input("Customer Id: ").strip()
                    if any(customer.user_id == user_id for customer in customers):
                        acc = BankAccount.create_savings(account_number=random_account)
                    else:
                        print(f'Customer not found {user_id}')
                elif account_choise == "2":
                    user_id = input("Customer Id: ").strip()
                    if any(customer.user_id == user_id for customer in customers):
                        acc = BankAccount(account_number=random_account)
                    else:
                        print(f'Customer not found {user_id}')
                elif account_choise == "3":
                    break
                else:
                    print("Invalid option")

        elif choice == "3":
            user_id = input("Customer Id: ").strip()
            customer = next((customer for customer in customers if customer.user_id == user_id), None)
            if customer:
                acc_number = input("Account Id: ").strip()
                account = next((acc for acc in customer.accounts if acc.account_number == acc_number),None)
                if account:
                    amount = input("Deposit amount: ").strip()
                    account.deposit(float(amount))

        elif choice == "4":
            user_id = input("Customer Id: ").strip()
            customer = next((customer for customer in customers if customer.user_id == user_id), None)
            if customer:
                acc_number = input("Account Id: ").strip()
                account = next((acc for acc in customer.accounts if acc.account_number == acc_number),None)
                if account:
                    amount = input("Deposit amount: ").strip()
                    account.withdraw(float(amount))

        elif choice == "5":
            user_id = input("Customer Id: ").strip()
            customer = next((customer for customer in customers if customer.user_id == user_id), None)
            if customer:
                src_acc_number = input("Source account Id: ").strip()
                src_acc = next((acc for acc in customer.accounts if acc.account_number == src_acc_number),None)

                dst_acc_number = input("Source account Id: ").strip()
                dst_acc = next((acc for acc in customer.accounts if acc.account_number == dst_acc_number),None)

                if src_acc and dst_acc:
                    amount = input("Transfer amount: ").strip()
                    src_acc.withdraw(float(amount))
                    dst_acc.deposit(float(amount))

        elif choice == "6":
            user_id = input("Customer Id: ").strip()
            customer = next((customer for customer in customers if customer.user_id == user_id), None)
            if customer:
                print(f'Total Balance: {customer.get_total_balance()}')
        else:
            print("Invalid option")


if __name__ == "__main__":
    customers = []
    menu(customers)
