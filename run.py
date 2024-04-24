from handler import DB_Handler

# Create tables.
db_handle = DB_Handler()

db_handle.exec_cmd("""SELECT name FROM sqlite_master WHERE type='table';""")

# Shows all table made successfully.
print(db_handle.DB_cursor.fetchall())
