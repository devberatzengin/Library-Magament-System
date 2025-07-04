from Modules.User import User
from datetime import datetime, timedelta
from Modules.Connection import Connection

class Staff(User):

    def __init__(self):
        super().__init__()

    def get_id(self):
        if self.user_id is not None:
            return self.user_id
        else:
            print("User ID is not set.")
            return None

    def get_staff_details(self):
        return {
            "username": self._User__username,
            "staff_id": self.__staff_id,
            "department": self.__department
        }

    def set_staff_details(self, staff_id, department):
        self.__staff_id = staff_id
        self.__department = department

    def add_new_book(self, title, author, isbn, publication_year):
        if self.am_i_staff() is False:
            print("You are not authorized to add new books.")
            return
        db = Connection()
        result = db.execute_query(
            "INSERT INTO tblBook (BookTitle, BookAuthor, BookISBN, BookPublicationYear) VALUES (?, ?, ?, ?)",
            (title, author, isbn, publication_year)
        )
        if result:
            print("New book added successfully.")
            return True
        else:
            print("Failed to add new book.")
            return False

    def delete_book(self, isbn):
        if self.am_i_staff() is False:
            print("You are not authorized to delete books.")
            return
        db = Connection()
        result = db.execute_query(
            "DELETE FROM tblBook WHERE BookISBN = ?",
            (isbn,)
        )
        if result:
            print("Book deleted successfully.")
            return True
        else:
            print("Failed to delete book.")
            return False

    def create_new_member(self, username, password, email, phone_number):
        if self.am_i_staff() is False:
            print("You are not authorized to create new members.")
            return
        db = Connection()
        result = db.execute_query(
            "INSERT INTO tblUser (UserName, UserPassword, UserEmail, UserPhoneNumber, UserRole) VALUES (?, ?, ?, ?, 0)",
            (username, password, email, phone_number)
        )
        if result:
            print("New member created successfully.")
            return True
        else:
            print("Failed to create new member.")
            return False

    def am_i_staff(self):
        db = Connection()
        result = db.execute_query(
            "SELECT * FROM tblUser WHERE UserName = ?",
            (self._User__username,)
        )
        if result and result[0][5] == 1:
            return True
        else:
            return False

    def loan_to_user(self, isbn: str, user_id: int, days_until_due: int = 14):
        db = Connection()
        book = db.execute_query(
            "SELECT BookID, CopiesAvailable FROM tblBook WHERE BookISBN = ?",
            (isbn,)
        )
        if not book:
            print("Book not found.")
            return False
        book_id, copies = book[0]
        if copies <= 0:
            print("No copies available to loan.")
            return False
        active_loans = db.execute_query(
            "SELECT COUNT(*) FROM tblLoans WHERE UserID = ? AND ReturnDate IS NULL",
            (user_id,)
        )
        if active_loans and active_loans[0][0] >= 3:
            print("This user already has 3 books on loan.")
            return False
        on_loan = db.execute_query(
            "SELECT * FROM tblLoans WHERE BookID = ? AND ReturnDate IS NULL",
            (book_id,)
        )
        if on_loan and len(on_loan) >= copies:
            print("All copies of this book are currently on loan.")
            return False
        due_date = (datetime.now() + timedelta(days=days_until_due)).date()
        insert = db.execute_query(
            "INSERT INTO tblLoans (BookID, UserID, DueDate) VALUES (?, ?, ?)",
            (book_id, user_id, due_date)
        )
        if insert:
            db.execute_query(
                "UPDATE tblBook SET CopiesAvailable = CopiesAvailable - 1 WHERE BookID = ?",
                (book_id,)
            )
            print("Book successfully loaned to user.")
            return True
        else:
            print("Failed to insert loan record.")
            return False

    def approve_request(self, reservation_id: int, days_until_due: int = 14):
        db = Connection()
        res = db.execute_query(
            "SELECT BookID, UserID, Status FROM tblReservations WHERE ReservationID = ?",
            (reservation_id,)
        )
        if not res:
            print("Reservation not found.")
            return False
        book_id, user_id, status = res[0]
        if status != "Pending":
            print("This reservation has already been processed.")
            return False
        book = db.execute_query(
            "SELECT CopiesAvailable FROM tblBook WHERE BookID = ?",
            (book_id,)
        )
        if not book or book[0][0] <= 0:
            print("No available copies to loan.")
            return False
        active_loans = db.execute_query(
            "SELECT COUNT(*) FROM tblLoans WHERE UserID = ? AND ReturnDate IS NULL",
            (user_id,)
        )
        if active_loans[0][0] >= 3:
            print("This user already has 3 active loans.")
            return False
        due_date = (datetime.now() + timedelta(days=days_until_due)).date()
        db.execute_query(
            "INSERT INTO tblLoans (BookID, UserID, DueDate) VALUES (?, ?, ?)",
            (book_id, user_id, due_date)
        )
        db.execute_query(
            "UPDATE tblBook SET CopiesAvailable = CopiesAvailable - 1 WHERE BookID = ?",
            (book_id,)
        )
        db.execute_query(
            "UPDATE tblReservations SET Status = 'Approved' WHERE ReservationID = ?",
            (reservation_id,)
        )
        print("Reservation approved and book loaned.")
        return True

    def reject_request(self, reservation_id: int, reason: str = "Not specified"):
        db = Connection()
        res = db.execute_query(
            "SELECT Status FROM tblReservations WHERE ReservationID = ?",
            (reservation_id,)
        )
        if not res:
            print("Reservation not found.")
            return False
        status = res[0][0]
        if status != "Pending":
            print(f"Cannot reject. Status is already '{status}'.")
            return False
        db.execute_query(
            "UPDATE tblReservations SET Status = 'Rejected', RejectionReason = ? WHERE ReservationID = ?",
            (reason, reservation_id)
        )
        print("Reservation has been rejected.")
        return True

    def view_pending_requests(self):
        db = Connection()
        pending = db.execute_query("""
            SELECT r.ReservationID, b.BookTitle, b.BookISBN, u.UserName, r.ReservationDate
            FROM tblReservations r
            JOIN tblBook b ON r.BookID = b.BookID
            JOIN tblUser u ON r.UserID = u.UserID
            WHERE r.Status = 'Pending'
            ORDER BY r.ReservationDate ASC
        """)
        if not pending:
            print("No pending book requests found.")
            return
        print("\nPending Book Requests:")
        print("-" * 60)
        for row in pending:
            print(f"ID: {row[0]} | {row[1]} ({row[2]}) | {row[3]} | {row[4]}")
        print("-" * 60)
