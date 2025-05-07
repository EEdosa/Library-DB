# Library-DB

Run by going to code folder and follow these steps 

Step 1. Install Python

Step 2. Run the following commands to install dependencies:
    pip3 install PyQt5
    pip3 install tkinter
    pip3 install kivy

Step 3: Download Library.db or create Library.db from the LMS.sql file

Step 4. Run python program using 'python Library.py' to open GUI

Project 1: Railway Reservation System

Course: CSE 3330 – Databases

Semester: Spring 2025

#Part 1

This project involved designing and implementing a railway reservation system to manage train schedules, seat reservations, passenger information, and ticketing. Our team used MySQL to create a normalized database schema and wrote SQL scripts to populate the tables with sample data.

We implemented SQL queries to support core functionalities such as:

Searching for trains between stations

Booking and canceling tickets

Viewing available seats and reservation statuses

Managing passenger and train information

Additionally, we created a command-line interface using Python and MySQL connector to interact with the database. We also wrote views and stored procedures to simplify complex query logic and ensure data integrity. This project helped reinforce our understanding of ER modeling, relational schema design, and advanced SQL concepts such as joins, grouping, and nested queries.

#Part 2

This project focused on developing a full-fledged Library Management System with a Python Tkinter-based GUI and a SQLite backend. The goal was to implement core library operations including book management, borrower registration, book lending, and late fee tracking.

Key features of the system include:

Borrower Registration: Add new borrowers to the system with personal and contact information.

Book and Author Management: Add new books, authors, and associate them with library branches and copies.

Checkout and Return: Record book checkouts and returns, updating due dates and return statuses.

Loan Tracking: Monitor loan records, view all books currently checked out, and identify overdue items.

Late Fee Reporting: Calculate and display the total late fee for each borrower based on return dates.

We implemented SQL queries, views, and error-handling logic to ensure a robust and user-friendly application. The project emphasized practical database interaction, user interface design, and integration between the front-end and back-end systems.
