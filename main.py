# main.py
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

@click.command()
@click.option('--username', prompt=True, help='Enter a username')
@click.option('--email', prompt=True, help='Enter your email address')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Enter your password')
def create_user(username, email, password):
    db = SessionLocal()

    # Check if the username or email already exists in the database (you should implement this check)
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

    # Get the current time in the EAT timezone
    current_time_eat = datetime.now(eat_timezone)

    # Create a new User object and add it to the database with the EAT timestamp
    user = User(username=username, email=email, password=password, registration_date=current_time_eat)
    db.add(user)
    db.commit()
    db.close()

    print(f"User {username} registered successfully.")
# Portfolio Management Functions
@click.command("create-portfolio")
@click.option("--user_id", type=int, help="User ID of the owner of the portfolio")
@click.option("--name", type=str, help="Name of the portfolio")
def create_portfolio(user_id, name):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        db.close()  # Close the session if the user is not found
        click.echo(f"User with ID {user_id} does not exist.")
        return

    try:
        new_portfolio = Portfolio(name=name, owner=user)
        db.add(new_portfolio)
        db.commit()
        click.echo(f"Portfolio '{name}' created successfully for user '{user.username}'.")
    except Exception as e:
        db.rollback()  # Rollback the transaction in case of an error
        raise
    finally:
        db.close()  

@click.command()
@click.argument('portfolio_id', type=int)
@click.argument('new_name')
def update_portfolio_name(portfolio_id, new_name):
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

@click.command()
@click.argument('portfolio_id', type=int)
def delete_portfolio(portfolio_id):
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
@click.argument('portfolio_id', type=int)
@click.argument('transaction_type')
@click.argument('amount', type=float)
def create_transaction(portfolio_id, transaction_type, amount):
    db = SessionLocal()
    transaction = Transaction(portfolio_id=portfolio_id, transaction_type=transaction_type, amount=amount)
    db.add(transaction)
    db.commit()
    db.close()
    print("Transaction created successfully.")

@click.command("update-transaction")
@click.argument('transaction_id', type=int)
@click.argument('new_amount', type=float)
def update_transaction(transaction_id, new_amount):
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
@click.argument('transaction_id', type=int)
def delete_transaction(transaction_id):
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

@click.command("show-user-portfolios")
@click.argument('user_id', type=int)
def show_user_portfolios(user_id):
    portfolios = get_user_portfolios(user_id)
    if portfolios:
        for portfolio in portfolios:
            print(f"Portfolio ID: {portfolio.id}, Name: {portfolio.name}")
    else:
        print("User not found or has no portfolios.")


@click.command("show-user-transactions")
@click.argument('user_id', type=int)
def show_user_transactions(user_id):
    transactions = get_user_transactions(user_id)
    if transactions:
        for transaction in transactions:
            print(f"Transaction ID: {transaction.id}, Type: {transaction.transaction_type}, Amount: {transaction.amount}")
    else:
        print("User not found or has no transactions.")



if __name__ == "__main__":
    print("WELCOME TO MY WALLET KENYA: TYPE COMMAND OF CHOICE!!")
#python main.py create-user
    main.add_command(create_user)
#python main.py create-portfolio --user_id 1 --name "Tech Stocks"
    main.add_command(create_portfolio)
#python main.py update-portfolio-name <portfolio_id> <new_name>
    main.add_command(update_portfolio_name)
#python main.py delete-portfolio <portfolio_id>
    main.add_command(delete_portfolio)
#python main.py create-transaction <portfolio_id> <amount>
    main.add_command(create_transaction)
#python main.py update-transaction <Transaction_id> <new amount>
    main.add_command(update_transaction)
#python main.py delete-transaction <Transaction_id>
    main.add_command(delete_transaction)
#python main.py show-user-portfolios <User_id>
    main.add_command(show_user_portfolios)
#python main.py show-user-transactions <User_id>
    main.add_command(show_user_transactions)

    main()
