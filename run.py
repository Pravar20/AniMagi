from handler import DB_Handler, Anime
from datetime import date


db_handle = DB_Handler()
# db_handle.sample_data_insert()
print("AOT rating:", db_handle.get_anime_rating('Attack on Titan'))

# view_tbl_cmd = '''SELECT * FROM Casting'''
# cmd_out = db_handle.exec_cmd(view_tbl_cmd)
# db_handle.show_table(cmd_out, ['Casting_id', 'Casting_VA_DB_id'])
