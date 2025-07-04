from Modules.User import User
from datetime import datetime, timedelta
from Modules.Connection import Connection

class Staff(User):

    def __init__(self):
        super().__init__()
        
    def get_id (self):
        if self.user_id is not None:
            return self.user_id
        else:
            print("ℹ️ User ID is not set.")
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
            print("❌ You are not authorized to add new books.")
            return
        else:
            print("✅ You are authorized to add new books.")
            db = Connection()
            result = db.execute_query(
                "INSERT INTO tblBook (BookTitle, BookAuthor, BookISBN, BookPublicationYear) VALUES (?, ?, ?, ?)",
                (title, author, isbn, publication_year)
            )
            if result:
                print("✅ New book added successfully.")
                return True
            else:
                print("❌ Failed to add new book.")
                return False

    def delete_book(self, isbn):
        if self.am_i_staff() is False:
            print("❌ You are not authorized to delete books.")
            return 
        else:
            print("✅ You are authorized to delete books.")
            db = Connection()
            result = db.execute_query(
                "DELETE FROM tblBook WHERE BookISBN = ?",
                (isbn,)
            )
            if result:
                print("✅ Book deleted successfully.")
                return True
            else:
                print("❌ Failed to delete book.")
                return False
   
    def create_new_member(self, username, password, email, phone_number):
        if self.am_i_staff() is False:
            print("❌ You are not authorized to create new members.")
            return
        else:
            print("✅ You are authorized to create new members.")
            db = Connection()
            result = db.execute_query(
                "INSERT INTO tblUser (UserName, UserPassword,UserEmail,UserPhoneNumber,UserRole) VALUES (?, ?, ?, ?, 0)",
                (username, password, email, phone_number)
            )
            if result:
                print("✅ New member created successfully.")
                return True
            else:
                print("❌ Failed to create new member.")
                return False
        
    def am_i_staff(self):
        db = Connection()
        result = db.execute_query(
            "SELECT * FROM tblUser WHERE UserName = ?",
            (self._User__username,)
        )
        if result and result[0][5] == 1:
            print("✅ You are a staff member.")
            return True
        else:
            print("❌ You are not a staff member.")
            return False
        
    def loan_to_user(self, isbn: str, user_id: int, days_until_due: int = 14):
        db = Connection()

        # 1. Kitap ISBN ile bulunur
        book = db.execute_query(
            "SELECT BookID, CopiesAvailable FROM tblBook WHERE BookISBN = ?",
            (isbn,)
        )

        if not book:
            print("❌ Book not found.")
            return False

        book_id, copies = book[0]

        if copies <= 0:
            print("❌ No copies available to loan.")
            return False

        # 2. Üyenin aktif ödünç sayısını kontrol et (ReturnDate IS NULL → henüz iade edilmemiş)
        active_loans = db.execute_query(
            "SELECT COUNT(*) FROM tblLoans WHERE UserID = ? AND ReturnDate IS NULL",
            (user_id,)
        )

        if active_loans and active_loans[0][0] >= 3:
            print("⚠️ This user already has 3 books on loan. Cannot loan more.")
            return False

        # 3. Kitap hâlihazırda tüm kopyaları ödünçte mi?
        on_loan = db.execute_query(
            "SELECT * FROM tblLoans WHERE BookID = ? AND ReturnDate IS NULL",
            (book_id,)
        )

        if on_loan and len(on_loan) >= copies:
            print("❌ All copies of this book are currently on loan.")
            return False

        # 4. DueDate hesapla
        due_date = (datetime.now() + timedelta(days=days_until_due)).date()

        # 5. tblLoans tablosuna kayıt ekle
        insert = db.execute_query(
            "INSERT INTO tblLoans (BookID, UserID, DueDate) VALUES (?, ?, ?)",
            (book_id, user_id, due_date)
        )

        if insert:
            # 6. Kopya sayısını 1 azalt
            db.execute_query(
                "UPDATE tblBook SET CopiesAvailable = CopiesAvailable - 1 WHERE BookID = ?",
                (book_id,)
            )

            print("✅ Book successfully loaned to user.")
            return True
        else:
            print("❌ Failed to insert loan record.")
            return False