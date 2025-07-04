import pyodbc
from Modules.Log import log_error

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

    def execute_query(self, query, params=None, source="execute_query"):
        try:
            cursor = self.get_cursor()
            if not cursor:
                log_error("Cursor is None", source)
                return None

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            query_type = query.strip().split()[0].lower()

            if query_type == "select":
                result = cursor.fetchall()
                print("✅ SELECT query executed.")
                return result
            else:
                self.__conn.commit()
                print("✅ Non-SELECT query executed and committed.")
                return True  # UPDATE, INSERT, DELETE için True döner

        except Exception as e:
            log_error(str(e), source)
            print(f"❌ Query error: {e}")
            return None
