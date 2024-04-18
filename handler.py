import sqlite3_connector
import datetime

"""
# setting up Database
def create_table():
    
    # anime table
    c.execute('''CREATE TABLE IF NOT EXISTS ANIME(
              anime_id INTEGER PRIMARY KEY,
              anime_name TEXT NOT NULL,
              anime_rating INTEGER,
              anime_aired DATE,
              studio_id INTEGER,
              cast_id INTEGER
    )''')
    # user account table
    c.execute('''CREATE TABLE IF NOT EXISTS USER(
              user_id INTEGER PRIMARY KEY,
              user_tag TEXT NOT NULL,
              user_email TEXT NOT NULL,
              user_ph_no TEXT,
              user_password TEXT NOT NULL
    )''')
    # rating table
    c.execute('''CREATE TABLE IF NOT EXISTS RATING(
              rating_id INTEGER PRIMARY KEY,
              anime_id INTEGER,
              user_id INTEGER,
              rating INTEGER
    )''')
    # production studio table
    c.execute('''CREATE TABLE IF NOT EXISTS STUDIO(
              studio_id INTEGER PRIMARY KEY,
              studio_name TEXT NOT NULL,
              anime_id INTEGER,
              cast_id INTEGER,
              cast_storage TEXT
    )''')

# insert data into anime table
def insert_anime(anime_name, anime_rating, anime_aired, studio_id, cast_id):
    c.execute('''
        INSERT INTO ANIME (anime_name, anime_rating, anime_aired, studio_id, cast_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (anime_name, anime_rating, anime_aired, studio_id, cast_id))

# remove data from anime table
def remove_anime(anime_id):
    c.execute('''DELETE FROM ANIME WHERE anime_id = ?''', (anime_id,))

# update data in anime table
def update_anime(anime_id, update_data_type, data):
    if update_data_type == 'anime_name':
        c.execute('''UPDATE ANIME SET anime_name = ? WHERE anime_id = ?''', (data, anime_id))
    elif update_data_type == 'anime_rating':
        c.execute('''UPDATE ANIME SET anime_rating = ? WHERE anime_id = ?''', (data, anime_id))
    elif update_data_type == 'anime_aired':
        c.execute('''UPDATE ANIME SET anime_aired = ? WHERE anime_id = ?''', (data, anime_id))
    elif update_data_type == 'studio_id':
        c.execute('''UPDATE ANIME SET studio_id = ? WHERE anime_id = ?''', (data, anime_id))
    elif update_data_type == 'cast_id':
        c.execute('''UPDATE ANIME SET cast_id = ? WHERE anime_id = ?''', (data, anime_id)) else:
        print('Invalid data type')

def fetch_anime_by_name(anime_name):

    c.execute('SELECT * FROM ANIME WHERE anime_name = ?', (anime_name,))
    
    anime_found = c.fetchone()
    if anime_found:
        return anime_found else:
        print(f"No anime found with anime_id: {anime_name}")

# insert data into user table
def insert_user_data(user_tag, user_email, user_ph_no, user_password):
    c.execute('''
        INSERT INTO USER (user_tag, user_email, user_ph_no, user_password)
        VALUES (?, ?, ?, ?)
    ''', (user_tag, user_email, user_ph_no, user_password))

# remove data from user table
def remove_user_data(user_id):
    c.execute('''DELETE FROM USER WHERE user_id = ?''', (user_id,))

# update data in user table
def update_user_data(user_id, update_data_type, data):
    if update_data_type == 'user_tag':
        c.execute('''UPDATE USER SET user_tag = ? WHERE user_id = ?''', (data, user_id))
    elif update_data_type == 'user_email':
        c.execute('''UPDATE USER SET user_email = ? WHERE user_id = ?''', (data, user_id))
    elif update_data_type == 'user_ph_no':
        c.execute('''UPDATE USER SET user_ph_no = ? WHERE user_id = ?''', (data, user_id))
    elif update_data_type == 'user_password':
        c.execute('''UPDATE USER SET user_password = ? WHERE user_id = ?''', (data, user_id)) else:
        print('Invalid data type')

def clear_table(table_name):
    table = table_name.upper()
    query = f"DELETE FROM {table_name}"
    c.execute(query)


    c.execute('''CREATE TABLE IF NOT EXISTS ANIME(
              anime_id INTEGER PRIMARY KEY,
              anime_name TEXT NOT NULL,
              anime_rating INTEGER,
              anime_aired DATE,
              studio_id INTEGER,
              cast_id INTEGER
    )''')
"""


class DB_handler(sqlite3_connector.Animagi_DB):
    def __init__(self, DB_name=...):
        super().__init__(DB_name)

    def __FIRST_CREATE_TABLES(self):
        # _____________Anime part of DB_____________
        anime_table = [
            ['create', 'table', '!exists', 'Anime'],
            ['id', int, 'unsigned', '!null', 'pk', '++'],
            ['en_name', (str, 150)],
            ['jp_name', (str, 150)],

            ['icon', (str, 30)],    # The path for icon of the anime stored in \icons\Anime
                                    # 'icons/Anime/1.jpg' stores this.
            ['rating', int],
            ['aired', datetime],

            ['Studio_id', int, 'unsigned'],
            ['Cast_id', int, 'unsigned'],
            ['Genre_id', int, 'unsigned'],

            ['ck', ['Anime_en_name', 'is !null', 'or', 'Anime_jp_name', 'is !null']],
            ['fk', ['Anime_Studio_id'], 'ref', 'Studio', ['Studio_id']],
            ['fk', ['Anime_Cast_id'], 'ref', 'Cast', ['Cast_id']],
            ['fk', ['Anime_Genre_id'], 'ref', 'Genre', ['Genre_id']]
        ]
        # Store genre names with respective ids.
        genre_db_table = [
            ['create', 'table', '!exists', 'Genre_DB'],
            ['id', int, 'unsigned', '!null', 'pk', '++'],   # Referenced by Genre
            ['name', (str, 20), '!null', 'unique']
        ]
        # Table for allowing multi-value attribute of genre in anime table.
        genre_table = [
            ['create', 'table', '!exists', 'Genre'],
            ['id', int, 'unsigned', '!null', 'pk'],     # Referenced by Anime

            ['Genre_DB_id', int, 'unsigned', '!null'],
            ['fk', ['Genre_Genre_DB_id'], 'ref', 'Genre_DB', ['Genre_DB_id']]
        ]

        # _____________User part of DB_____________
        user_table = [
            ['create', 'table', '!exists', 'User'],
            ['id', int, 'unsigned', '!null', 'pk', '++'],
            ['tag', (str, 20), '!null', 'unique'],
            ['icon', (str, 30)],    # The path for icon of the anime stored in \icons\User
            ['email', (str, 320), '!null', 'unique'],   # Needs to be validated by python
            ['pwdhash', (str, 97), '!null']     # Makes use of Argon2
        ]
        # User ratings.
        ratings_table = [
            ['create', 'table', '!exists', 'Ratings'],
            ['User_id', int, 'unsigned', '!null'],
            ['Anime_id', int, 'unsigned', '!null'],
            ['rating', int, 'unsigned', '!null'],   # Set by python to be 0-10.

            ['pk', ['User_id', 'Anime_id']],
            ['fk', ['Ratings_User_id'], 'ref', 'User', ['User_id']],
            ['fk', ['Ratings_Anime_id'], 'ref', 'Anime', ['Anime_id']]
        ]

        # _____________Production part of DB_____________
        production_table = [
            ['create', 'table', '!exists', 'Production'],
            ['Anime_id', int, 'unsigned', '!null'],
            ['Studio_id', int, 'unsigned', '!null'],
            ['Cast_id', int, 'unsigned', '!null'],

            ['pk', ['Production_Anime_id', 'Production_Studio_id', 'Production_Cast_id']],
            ['fk', ['Production_Anime_id'], 'ref', 'Anime', ['Anime_id']],
            ['fk', ['Production_Studio_id'], 'ref', 'Studio', ['Studio_id']],
            ['fk', ['Production_Cast_id'], 'ref', 'Cast', ['Cast_id']]
        ]

        studio_table = [
            ['create', 'table', '!exists', 'Studio'],
            ['id', int, 'unsigned', '!null'],  # Referenced by Production
            ['Studio_DB_id', int, 'unsigned', '!null'],

            ['pk', ['Studio_id', 'Studio_Studio_DB_id']],
            ['fk', ['Studio_Studio_DB_id'], 'ref', 'Studio_DB', ['Studio_DB_id']]
        ]

        studio_db_table = [
            ['create', 'table', '!exists', 'Studio_DB'],
            ['id', int, 'unsigned', '!null', 'pk', '++'],  # Referenced by Studio
            ['name', (str, 70), '!null']
        ]

        cast_table = [
            ['create', 'table', '!exists', 'Cast'],
            ['id', int, 'unsigned', '!null'],   # Referenced by Production
            ['VA_DB_id', int, 'unsigned', '!null'],
            ['role', (str, 70)],

            ['pk', ['Cast_id', 'Cast_VA_DB_id']],
            ['fk', ['Cast_VA_DB_id'], 'ref', 'VA_DB', ['VA_DB_id']]
        ]

        va_db_table = [
            ['create', 'table', '!exists', 'VA_DB'],
            ['id', int, 'unsigned', '!null', 'pk', '++'],   # Referenced by Cast
            ['name', (str, 70), '!null'],
            ['icon', (str, 30)]     # The path for icon of the anime stored in \icons\VA
        ]

        # _____________Comment part of DB_____________
        # TODO:

    def __del__(self):
        super().__del__()
