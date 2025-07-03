import pyodbc

class Connection:
    
    

    def __init__(self):
        try:
            self.__conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=localhost\\SQLEXPRESS;'
                'DATABASE=LibraryDb;'
                'Trusted_Connection=yes;'
            )
            print("✅ Connection established.")
        except pyodbc.Error as e:
            print(f"❌ Connection error: {e}")
            self.__conn = None
            
    def get_cursor(self):
        if self.__conn:
            try:
                cursor = self.__conn.cursor()
                print("🖥️ Cursor obtained.")
                return cursor
            except Exception as e:
                print(f"❌ Cursor error: {e}")
                return None
        else:
            print("❌ No connection available.")
            return None

    def close_connection(self):
        try:
            self.__conn.close()
            print("🔒 Connection closed.")
        except Exception as e:
            print(f"❌ Error closing connection: {e}")

    def get_connection_info(self):
        try:
            server = self.__conn.getinfo(pyodbc.SQL_SERVER_NAME)
            database = self.__conn.getinfo(pyodbc.SQL_DATABASE_NAME)
            print(f"🧠 Connected to server: {server}, database: {database}")
            return server, database
        except Exception as e:
            print(f"❌ Info error: {e}")
            return None, None

    def execute_query(self, query, params=None):
        try:
            cursor = self.get_cursor()
            if cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                self.__conn.commit()
                print("✅ Query executed.")
                try:
                    return cursor.fetchall()
                except:
                    return None  # for queries that do not return results
        except Exception as e:
            print(f"❌ Query error: {e}")
            return None
t