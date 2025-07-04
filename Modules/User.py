from Modules.Connection import Connection



class User:
    
    def __init__(self):
        self.__username = None
        self.__password = None
        self.user_id = None
        
    def login(self, input_username, input_password):
        db = Connection()
        result = db.execute_query(
            "SELECT * FROM tblUser WHERE UserName = ? AND UserPassword = ?",
            (input_username, input_password)
        )
        if result and len(result) > 0:  
            print("✅ Login successful.")
            self._User__username = result[0][1]
            self._User__password = result[0][2]
            self.user_id = result[0][0]  # ID'yi buraya al!
            return True
        else:
            print("❌ Invalid username or password.")
            return False

    def register(self, input_username, input_password):
        
        db = Connection()
        # Check if username already exists
        existing = db.execute_query(
            "SELECT * FROM tblUser WHERE UserName = ?",
            (input_username,)
        )

        if existing and len(existing) > 0:
            print("⚠️ Username already exists. Please choose another one.")
            return False

        # Insert new user if not exists
        result = db.execute_query(
            "INSERT INTO tblUser (UserName, UserPassword) VALUES (?, ?)",
            (input_username, input_password)
        )
        if result is None:
            print("✅ Registration successful.")
            return True
        else:
            print("❌ Registration failed.")
            return False

    def get_details(self):
        if self.__username:
            return {
                "username": self.__username,
                "password": self.__password,
                "email": self.__email,
                "phone_number": self.__phone_number
            }
        else:
            print("❌ No user logged in.")
            return None

    