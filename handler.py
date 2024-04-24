import sqlite3_connector
import datetime


class DB_Handler(sqlite3_connector.Animagi_DB):
    def __init__(self, DB_name=...):
        super().__init__(DB_name)

    def __FIRST_CREATE_TABLES(self):
        # _____________Anime part of DB_____________
        anime_table = [
            ['create', 'table', '!exists', 'Anime'],
            ['id', int, 'unsigned', '!null', 'pk', '++'],   # Anime_id
            ['en_name', (str, 150)],
            ['jp_name', (str, 150)],
            ['icon', (str, 30)],    # The path for icon of the anime stored in \icons\Anime
            # 'icons/Anime/1.jpg' stores this.
            ['rating', int],        # Stores sum of rating, updated when a rating is posted.
            # For display divide this number by count of rating done.
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
            ['rating', int, 'unsigned', '!null'],   # Set check to be 0-10.

            ['ck', ['Ratings_rating', 'btwn', '0', 'and', '10']],
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
        thread_table = [
            ['create', 'table', '!exists', 'Thread'],
            ['id', int, 'unsigned', '!null', 'pk', '++'],   # Referenced by Comment
            ['Anime_id', int, 'unsigned', '!null'],

            ['fk', ['Thread_Anime_id'], 'ref', 'Anime', ['Anime_id']],
        ]

        comment_table = [
            ['create', 'table', '!exists', 'Comment'],
            ['Thread_id', int, 'unsigned', '!null'],
            ['OP_id', int, 'unsigned', '!null'],    # Basically a property of Thread_id, storing the comment data.
            ['reply_id', int, 'unsigned', '!null'],

            ['pk', ['Comment_Thread_id', 'Comment_reply_id']],
            ['fk', ['Comment_OP_id'], 'ref', 'Comment_DB', ['Comment_DB_id']],
            ['fk', ['Comment_reply_id'], 'ref', 'Comment_DB', ['Comment_DB_id']],
        ]

        comment_db_table = [
            ['create', 'table', '!exists', 'Comment_DB'],
            ['id', int, 'unsigned', '!null', 'pk', '++'],
            ['text', str, '!null'],
            ['User_id', int, 'unsigned', '!null'],
            ['timestamp', datetime, '!null'],

            ['fk', ['Comment_DB_User_id'], 'ref', 'User', ['User_id']]
        ]

        # __________________________________________________________________________________________
        # With the commands above run the execs.
        self.exec_cmd(self.get_create_tbl_cmd(anime_table))
        self.exec_cmd(self.get_create_tbl_cmd(genre_db_table))
        self.exec_cmd(self.get_create_tbl_cmd(genre_table))
        self.exec_cmd(self.get_create_tbl_cmd(user_table))
        self.exec_cmd(self.get_create_tbl_cmd(ratings_table))
        self.exec_cmd(self.get_create_tbl_cmd(production_table))
        self.exec_cmd(self.get_create_tbl_cmd(studio_table))
        self.exec_cmd(self.get_create_tbl_cmd(studio_db_table))
        self.exec_cmd(self.get_create_tbl_cmd(cast_table))
        self.exec_cmd(self.get_create_tbl_cmd(va_db_table))
        self.exec_cmd(self.get_create_tbl_cmd(thread_table))
        self.exec_cmd(self.get_create_tbl_cmd(comment_table))
        self.exec_cmd(self.get_create_tbl_cmd(comment_db_table))

    def __del__(self):
        super().__del__()
