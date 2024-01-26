import csv
import datetime

def write_accounts(accounts):
    with open('accounts.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for account in accounts:
            writer.writerow([account[0], account[1], float(account[2])])  # Convert balance to float before writing

def read_accounts():
    try:
        with open('accounts.csv', 'r') as file:
            reader = csv.reader(file)
            return [row for row in reader]
    except FileNotFoundError:
        return []



def read_transactions():
    try:
        with open('transactions.csv', 'r') as file:
            reader = csv.reader(file)
            return [row for row in reader]
    except FileNotFoundError:
        return []

def write_transaction(transaction):
    with open('transactions.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(transaction)

def print_accounts(accounts):
    for account in accounts:
        print(f"Account: {account[0]}, Type: {account[1]}, Balance: {account[2]}")

def is_valid_transaction(debit_account, credit_account, amount, accounts):
    if amount <= 0:
        raise ValueError("Amount should be larger than zero.")

    debit_type = next((acc[1] for acc in accounts if acc[0] == debit_account), None)
    credit_type = next((acc[1] for acc in accounts if acc[0] == credit_account), None)

    if debit_type == credit_type:
        raise ValueError("A transaction cannot happen between two accounts of the same type.")

    debit_balance = next((float(acc[2]) for acc in accounts if acc[0] == debit_account), None)
    credit_balance = next((float(acc[2]) for acc in accounts if acc[0] == credit_account), None)

    if debit_balance is None or credit_balance is None:
        raise ValueError("Accounts must exist and have balances.")


    return True

def update_balances(accounts, debit_account, credit_account, amount):
    for account in accounts:
        if account[0] == debit_account:
            account[2] = str(float(account[2]) + amount)
        elif account[0] == credit_account:
            account[2] = str(float(account[2]) - amount)

    

def print_balance_sheet(accounts):
    total_assets = 0
    total_liabilities = 0
    total_equity = 0
    total_expenses = 0
    total_income = 0

    for account in accounts:
        if account[1] == 'assets':
            total_assets += float(account[2])
        elif account[1] == 'liabilities':
            total_liabilities += float(account[2])
        elif account[1] == 'equity':
            total_equity += float(account[2])
        elif account[1] == 'expenses':
            total_expenses += float(account[2])
        elif account[1] == 'income':
            total_income += float(account[2])
    
    total_equity = total_equity - total_expenses + total_income

    print(f"Total Assets: {total_assets}")
    print(f"Total Liabilities: {total_liabilities}")
    print(f"Total Equity: {total_equity}")

    check = total_assets - total_liabilities - total_equity
    
    print(f"Check value: {check}")

    if check == 0.0:
        print("Accounts are correctly balanced.")
    else:
        print("Warning: Accounts are not balanced. Check your entries.")

def main():
    accounts = read_accounts()
    transactions = read_transactions()

    if not accounts:
        print("No accounts found. Please provide initial account information.")
        while True:
            try:
                account_name = input("Enter account name: ")
                account_type = input("Enter account type (assets, liabilities, expenses, income, equity): ")
                initial_balance = float(input("Enter initial balance: "))
                accounts.append([account_name, account_type, initial_balance])
                break
            except ValueError:
                print("Invalid input. Please enter a valid numeric value for the initial balance.")

        write_accounts(accounts)

    while True:
        print("\nOptions:")
        print("1. Insert new account")
        print("2. Enter new transaction")
        print("3. Print account balances")
        print("4. Print balance sheet")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            try:
                account_name = input("Enter account name: ")
                account_type = input("Enter account type (assets, liabilities, expenses, income, equity): ")
                initial_balance = float(input("Enter initial balance: "))
                accounts.append([account_name, account_type, initial_balance])
                write_accounts(accounts)
                print(f"Account '{account_name}' added successfully.")
            except ValueError:
                print("Invalid input. Please enter a valid numeric value for the initial balance.")

        elif choice == '2':
            try:
                date = datetime.datetime.now().strftime("%Y-%m-%d")
                debit_account = input("Enter debit account: ")
                credit_account = input("Enter credit account: ")
                amount = float(input("Enter amount: "))
                description = input("Enter description: ")

                if is_valid_transaction(debit_account, credit_account, amount, accounts):
                    update_balances(accounts, debit_account, credit_account, amount)
                    write_accounts(accounts)
                    transaction = [date, debit_account, credit_account, amount, description]
                    write_transaction(transaction)
                    print("Transaction recorded successfully.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '3':
            print("Updated accounts and balances:")
            print_accounts(accounts)

        elif choice == '4':
            print("\nBalance Sheet:")
            print_balance_sheet(accounts)

        elif choice == '5':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()