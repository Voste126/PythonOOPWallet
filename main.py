# main.py
import os
import click
import pytz #for the east african timezone
from sqlalchemy.orm import Session
from modules.user import User
from modules.portfolio import Portfolio
from modules.transaction import Transaction
from modules.database import SessionLocal, engine, Base
from datetime import datetime

# Define the East African Time (EAT) timezone
eat_timezone = pytz.timezone('Africa/Nairobi')

Base.metadata.create_all(bind=engine)


#my query helper methods for main.py
# Function to retrieve all portfolios for a user
def get_user_portfolios(user_id):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        portfolios = user.portfolios
        db.close()
        return portfolios
    else:
        db.close()
        return None

# Function to retrieve all transactions for a user
def get_user_transactions(user_id):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        transactions = []
        for portfolio in user.portfolios:
            transactions.extend(portfolio.transactions)
        db.close()
        return transactions
    else:
        db.close()
        return None






@click.group()
def main():
    pass

# Function to create a user with prompts
def create_user_prompt():
    username = click.prompt('Enter a username')
    email = click.prompt('Enter your email address')
    password = click.prompt('Enter your password', hide_input=True, confirmation_prompt=True)
    
    db = SessionLocal()
    existing_user = db.query(User).filter(User.username == username).first()
    existing_email = db.query(User).filter(User.email == email).first()

    if existing_user:
        db.close()
        print(f"User {username} already exists.")
        return

    if existing_email:
        db.close()
        print(f"Email {email} is already registered.")
        return

    current_time_eat = datetime.now(eat_timezone)
    
    user = User(username=username, email=email, password=password, registration_date=current_time_eat)
    db.add(user)
    db.commit()
    db.close()

    print(f"User {username} registered successfully.")


# Portfolio Management Functions
# Function to create a portfolio with prompts
@click.command("create-portfolio")
def create_portfolio_prompt():
    user_id = click.prompt('Enter User ID', type=int)
    name = click.prompt('Enter Portfolio Name', type=str)
    
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        db.close()
        print(f"User with ID {user_id} does not exist.")
        return

    try:
        new_portfolio = Portfolio(name=name, owner=user)
        db.add(new_portfolio)
        db.commit()
        print(f"Portfolio '{name}' created successfully for user '{user.username}'.")
    except Exception as e:
        db.rollback()  # Rollback the transaction in case of an error
        raise
    finally:
        db.close()

@click.command("update-portfolio-name")
def update_portfolio_name_prompt():
    portfolio_id = click.prompt('Enter Portfolio ID', type=int)
    new_name = click.prompt('Enter New Portfolio Name', type=str)

    db = SessionLocal()
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if portfolio:
        portfolio.name = new_name
        db.commit()
        db.close()
        print(f"Portfolio name updated to '{new_name}' successfully.")
    else:
        db.close()
        print("Portfolio not found.")

@click.command("delete-portfolio")
def delete_portfolio_prompt():
    portfolio_id = click.prompt('Enter Portfolio ID', type=int)
    
    db = SessionLocal()
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if portfolio:
        db.delete(portfolio)
        db.commit()
        db.close()
        print(f"Portfolio deleted successfully.")
    else:
        db.close()
        print("Portfolio not found.")

# Transaction Management Functions
@click.command("create-transaction")
def create_transaction_prompt():
    portfolio_id = click.prompt('Enter Portfolio ID', type=int)
    transaction_type = click.prompt('Enter Transaction Type', type=str)
    amount = click.prompt('Enter Transaction Amount', type=float)

    db = SessionLocal()
    transaction = Transaction(portfolio_id=portfolio_id, transaction_type=transaction_type, amount=amount)
    db.add(transaction)
    db.commit()
    db.close()
    print("Transaction created successfully.")


@click.command("update-transaction")
def update_transaction_prompt():
    transaction_id = click.prompt('Enter Transaction ID', type=int)
    new_amount = click.prompt('Enter New Transaction Amount', type=float)

    db = SessionLocal()
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction:
        transaction.amount = new_amount
        db.commit()
        db.close()
        print("Transaction updated successfully.")
    else:
        db.close()
        print("Transaction not found.")

@click.command("delete-transaction")
def delete_transaction_prompt():
    transaction_id = click.prompt('Enter Transaction ID', type=int)
    
    db = SessionLocal()
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction:
        db.delete(transaction)
        db.commit()
        db.close()
        print("Transaction deleted successfully.")
    else:
        db.close()
        print("Transaction not found.")

# Function to show user portfolios with prompts
@click.command("show-user-portfolios")
def show_user_portfolios_prompt():
    user_id = click.prompt('Enter User ID', type=int)
    portfolios = get_user_portfolios(user_id)
    
    if portfolios:
        print("User Portfolios:")
        for portfolio in portfolios:
            print(f"Portfolio ID: {portfolio.id}, Name: {portfolio.name}")
    else:
        print("User not found or has no portfolios.")


@click.command("show-user-transactions")
def show_user_transactions_prompt():
    user_id = click.prompt('Enter User ID', type=int)
    transactions = get_user_transactions(user_id)
    if transactions:
        for transaction in transactions:
            print(f"Transaction ID: {transaction.id}, Type: {transaction.transaction_type}, Amount: {transaction.amount}")
    else:
        print("User not found or has no transactions.")

def exit_program():
    print("Exiting the program.")
    # You can add any additional cleanup or exit actions here if needed
    exit()

def display_menu():
        os.system('clear')
        print("----------------WELCOME TO MY WALLET KENYA: SELECT AN OPTION---------------------")
        print("1. Create User")
        print("2. Create Portfolio")
        print("3. Update Portfolio Name")
        print("4. Delete Portfolio")
        print("5. Create Transaction")
        print("6. Update Transaction")
        print("7. Delete Transaction")
        print("8. Show User Portfolios")
        print("9. Show User Transactions")
        print("0. Exit")

def handle_choice(choice):
            if choice == 1:
                create_user_prompt()
            elif choice == 2:
                create_portfolio_prompt()
            elif choice == 3:
                update_portfolio_name_prompt()
            elif choice == 4:
                delete_portfolio_prompt()
            elif choice == 5:
                create_transaction_prompt()
            elif choice == 6:
                update_transaction_prompt()
            elif choice == 7:
                delete_transaction_prompt()
            elif choice == 8:
                show_user_portfolios_prompt()
            elif choice == 9:
                show_user_transactions_prompt()
            elif choice == 0:
                exit_program()
            else:
                print("Invalid choice. Please select a valid option.")
                choice = int(input("Enter your choice (0-9): "))
       

            
            
if __name__ == "__main__":
    while True:
        display_menu()
        
        while True:
            choice = int(input("Enter your choice (0-9): "))
            handle_choice(choice)
                

        





