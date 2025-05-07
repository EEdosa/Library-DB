from tkinter import *
import sqlite3

result_frame = None   
 
#define submit function - Trigger implemented in db
# 1.
def checkout_book():
    global result_frame
    submit_conn = sqlite3.connect('Library.db')
    submit_cur = submit_conn.cursor()
 
    submit_cur.execute("""
        INSERT INTO Book_Loans VALUES(:Book_Id, :Branch_Id, :Card_No, :Date_Out, :Due_Date, :Returned_date, :Late)
    """, {
        'Book_Id' : int(book_Id.get()),          
        'Branch_Id' : int(branch_Id.get()),    
        'Card_No' : int(card_number.get()),    
        'Date_Out' : date_out.get(),
        'Due_Date' : due_date.get(),
        'Returned_date': None,          
        'Late': None,
    })
    submit_cur.execute("""
        SELECT * FROM Book_Copies
        WHERE Book_Id = ? AND Branch_Id = ?
    """, (
        book_Id.get(),
        branch_Id.get()
    ))
 
    records = submit_cur.fetchall()
    print(records)
 
    print_records = ''
    for record in records:
        print_records += f"Book ID: {record[0]}, Branch ID: {record[1]}, Copies Left: {record[2]}\n"

    if result_frame is not None:
        result_frame.destroy()
    
    result_frame = LabelFrame(root, text="Book Checkout Report", padx=10, pady=10)
    result_frame.grid(row=30, column=1, columnspan=3, padx=20, pady=20)
 
    # Display in GUI
    book_copies = Label(result_frame, text= print_records)
    book_copies.grid(row=30, column=1, columnspan=2)
 
    submit_conn.commit()
    submit_conn.close()
 
 
# 2.
# NOTE - NEED AUTOINCREMENT IN TABLE TO WORK, also idk if the print works
def add_new_BORROWER():
    global result_frame
    submit_conn = sqlite3.connect('Library.db')
    iq_conn = sqlite3.connect('Library.db')
    iq_cur = iq_conn.cursor()
    submit_cur = submit_conn.cursor()
    #  2.  ADD NEW BORROWER WITH AUTO GENERATE
    submit_cur.execute("INSERT INTO BORROWER(Name, Address, Phone) VALUES(:name, :address, :phone) ",
                      {
                          #'card_number': card_number.get(),
                          'name': name.get(),
                          'address': address.get(),
                          'phone': phone.get(),
                      })
    submit_cur.execute("SELECT Card_No FROM BORROWER WHERE Name = ? AND Address = ? AND Phone = ?",(name.get(), address.get(), phone.get(),))
    records = submit_cur.fetchall()
    print(records)
 
    print_records = ''
    for record in records:
       print_records += str(record[0]) + "\n"

    if result_frame is not None:
        result_frame.destroy()
    
    result_frame = LabelFrame(root, text="New Borrower ID", padx=10, pady=10)
    result_frame.grid(row=30, column=1, columnspan=3, padx=20, pady=20)

 
    an_label = Label(result_frame, text = print_records)
    an_label.grid(row = 30, column = 1, columnspan = 2)
   
    submit_conn.commit()
    submit_conn.close()
 
# 3.
 
def add_book():
    submit_conn = sqlite3.connect('Library.db')
    submit_cur = submit_conn.cursor()
 
    submit_cur.execute("INSERT INTO Book(Title, Publisher_Name) VALUES(:Title, :Publisher_Name) ",
                {
                    #'Book_Id': book_Id.get(),
                    'Title' : booktitle.get(),
                    'Publisher_Name' :publisher.get(),
                })
    
    new_book_id = submit_cur.lastrowid
   
    submit_cur.execute("INSERT INTO Book_Authors(Author_Name) VALUES(:Author_Name)",
                {
                    #'Book_Id' : book_Id.get(),
                    'Author_Name' : author.get(),                
                })
 
    # Add to all 5 branches with 5 copies
    for branch_id in range(1, 6):
        submit_cur.execute("INSERT INTO Book_Copies VALUES(:Book_Id, :Branch_Id, :No_Of_Copies)",
                    {
                        'Book_Id': new_book_id,
                        'Branch_Id': branch_id,
                        'No_Of_Copies': 5,
                    })
 
    submit_conn.commit()
    submit_conn.close()
 
 
# 4.  queries
def copies_loaned():
    global result_frame
    iq_conn = sqlite3.connect('Library.db')
    iq_cur = iq_conn.cursor()
 
    iq_cur.execute("""
        SELECT B.Branch_Id, COUNT(*) AS Copies_Loaned
        FROM Book_Loans BL
        JOIN Book Bk ON BL.Book_Id = Bk.Book_Id
        JOIN Library_Branch B ON BL.Branch_Id = B.Branch_Id
        WHERE Bk.Title = ?
        GROUP BY B.Branch_Id
    """, (booktitle.get(),))
    records = iq_cur.fetchall()
    print(records)
    print_records = ''
    for record in records:
        print_records += f"Branch ID {record[0]}: {record[1]} copies loaned out\n"
    
    if result_frame is not None:
        result_frame.destroy()
    
    result_frame = LabelFrame(root, text="Copies Loaned Report", padx=10, pady=10)
    result_frame.grid(row=30, column=1, columnspan=3, padx=20, pady=20)

 
    iq_label = Label(result_frame, text = print_records)
    iq_label.grid(row = 30, column = 1, columnspan = 2)
 
    iq_conn.close()

#5. 
def days_late():
    global result_frame
    dl_conn = sqlite3.connect('Library.db')
    dl_cur = dl_conn.cursor()

    dl_cur.execute("""
        SELECT 
        Book_Id,
        Card_No,
        Branch_Id,
        Due_Date,
        Returned_date,
        julianday(Returned_date) - julianday(Due_Date) AS Days_Late
        FROM BOOK_LOANS 
        WHERE Late = 1 AND Due_Date BETWEEN ? AND ? AND Returned_Date IS NOT NULL
    """, (due_date_start.get(), due_date_end.get()))
    records = dl_cur.fetchall()
    print(records)
    print_records = ''
    
    for record in records:
        print_records += f"Book ID: {record[0]}, Branch ID: {record[1]}, Card #: {record[2]}, {record[5]} days late\n"
    
    if result_frame is not None:
        result_frame.destroy()
    
    result_frame = LabelFrame(root, text="Late Books Report", padx=10, pady=10)
    result_frame.grid(row=30, column=1, columnspan=3, padx=20, pady=20)


    dl_label = Label(result_frame, text = print_records)
    dl_label.grid(row = 30, column=1, columnspan = 2)


    dl_conn.close()

#6a.
def view_results():
    global result_frame

    view_conn = sqlite3.connect('Library.db')
    view_cur = view_conn.cursor()

    query = """
        SELECT
        Card_No,
        Borrower_Name,
        printf('$%.2f', LateFeeBalance)
        FROM vBookLoanInfo
                     """
    params = []

    if card_number.get():
        query += " WHERE Card_No = ?"
        params.append(card_number.get())
    if name.get():
        query += " WHERE Borrower_Name LIKE ?"
        params.append(f"%{name.get()}%")

    view_cur.execute(query, params)

    records = view_cur.fetchall()
    print(records)
    print_records = ''

    for record in records:
        print_records += f"Card #: {record[0]}, Name: {record[1]}, LateFeeBalance: {record[2]}\n"
    
    if result_frame is not None:
        result_frame.destroy()
    
    result_frame = LabelFrame(root, text="Late Fee Report", padx=10, pady=10)
    result_frame.grid(row=30, column=1, columnspan=3, padx=20, pady=20)


    view_label = Label(result_frame, text = print_records)
    view_label.grid(row = 30, column=1, columnspan = 2)

    view_conn.close()

 #6b.
def view_bookinfo():
    global result_frame

 
    conn = sqlite3.connect("Library.db")
    c = conn.cursor()
 
    query = """
    SELECT
        V.Card_No AS "Borrower ID",
        V.Borrower_Name AS "Borrower Name",
        V.Book_Title AS "Book Title",
        V.Branch_Id AS "Branch ID",
        V.Date_Out AS "Date Out",
        V.Due_Date AS "Due Date",
        V.Returned_date AS "Date Returned",
        V.TotalDays AS "Total Days",
        V.Days_Late AS "Days Late",
        CASE
            WHEN V.LateFeeBalance = 0 THEN 'Non-Applicable'
            ELSE printf('$%.2f', V.LateFeeBalance)
        END AS "Late Fee"
    FROM vBookLoanInfo V, BOOK_LOANS BL, BOOK B
    WHERE BL.Book_Id = B.Book_Id AND BL.Card_No = V.Card_No
    """
    params = []

    if card_number.get():
        query += " AND BL.Card_No = ?"
        params.append(card_number.get())
 
    if book_Id.get():
        query += " AND BL.Book_Id = ?"
        params.append(book_Id.get())
    if booktitle.get():
        query += " AND B.Title LIKE ?"
        params.append(f"%{booktitle.get()}%")

    query += " ORDER BY V.LateFeeBalance DESC"
    
    c.execute(query, params)
    records = c.fetchall()
    print(records)
 
    display_text = ""
    for record in records:
        display_text += f"Borrower ID: {record[0]}, Borrower Name: {record[1]}, Book Title: {record[2]}, Book ID: {record[3]},Date Out: {record[4]}, Due Date: {record[5]}, Returned: {record[6]}, Total Days: {record[7]}, Days Late: {record[8]}, LateFeeBalance: {record[9]}\n"
    
    if result_frame is not None:
        result_frame.destroy()
    result_frame = LabelFrame(root, text="Book Information", padx=10, pady=10)
    result_frame.grid(row=30, column=1, columnspan=3, padx=20, pady=20)
    result_label = Label(result_frame, text=display_text)
    result_label.grid(row=30, column=0, columnspan=2)

    conn.close()
 
root = Tk()
root.title('Library Database')
 
root.geometry("600x600")
 
#connect to db
 
conn = sqlite3.connect('Library.db')
 
#create cursor
library_cur = conn.cursor()
 
#GUI components
#Define them in grid
 
#define all the text boxes
 
card_number = Entry(root, width = 30)
card_number.grid(row = 0, column = 1, padx = 20 )
 
name = Entry(root, width = 30)
name.grid(row = 1, column = 1)
 
address = Entry(root, width = 30)
address.grid(row = 2, column = 1)
 
phone = Entry(root, width = 30)
phone.grid(row = 3, column = 1)
 
book_Id = Entry(root, width = 30)
book_Id.grid(row = 4, column = 1)
 
booktitle = Entry(root, width = 30)
booktitle.grid(row = 5, column = 1)
 
branch_Id = Entry(root, width = 30)
branch_Id.grid(row = 6, column = 1)
 
date_out = Entry(root, width = 30)
date_out.grid(row = 7, column = 1)

due_date = Entry(root, width = 30)
due_date.grid(row = 8, column = 1)

due_date_start = Entry(root, width = 30)
due_date_start.grid(row = 9, column = 1)

due_date_end = Entry(root, width = 30)
due_date_end.grid(row = 10, column = 1)
 
publisher = Entry(root, width = 30)
publisher.grid(row = 11, column = 1)
 
author = Entry(root, width = 30)
author.grid(row = 12, column = 1)
 
no_of_copies = Entry(root, width = 30)
no_of_copies.grid(row = 13, column = 1)

 
#define labels
 
card_number_label = Label(root, text = 'Card Number:' )
card_number_label.grid(row = 0, column = 0)
 
name_label = Label(root, text = ' Name:' )
name_label.grid(row = 1, column = 0)
 
address_label = Label(root, text = 'Address:' )
address_label.grid(row = 2, column = 0)
 
phone_label = Label(root, text = 'Phone:' )
phone_label.grid(row = 3, column = 0)
 
book_label = Label(root, text = 'BookID:' )
book_label.grid(row = 4, column = 0)
 
book_title_label = Label(root, text = 'Book Title:' )
book_title_label.grid(row = 5, column = 0)
 
branch_Id_label = Label(root, text = 'Branch_Id:' )
branch_Id_label.grid(row = 6, column = 0)
 
date_out_label = Label(root, text = 'Date Out:' )
date_out_label.grid(row = 7, column = 0)
 
due_date_label = Label(root, text = 'Due Date:' )
due_date_label.grid(row = 8, column = 0)

due_date_start_label = Label(root, text = 'Due Date Start:')
due_date_start_label.grid(row = 9, column = 0)

due_date_end_label = Label(root, text = 'Due Date End:')
due_date_end_label.grid(row = 10, column = 0)
 
publisher_label = Label(root, text = 'Publisher:' )
publisher_label.grid(row = 11, column = 0)
 
author_label = Label(root, text = 'Author:' )
author_label.grid(row = 12, column = 0)
 
no_of_copies_label = Label(root, text = '# of Copies:' )
no_of_copies_label.grid(row = 13, column = 0)
 
 
 
#excute an SQL commands
 
copies = Button(root, text = 'Find Branch Copies', command = copies_loaned)
copies.grid(row = 17, column = 0 )
 
submit_btn = Button(root, text = 'Add New Borrower', command = add_new_BORROWER)
submit_btn.grid(row = 15, column = 0 )
 
checkout = Button(root, text = 'Checkout Book', command = checkout_book)
checkout.grid(row = 14, column = 0 )
 
add_books = Button(root, text = 'Add Books', command = add_book)
add_books.grid(row = 16, column = 0 )

daysLate = Button(root, text = 'Days Late', command = days_late)
daysLate.grid(row = 18, column = 0)
 
viewResults = Button(root, text = 'Borrower Late Fees', command = view_results)
viewResults.grid(row=19, column = 0)

bookInfo = Button(root, text = 'Book Information', command = view_bookinfo)
bookInfo.grid(row=20, column=0)

root.mainloop() #keeps window open and running