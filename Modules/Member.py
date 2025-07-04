from Modules.Connection import Connection
from datetime import datetime
from Modules.User import User

class Member(User):

    def __init__(self):
        super().__init__()

    def get_id(self):
        if self.user_id is not None:
            return self.user_id
        else:
            print("User ID is not set.")
            return None

    def am_i_member(self):
        db = Connection()
        result = db.execute_query(
            "SELECT * FROM tblUser WHERE UserName = ?",
            (self._User__username,)
        )
        if result and result[0][5] == 0:
            return True
        else:
            return False

    def return_book(self, isbn: str):
        if self.am_i_member() is False:
            print("You are not authorized to return books.")
            return False

        db = Connection()
        book = db.execute_query(
            "SELECT BookID FROM tblBook WHERE BookISBN = ?",
            (isbn,)
        )
        if not book:
            print("Book not found.")
            return False
        book_id = book[0][0]

        loan = db.execute_query(
            """
            SELECT LoanID FROM tblLoans 
            WHERE BookID = ? AND UserID = ? AND ReturnDate IS NULL
            """,
            (book_id, self.user_id)
        )
        if not loan:
            print("You do not have this book on loan.")
            return False
        loan_id = loan[0][0]

        updated = db.execute_query(
            "UPDATE tblLoans SET ReturnDate = ? WHERE LoanID = ?",
            (datetime.now().date(), loan_id)
        )
        if updated:
            db.execute_query(
                "UPDATE tblBook SET CopiesAvailable = CopiesAvailable + 1 WHERE BookID = ?",
                (book_id,)
            )
            print("Book returned successfully.")
            return True
        else:
            print("Return failed.")
            return False

    def view_active_loans(self):
        db = Connection()
        result = db.execute_query(
            """
            SELECT b.BookTitle, b.BookISBN, l.LoanDate, l.DueDate
            FROM tblLoans l
            JOIN tblBook b ON l.BookID = b.BookID
            WHERE l.UserID = ? AND l.ReturnDate IS NULL
            """,
            (self.user_id,)
        )
        if result:
            print("Your active loans:")
            for row in result:
                print(f"{row[0]} (ISBN: {row[1]}) | Loaned: {row[2]} | Due: {row[3]}")
        else:
            print("No active loans found.")

    def request_book(self, isbn: str):
        db = Connection()
        book = db.execute_query(
            "SELECT BookID FROM tblBook WHERE BookISBN = ?",
            (isbn,)
        )
        if not book:
            print("Book not found.")
            return False
        book_id = book[0][0]

        existing = db.execute_query(
            "SELECT * FROM tblReservations WHERE BookID = ? AND UserID = ? AND Status = 'Pending'",
            (book_id, self.user_id)
        )
        if existing:
            print("You have already requested this book.")
            return False

        db.execute_query(
            "INSERT INTO tblReservations (BookID, UserID, ReservationDate, Status) VALUES (?, ?, ?, ?)",
            (book_id, self.user_id, datetime.now().date(), "Pending")
        )
        print("Book request sent successfully.")
        return True
