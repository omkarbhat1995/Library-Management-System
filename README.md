# 📚 Library Management System
A fully functional SQL-based backend system to support library operations using structured data and SQL queries. This project features a Python-based Streamlit frontend connected to a MySQL database to help librarians manage books, users, and transactions efficiently.

## ✨ Features
Book Management: Add new books to the inventory and view current available copies.

Member Management: Register new members with active/inactive status tracking.


Issue & Return Processing: Secure transaction handling that updates book_issues and inventory simultaneously, with automatic rollback protection if an error occurs.

Library Analytics & Reports:

Track which member has borrowed which book.

Identify overdue books automatically.

View the top 5 most borrowed books via interactive charts.

## 🛠️ Tech Stack
- Frontend: Streamlit (Python)

- Backend: Python

- Database: MySQL

- Libraries: streamlit, mysql-connector-python, pandas, python-dotenv

## 📂 Project Structure
This project separates the backend database logic from the frontend user interface, making the codebase much cleaner and easier to maintain.
```
library-management-system/
│
├── app.py                  # Main Streamlit UI application
├── .env                    # Environment variables (Credentials)
└── db/
    └── connect_mysql.py    # MySQL database connection and transaction logic
    └── db_table_creations  # MySQL database creation file with table creation and data entry

```

## 🚀 Installation & Setup
1. Prerequisites
Python 3.8+ installed on your machine.

MySQL Server installed and running locally.

2. Install Dependencies
Open your terminal, navigate to the project folder, and install the required Python packages:
```bash
pip install streamlit mysql-connector-python pandas python-dotenv
```

3. Database Setup
You need to create the database and the tables in MySQL based on the schema requirements. Run the provided SQL setup script in your MySQL environment (e.g., MySQL Workbench or the MySQL command line)  to create the library_db database, the books, members, and book_issues tables, and insert the initial sample data.

4. Configure Environment Variables
Your .env file must be placed in the root directory of your project (alongside app.py, not inside the db folder). Create a file named exactly .env and add your local MySQL credentials:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_actual_password
DB_NAME=library_db
```

## 💻 How to Run the Application
When you run the application, you must navigate to the exact folder in your terminal where app.py is located. Run the following command:
```bash
streamlit run app.py
```
A browser window will open automatically pointing to http://localhost:8501, where you can interact with your new SQL-backed Python application.