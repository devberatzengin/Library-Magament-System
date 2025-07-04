from datetime import datetime

def log_error(message, source=None):
    from Modules.Connection import Connection
    db = Connection()
    db.execute_query(
        "INSERT INTO tblLogs (ErrorMessage, Source, ErrorDate) VALUES (?, ?, ?)",
        (message, source, datetime.now())
    )
