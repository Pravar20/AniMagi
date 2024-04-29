import sqlite3_connector
import sqlite3  # For raising errors
from datetime import date, datetime
import pandas as pd
from typing import TypedDict
from IPython.display import display
from statistics import mean
import re

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
            ['id', int, '!null', 'pk', '++'],  # Referenced by Reply
            ['Anime_id', int, '!null'],
            ['Comment_DB_id', int, '!null'],       # Referencing Comment_DB_id

            ['fk', ['Thread_Anime_id'], 'ref', 'Anime', ['Anime_id']],
            ['fk', ['Thread_Comment_DB_id'], 'ref', 'Comment_DB', ['Comment_DB_id']],
        ])
        # Reply Table.
        tables.append([
            ['create', 'table', '!exists', 'Reply'],
            ['Thread_id', int, '!null'],
            ['Comment_DB_id', int, '!null'],     # Referencing Comment_DB_id

            ['pk', ['Reply_Thread_id', 'Reply_Comment_DB_id']],
            ['fk', ['Reply_Thread_id'], 'ref', 'Thread', ['Thread_id']],
            ['fk', ['Reply_Comment_DB_id'], 'ref', 'Comment_DB', ['Comment_DB_id']],
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
        cast_inp = [(anime_idx, self.__get_casting_idx(cast[0], cast[1])) for cast in casting]

        # Insert into Cast table.
        cast_insert_cmd = '''INSERT INTO Cast (Cast_Anime_id, Cast_Casting_id) VALUES (?, ?)'''
        self.exec_many_cmd(cast_insert_cmd, cast_inp)

    def __get_casting_idx(self, va_name, role_name, va_idx_override=None):
        """
        Gets the casting id from the Casting table, if it doesnt exist, inserts it then returns
        the idx.
        :param va_name: Name of VA who voiced to role.
        :param role_name: Name of role voiced.
        :param va_idx_override: Override from higher call to skip VA search.
        """
        va_idx = self.__get_va_idx(va_name) if va_idx_override is None else va_idx_override
        # Insert the role.
        try:
            role_insert_cmd = '''INSERT INTO Casting (Casting_VA_DB_id, Casting_role) VALUES (?, ?)'''
            self.exec_cmd(role_insert_cmd, (va_idx, role_name))
        # If role assigned to VA is stored catch the error thrown.
        except sqlite3.IntegrityError as e:
            pass
        query_casting_cmd = '''SELECT Casting_id FROM Casting WHERE Casting_VA_DB_id = ? AND Casting_role = ?'''
        return self.exec_cmd(query_casting_cmd, (va_idx, role_name)).fetchone()[0]

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

    # ~~~~~~~~~~~~~~~~~~Insert into Comment table functions~~~~~~~~~~~~~~~~~~
    def make_thread(self, anime_name, user_name, OP_cmnt, user_idx_override=None,
                    ani_idx_override=None):
        """
        Make a thread and return the thread id.
        :param anime_name: Name of anime to make the thread for.
        :param user_name: Name of user to make the thread for.
        :param OP_cmnt: Command to make the thread for.
        :param user_idx_override: Override from higher call to skip user search.
        :param ani_idx_override: Override from higher call to skip anime search.
        :return: Thread id (Shouldn't be None).
        """
        ani_idx = self.__get_anime_idx(anime_name) if ani_idx_override is None else ani_idx_override
        usr_idx = self.__get_user_idx(user_name) if user_idx_override is None else user_idx_override

        # Check both the anime and user exists.
        if ani_idx is None:
            print(f'handler.make_thread(): No anime with name {anime_name} found, can\'t comment on it.')
            return
        if usr_idx is None:
            print(f'handler.make_thread(): Invalid user name {user_name}, comment interrupted.')
            return
        # Make the comment.
        cmnt_idx = self.__create_comment(user_name, OP_cmnt, user_idx_override)

        # Insert the thread.
        thread_cmd = '''INSERT INTO Thread (Thread_Anime_id, Thread_Comment_DB_id) VALUES (?, ?)'''
        self.exec_cmd(thread_cmd, (ani_idx, cmnt_idx))

        # Return the thread index.
        return self.get_thread_idx(anime_name, user_name, OP_cmnt, ani_idx_override=ani_idx, user_idx_override=usr_idx)

    def get_thread_idx(self, anime_name, user_name, cmnt, ani_idx_override=None,
                       user_idx_override=None):
        ani_idx = self.__get_anime_idx(anime_name) if ani_idx_override is None else ani_idx_override
        usr_idx = self.__get_user_idx(user_name) if user_idx_override is None else user_idx_override
        cmnt_idx = self.__get_cmnt_idx(user_name, cmnt, usr_idx_override=usr_idx)
        if None not in [ani_idx, usr_idx, cmnt_idx]:
            print(f'handler.search_thread(): Can\'t search for the requested thread.')
            return None

        search_cmd = '''SELECT Thread_id FROM Thread WHERE Thread_Comment_DB_id = ?'''
        srch_idx = self.exec_cmd(search_cmd, (cmnt_idx,)).fetchone()
        return srch_idx[0] if srch_idx is not None else None

    def reply_to_thread(self, thread_id, replier_name, reply, replier_idx_override=None):
        replier_idx = self.__get_user_idx(replier_name) if replier_idx_override is None else replier_idx_override
        if replier_idx is None:
            print("handler.reply_to_thread(): Need to make an account to reply to a thread.")
            return
        # Make the comment.
        cmnt_idx = self.__create_comment(replier_name, reply, usr_idx_override=replier_idx)

        # Add reply to thread.
        reply_cmd = '''INSERT INTO Reply (Reply_Thread_id, Reply_Comment_DB_id) VALUES (?, ?)'''
        try:
            self.exec_cmd(reply_cmd, (thread_id, cmnt_idx))
        except sqlite3.IntegrityError as e:
            print("handler.reply_to_thread(): Can't reply to an invalid thread_id.\n", e)

    def __get_cmnt_idx(self, user_name, cmnt, usr_idx_override=None):
        usr_idx = self.__get_user_idx(user_name) if usr_idx_override is None else usr_idx_override
        search_cmnt_cmd = '''SELECT Comment_DB_id FROM Comment_DB WHERE Comment_DB_User_id = ? AND Comment_DB_text = ?'''
        idx = self.exec_cmd(search_cmnt_cmd, (usr_idx, cmnt)).fetchone()
        return idx[0] if idx is not None else None

    def __create_comment(self, user_name, cmnt, usr_idx_override=None):
        """
        Makes a comment and returns the comment ID.
        :param user_name: Name of the user.
        :param cmnt: Comment text.
        :param usr_idx_override: Override from higher call to skip user search.
        """
        user_idx = self.__get_user_idx(user_name) if usr_idx_override is None else usr_idx_override
        if user_idx is None:
            print(f'handler.__create_comment(): No user name {user_name}, comment interrupted.')
            return
        cmnt_cmd = '''INSERT INTO Comment_DB (Comment_DB_text, Comment_DB_User_id, Comment_DB_post_time) VALUES (?, ?, ?)'''
        self.exec_cmd(cmnt_cmd, (cmnt, user_idx, datetime.now()))
        return self.__get_cmnt_idx(user_name, cmnt, usr_idx_override=user_idx)

    # ~~~~~~~~~~~~~~~~~~Insert into Ratings table functions~~~~~~~~~~~~~~~~~~
    def give_rating(self, user_name, anime_name, rating, usr_idx_override=None, ani_idx_override=None):
        usr_idx = self.__get_user_idx(user_name) if usr_idx_override is None else usr_idx_override
        ani_idx = self.__get_anime_idx(anime_name) if ani_idx_override is None else ani_idx_override

        if usr_idx is None:
            print(f'handler.give_rating(): Need to make an account to rate the anime.')
            return
        if ani_idx is None:
            print(f'handler.give_rating(): Anime not in DB, we will update our database.')
            # Can put a log here to let admins know.
            return

        rate_cmd = '''INSERT INTO Ratings (Ratings_User_id, Ratings_Anime_id, Ratings_rating) VALUES (?, ?, ?)'''
        self.exec_cmd(rate_cmd, (usr_idx, ani_idx, rating))

    def get_anime_rating(self, anime_name):
        ani_idx = self.__get_anime_idx(anime_name)
        if ani_idx is None:
            print("Anime not in our database, we will update our database, sorry for inconvenience.")
            return
        ratings_cmd = '''SELECT Ratings_rating FROM Ratings WHERE Ratings_Anime_id = ?'''
        ratings = [row[0] for row in self.exec_cmd(ratings_cmd, (ani_idx,)).fetchall()]
        # Return the average ratings.
        return mean(ratings)

    # ~~~~~~~~~~~~~~~~~~Insert into User table functions~~~~~~~~~~~~~~~~~~
    def create_user(self, urs_tag, mail_id, pswd):
        if not self.__validate_email(mail_id):
            print("Invalid email address, please try again.")
            return
        password_hash = None
        pass

    @staticmethod
    def __validate_email(email):
        # Regular expression pattern for validating email addresses
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        # Compile the pattern
        regex = re.compile(pattern)
        # Use search method to check if the email matches the pattern
        return regex.search(email)

    def __get_user_idx(self, user_name):
        user_idx_cmd = '''SELECT User_id FROM User WHERE User_tag = ?'''
        idx = self.exec_cmd(user_idx_cmd, (user_name,)).fetchone()
        return idx[0] if idx is not None else None

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __get_anime_idx(self, anime_name):
        anime_idx_cmd = '''SELECT Anime_id FROM Anime WHERE Anime_en_name = ? OR Anime_jp_name = ?'''
        idx = self.exec_cmd(anime_idx_cmd, (anime_name, anime_name)).fetchone()
        return idx[0] if idx is not None else None

    @ staticmethod
    def show_table(cursor_out, indices=None):
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
