class Book:
    
    def __init__(self, title, author, isbn, publication_year):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication_year = publication_year

    def get_details(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "publication_year": self.publication_year
        }

    def get_stok(self):
        db = Connection()
        result = db.execute_query(
            "SELECT Stock FROM tblBook WHERE BookISBN = ?",
            (self.isbn,)
        )
        if result and len(result) > 0:
            return result[0][0]
        else:
            return None
    
    def update_stock(self, new_stock):
        db = Connection()
        result = db.execute_query(
            "UPDATE tblBook SET Stock = ? WHERE BookISBN = ?",
            (new_stock, self.isbn)
        )
        if result is not None:
            print("✅ Stock updated successfully.")
            return True
        else:
            print("❌ Failed to update stock.")
            return False
        
    