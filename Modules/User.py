from connection import Connection

class User:
    
    def __init__(self, username, password,email, phone_number):
        self.username = username
        self.password = password
        self.email = email
        self.phone_number = phone_number
    
    def login(self, input_username, input_password):
        
        db = Connection()
        result = db.execute_query(
            "SELECT * FROM Users WHERE username = ? AND password = ?",
            (input_username, input_password)
        )
        if result and len(result) > 0:
            print("✅ Login successful.")
            return True
        else:
            print("❌ Invalid username or password.")
            return False

    def register(self, input_username, input_password):
        
        db = Connection()
        # 1. Check if username already exists
        existing = db.execute_query(
            "SELECT * FROM Users WHERE username = ?",
            (input_username,)
        )

        if existing and len(existing) > 0:
            print("⚠️ Username already exists. Please choose another one.")
            return False

        # 2. Insert new user if not exists
        result = db.execute_query(
            "INSERT INTO Users (username, password) VALUES (?, ?)",
            (input_username, input_password)
        )
        if result is None:
            print("✅ Registration successful.")
            return True
        else:
            print("❌ Registration failed.")
            return False
