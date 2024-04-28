
import sqlite3_connector
import sqlite3  # For raising errors
import datetime
from datetime import date
import pandas as pd
from typing import TypedDict
from IPython.display import display


def list_to_string(lst):
    return '(' + ', '.join(lst) + ')'


class Anime(TypedDict):
    """
    {
        'en_name': str,
        'jp_name': str,
        'aired': datetime.date,
        'episodes': int,
        'anime_icon': str,
        'genres': list(str),
        'studios': list(str),
        'roles': list((str:VA_name, str:Role)),
    }
    """
    en_name: str
    jp_name: str
    aired: date
    episodes: int
    anime_icon: str
    genres: list
    studios: list
    roles: list


class DB_Handler(sqlite3_connector.Animagi_DB):
    def __init__(self, DB_name=sqlite3_connector.DEFAULT_DB):
        super().__init__(DB_name)
        self.__first_create_tables()
        self.__sample_data_insert()

    def __first_create_tables(self):
        tables = []
        # _____________Anime part of DB_____________
        # Anime Table.
        tables.append([
            ['create', 'table', '!exists', 'Anime'],
            ['id', int, '!null', 'pk', '++'],  # Anime_id
            ['en_name', (str, 150), 'default', 'null', 'unique'],
            ['jp_name', (str, 150), 'default', 'null', 'unique'],
            ['icon', (str, 200), 'default', 'null'],    # The link to photo
            ['rating', int, 'unsigned', 'default', '0'],
            # Stores sum of rating, updated when a rating is posted.
            # For display divide this number by count of rating done.
            ['aired', datetime],
            ['episodes', int, 'unsigned', 'default', '0'],

            ['ck', ['Anime_en_name', 'is !null', 'or', 'Anime_jp_name', 'is !null']],
        ])
        # Table for allowing multi-value attribute of genre in anime table.
        # Genre Table.
        tables.append([
            ['create', 'table', '!exists', 'Genre'],
            ['Anime_id', int, '!null'],
            ['Genre_DB_id', int, '!null'],

            ['pk', ['Genre_Anime_id', 'Genre_Genre_DB_id']],
            ['fk', ['Genre_Anime_id'], 'ref', 'Anime', ['Anime_id']],
            ['fk', ['Genre_Genre_DB_id'], 'ref', 'Genre_DB', ['Genre_DB_id']]
        ])
        # Store genre names with respective ids.
        # Genre DB Table.
        tables.append([
            ['create', 'table', '!exists', 'Genre_DB'],
            ['id', int, '!null', 'pk', '++'],  # Referenced by Genre
            ['name', (str, 20), '!null', 'unique']
        ])

        # _____________User part of DB_____________
        # User Table.
        tables.append([
            ['create', 'table', '!exists', 'User'],
            ['id', int, '!null', 'pk', '++'],
            ['tag', (str, 20), '!null', 'unique'],
            ['icon', (str, 200), 'default', 'null'],  # The icon link string.
            ['email', (str, 320), '!null', 'unique'],  # Needs to be validated by python
            ['pwdhash', (str, 97), '!null']  # Makes use of Argon2
        ])
        # Ratings Table.
        tables.append([
            ['create', 'table', '!exists', 'Ratings'],
            ['User_id', int, '!null'],
            ['Anime_id', int, '!null'],
            ['rating', int, '!null'],  # Set check to be 0-10.

            ['ck', ['Ratings_rating', 'btwn', '0', 'and', '10']],
            ['pk', ['Ratings_User_id', 'Ratings_Anime_id']],
            ['fk', ['Ratings_User_id'], 'ref', 'User', ['User_id']],
            ['fk', ['Ratings_Anime_id'], 'ref', 'Anime', ['Anime_id']]
        ])

        # _____________Production part of DB_____________
        # Studio Table.
        tables.append([
            ['create', 'table', '!exists', 'Studio'],
            ['Anime_id', int, '!null'],
            ['Studio_DB_id', int, '!null'],

            ['pk', ['Studio_Anime_id', 'Studio_Studio_DB_id']],
            ['fk', ['Studio_Anime_id'], 'ref', 'Anime', ['Anime_id']],
            ['fk', ['Studio_Studio_DB_id'], 'ref', 'Studio_DB', ['Studio_DB_id']]
        ])
        # Studio DB Table.
        tables.append([
            ['create', 'table', '!exists', 'Studio_DB'],
            ['id', int, '!null', 'pk', '++'],  # Referenced by Studio
            ['name', (str, 70), '!null', 'unique']
        ])
        # Cast Table, stores anime and cast list, allowing same casting for different anime.
        tables.append([
            ['create', 'table', '!exists', 'Cast'],
            ['Anime_id', int, '!null'],
            ['Casting_id', int, '!null'],

            ['pk', ['Cast_Anime_id', 'Cast_Casting_id']],
            ['fk', ['Cast_Anime_id'], 'ref', 'Anime', ['Anime_id']],
            ['fk', ['Cast_Casting_id'], 'ref', 'Casting', ['Casting_id']]
        ])
        # Casting Table.
        tables.append([
            ['create', 'table', '!exists', 'Casting'],
            ['id', int, '!null', 'pk', '++'],
            ['VA_DB_id', int, '!null'],
            ['role', (str, 70)],

            ['unique', ['Casting_VA_DB_id', 'Casting_role']],
            ['fk', ['Casting_VA_DB_id'], 'ref', 'VA_DB', ['VA_DB_id']]
        ])
        # VA BD Table.
        tables.append([
            ['create', 'table', '!exists', 'VA_DB'],
            ['id', int, '!null', 'pk', '++'],  # Referenced by Casting
            ['name', (str, 70), '!null', 'unique'],
            ['icon', (str, 200), 'default', 'null']  # The link to photo.
        ])

        # _____________Comment part of DB_____________
        # Thread Table.
        tables.append([
            ['create', 'table', '!exists', 'Thread'],
            ['id', int, '!null', 'pk', '++'],  # Referenced by Comment
            ['Anime_id', int, '!null'],

            ['fk', ['Thread_Anime_id'], 'ref', 'Anime', ['Anime_id']],
        ])
        # Comment Table.
        tables.append([
            ['create', 'table', '!exists', 'Comment'],
            ['Thread_id', int, '!null'],
            ['OP_id', int, '!null'],  # Basically a property of Thread_id, storing the comment data.
            ['reply_id', int, '!null'],

            ['pk', ['Comment_Thread_id', 'Comment_reply_id']],
            ['fk', ['Comment_OP_id'], 'ref', 'Comment_DB', ['Comment_DB_id']],
            ['fk', ['Comment_reply_id'], 'ref', 'Comment_DB', ['Comment_DB_id']],
        ])
        # Comment DB Table.
        tables.append([
            ['create', 'table', '!exists', 'Comment_DB'],
            ['id', int, '!null', 'pk', '++'],
            ['text', 'txt', '!null'],
            ['User_id', int, '!null'],
            ['post_time', datetime, '!null'],

            ['fk', ['Comment_DB_User_id'], 'ref', 'User', ['User_id']]
        ])

        # __________________________________________________________________________________________
        # With the commands above run the execs.
        for tbl in tables:
            self.exec_cmd(self.get_create_tbl_cmd(tbl))
            self.commit()

    def __sample_data_insert(self):
        # ____________________VA DB prime____________________
        va_db_inp = [
            ("Kaji, Yuuki", 'https://cdn.myanimelist.net/r/42x62/images/voiceactors/2/66416.jpg?s=91e56f66a0be72a89dff77e0d8ec55ce'),
            ("Inoue, Marina", 'https://cdn.myanimelist.net/r/42x62/images/voiceactors/1/68016.jpg?s=aa4c55f4d2b3281db36bec68900e4695'),
            ("Ishikawa, Yui", 'https://cdn.myanimelist.net/r/42x62/images/voiceactors/2/69967.jpg?s=2934c5cc8f074309f2681b81624f540f'),
            ("Kamiya, Hiroshi", 'https://cdn.myanimelist.net/r/42x62/images/voiceactors/1/66163.jpg?s=775d0965030b624274719144d678113a'),
            ("Ono, Daisuke", 'https://cdn.myanimelist.net/r/42x62/images/voiceactors/1/54593.jpg?s=2cd350a1a5beea92a102bb5309aabae5'),
            ("Park, Romi", 'https://cdn.myanimelist.net/r/42x62/images/voiceactors/1/54602.jpg?s=d50f919d30a6d801da91a30506c5d5e8'),
            ("Kobayashi, Yuu", 'https://cdn.myanimelist.net/r/42x62/images/voiceactors/1/54674.jpg?s=bea36a3540ce1bebe27820be99a19232'),
        ]
        self.insert_va_db(va_db_inp)

    def insert_anime(self, anime_dict: Anime):
        """
        Insert an Anime into the database.
        :param anime_dict: Anime type dictionary holding all anime data to be inserted.
        """
        try:
            self.__insert_anime_into_table(
                anime_dict['en_name'], anime_dict['jp_name'], anime_dict['aired'],
                anime_dict['episodes'], anime_dict['anime_icon']
            )
        except ValueError as e:
            print(e)
        # If here anime was inserted, get its idx.
        valid_name = None
        if anime_dict['en_name'] is not None:
            valid_name = anime_dict['en_name']
        else:
            valid_name = anime_dict['jp_name']
        ani_idx = self.__get_anime_idx(valid_name)

        # Add the genres.
        self.insert_genre(valid_name, anime_dict['genres'], ani_idx_override=ani_idx)
        # Add the studios.
        self.insert_studios(valid_name, anime_dict['studios'], ani_idx_override=ani_idx)
        # Add the cast as role-va pair.
        self.insert_casting(valid_name, anime_dict['roles'], ani_idx_override=ani_idx)

        # Commit to database.
        self.commit()

    def __insert_anime_into_table(self, en_name, jp_name, aired, episodes, icon_path=None):
        """
        Insert anime into anime table.
        :param en_name: Can be a string or None.
        :param jp_name: Can be a string or None.
        :param aired: A datetime object.
        :param episodes: Number of episodes.
        :param icon_path: A string or None.
        """
        if en_name is not None or jp_name is not None:
            cols = []
            anime_prm = []
            if en_name is not None:
                cols.append('Anime_en_name')
                anime_prm.append(en_name)
            if jp_name is not None:
                cols.append('Anime_jp_name')
                anime_prm.append(jp_name)
            if icon_path is not None:
                cols.append('Anime_icon')
                anime_prm.append(icon_path)
            cols.append('Anime_aired')
            anime_prm.append(aired)
            cols.append('Anime_episodes')
            anime_prm.append(episodes)

            anime_cmd = f'''INSERT INTO Anime {list_to_string(cols)} VALUES {list_to_string(['?'] * len(cols))}'''
            try:
                self.exec_cmd(anime_cmd, anime_prm)
                self.commit()
            except sqlite3.IntegrityError as e:
                print("Anime already exists.", e)
        else:
            raise ValueError("__insert_anime_into_table(): Requires a valid english or japanese name")

    # ~~~~~~~~~~~~~~~~~~Insert into Genre table functions~~~~~~~~~~~~~~~~~~
    def insert_genre(self, anime_name, genre_names: list, ani_idx_override=None):
        """
        Insert genres into genre table for the anime.
        :param anime_name: Name of anime to get the anime id.
        :param genre_names: Genre names.
        :param ani_idx_override: Override from higher call to skip anime search.
        """
        # print("GENRE LOG: ", genre_names)
        # Get the indices for anime and genre.
        anime_idx = self.__get_anime_idx(anime_name) if ani_idx_override is None else ani_idx_override
        genre_idxs = self.__get_genre_db_idxs(genre_names)
        # If anime is not in table can't add genre to it.
        if anime_idx is None:
            print(f'handler.insert_genre(): No anime with name {anime_name} found, insert interrupted.')
            return
        genre_cmd = '''INSERT INTO Genre VALUES (?, ?)'''
        for idx in genre_idxs:
            try:
                self.exec_cmd(genre_cmd, (anime_idx, idx))
            except sqlite3.IntegrityError as e:
                pass

    def __get_genre_db_idxs(self, genre_names):
        idx_lst = []
        # Insert if the genre doesn't exist.
        for genre_name in genre_names:
            try:
                self.insert_genre_db([(genre_name,)])
            # Ignore error if genre in db.
            except sqlite3.IntegrityError as e:
                pass
            genre_db_idx_cmd = '''SELECT Genre_DB_id FROM Genre_DB WHERE Genre_DB_name = ?'''
            idx_lst.append(self.exec_cmd(genre_db_idx_cmd, (genre_name,)).fetchone()[0])
        return idx_lst

    def insert_genre_db(self, genre_names):
        genre_db_cmd = '''INSERT INTO Genre_DB (Genre_DB_name) VALUES (?)'''
        self.exec_many_cmd(genre_db_cmd, genre_names)

    # ~~~~~~~~~~~~~~~~~~Insert into Studio table functions~~~~~~~~~~~~~~~~~~
    def insert_studios(self, anime_name, studio_names: list, ani_idx_override=None):
        """
        Insert studios into studio table for the anime.
        :param anime_name: Name of anime to get the anime id.
        :param studio_names: Studio names.
        :param ani_idx_override: Override from higher call to skip anime search.
        """
        # Get the indices for anime.
        anime_idx = self.__get_anime_idx(anime_name) if ani_idx_override is None else ani_idx_override
        studio_idxs = self.__get_studios_idxs(studio_names)
        if anime_idx is None:
            print(f'handler.insert_studios(): No anime with name {anime_name} found, insert interrupted.')
            return
        studio_cmd = '''INSERT INTO Studio (Studio_Anime_id, Studio_Studio_DB_id) VALUES (?, ?)'''
        for idx in studio_idxs:
            try:
                self.exec_cmd(studio_cmd, (anime_idx, idx))
            except sqlite3.IntegrityError as e:
                pass

    def __get_studios_idxs(self, studio_names):
        """
        Insert the studio names into the Studio table.
        :param studio_names: List of studio names.
        :return: List of studio indices.
        """
        idx_lst = []
        # Insert if the genre doesn't exist.
        for studio_name in studio_names:
            try:
                self.insert_studio_db([(studio_name,)])
            # Ignore error if genre in db.
            except sqlite3.IntegrityError as e:
                pass
            studio_db_idx_cmd = '''SELECT Studio_DB_id FROM Studio_DB WHERE Studio_DB_name = ?'''
            idx_lst.append(self.exec_cmd(studio_db_idx_cmd, (studio_name,)).fetchone()[0])
        return idx_lst

    def insert_studio_db(self, studio_names):
        studio_db_cmd = '''INSERT INTO Studio_DB (Studio_DB_name) VALUES (?)'''
        self.exec_many_cmd(studio_db_cmd, studio_names)

    # ~~~~~~~~~~~~~~~~~~Insert into Casting table functions~~~~~~~~~~~~~~~~~~
    def insert_casting(self, anime_name, casting: list, ani_idx_override=None):
        """
        Insert casting into Casting table.
        :param anime_name: Name of anime to get the anime id.
        :param casting: List of tuples as (va_name, role_name).
        :param ani_idx_override: Override from higher call to skip anime search.
        """
        # Get the indices for anime and genre.
        anime_idx = self.__get_anime_idx(anime_name) if ani_idx_override is None else ani_idx_override
        # If anime is not in table can't add genre to it.
        if anime_idx is None:
            print(f'handler.insert_casting(): No anime with name {anime_name} found, insert interrupted.')
            return
        # Assign the roles to the VAs.
        for cast in casting:
            va_idx = self.__get_va_idx(cast[0])
            role_insert_cmd = '''INSERT INTO Casting (Casting_VA_DB_id, Casting_role) VALUES (?, ?)'''
            try:
                self.exec_cmd(role_insert_cmd, (va_idx, cast[1]))
            # If role assigned to VA is stored skip it.
            except sqlite3.IntegrityError as e:
                pass

    def __get_va_idx(self, va_name):
        """
        Add the VA or if exists get the va index.
        :param va_name: Name of the VA.
        :return: Index of the VA.
        """
        # Insert if the VA doesn't exist.
        try:
            self.insert_va_db([(va_name,)])
        # Ignore error if VA in db.
        except sqlite3.IntegrityError as e:
            pass
        va_db_idx_cmd = '''SELECT VA_DB_id FROM VA_DB WHERE VA_DB_name = ?'''
        return self.exec_cmd(va_db_idx_cmd, (va_name,)).fetchone()[0]

    def insert_va_db(self, vas: list):
        # va is a tuple of (va name, icon string) or (name, None)
        for va in vas:
            if len(va) == 2 and va[1] is not None:
                va_db_cmd = '''INSERT INTO VA_DB (VA_DB_name, VA_DB_icon) VALUES (?, ?)'''
                try:
                    self.exec_cmd(va_db_cmd, va)
                # If adding icons allow continuing,
                except sqlite3.IntegrityError as e:
                    pass
            else:
                va_db_cmd = '''INSERT INTO VA_DB (VA_DB_name) VALUES (?)'''
                self.exec_cmd(va_db_cmd, (va[0],))

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __get_anime_idx(self, anime_name):
        anime_idx_cmd = '''SELECT Anime_id FROM Anime WHERE Anime_en_name = ? OR Anime_jp_name = ?'''
        query_inp = (anime_name, anime_name)
        idx = self.exec_cmd(anime_idx_cmd, query_inp).fetchone()
        return idx[0] if idx is not None else None

    def show_table(self, cursor_out, indices=None):
        """
        Print the cursor output as a table.
        :param indices: list of column names to be used as indices.
        :param cursor_out: Cursor object.
        """
        # Make the table as a DataFrame object.
        pd.set_option('display.max_colwidth', 320)
        tbl = pd.DataFrame([list(row) for row in cursor_out.fetchall()],
                           columns=[col[0] for col in cursor_out.description])
        # If indices are given add it to table.
        if indices is not None:
            tbl.set_index(indices, inplace=True)
        # Print the table.
        display(tbl)

    def __del__(self):
        super().__del__()
