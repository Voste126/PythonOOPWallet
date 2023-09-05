#PYTHONOOPWALLET
PROJECT TITLE: MY WALLET KENYA 

TABLE OF CONTENTS 
Project Title 
Table of Contents 
About the Project Features 
Demo 
Getting Started 
Prerequisites 
Installation 
Usage 
Contributing 
License 
Contact

ABOUT THE PROJECT 
This is a simple CLI end phase project that uses OOP concepts and SQLALchemy.
MY Wallet kenya is a CLI project that can be used in a large sale integration to its customer in the cyrptocurrencies and stock exchanges in general to watch for transaction and also investements in various markets. This idea can also be use by Data science and Data analysts to get insights on most popular markets once integrate and upgrade to serve such a purpose.

FEATURES 
Alembic- For version controls in terms of mananging migrations 
SQLAlchemy - FOr my database and also SQLALchemy Viewer as a Vscode extension
Modules that contains my tables 
Main.py that holds helper methods to enable the runnig of the program

DEMO
RUnning the commands under:
if __name__ == "__main__":
    print("Please use any command of choice and make user porfolio if you do not have one")
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

GETTING STARTED
Run the normal pipenv install and also check the requirements.txt to see other addtional libraries 
Also make sure to run pipenv shell before instalation of any other libraries needed

INSTALLATION 
pipenv install && pipenv shell


USAGE 
Learing purposes of object oriented programming and also data managment using SQLAlchemy

CONTRIBUTION 
This is a pahse code project  that is to enhance the OOP concepts using python in Moringa school. Its guided and graded by my Techinical mentor Joseph Wambua

LICENSE 
its a public repo that is used as a a portfolio project for end of phase 3

CONTACT Link and reach me on my linkedIn profile https://www.linkedin.com/in/steve-austine-84834823b/