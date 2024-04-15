"""
File incomplete: need to implement create foreign key things.
"""

import _sqlite3 as sqlite3
import datetime

DEFAULT_DB = 'animagi.db'


class Animagi_DB:
    def __init__(self, DB_name=DEFAULT_DB):
        """
        Constructor for database connection.
        Args:
            DB_name (_str_): String name for  the database file to be created/connected with. Default is "animagi.db".
        """
        self.DB_name = DB_name
        self.DB_connection = sqlite3.connect(DB_name)
        self.DB_cursor = self.DB_connection.cursor()
        self.DB_token_map = {
            int: 'INTEGER',
            float: 'REAL',
            str:  'TEXT',
            (str): (lambda n: f"VARCHAR({n})"),
            bytes: 'BLOB',
            datetime: 'DATETIME',
            'null': 'NULL',
            'not null': 'NOT NULL',
            'nnull':  'NOT NULL',
            'add': 'ADD',
            'and': 'AND',
            'as': 'AS',
            'asc': 'ASC',
            'ascending': 'ASC',
            'create': 'CREATE',
            'table': 'TABLE',
            'tbl': 'TABLE',
            'view': 'VIEW',
            'default': 'DEFAULT',
            'delete': 'DELETE',
            'del': 'DELETE',
            'desc': 'DESC',
            'descending': 'DESC',
            'exists': 'EXISTS',
            'pk': 'PRIMARY KEY',
            'primary key': 'PRIMARY KEY',
            'fk': 'FOREIGN KEY',
            'foreign key': 'FOREIGN KEY',
            'from': 'FROM',
            'group by': 'GROUP BY',
            'having': 'HAVING',
            'in': 'IN',
            'inner join': 'INNER JOIN',
            'insert into': 'INSERT INTO',
            'is null':  'IS NULL',
            'is not null': 'IS NOT NULL',
            'join': 'JOIN',
            'or': 'OR',
            'order by': 'ORDER BY',
            'outer join': 'OUTER JOIN',
            'select': 'SELECT',
            'unique': 'UNIQUE',
            'values': 'VALUES',
            'where': 'WHERE',
            'union': 'UNION',
            'if not': 'IF NOT',
            'if': 'IF',
            '!exists': 'IF NOT EXISTS'
        }

    def exec_cmd(self, cmd, inputs=None):
        """
        Execute a SQL command in the database.
        Args:
            cmd (_str_): The sanitized command.
            inputs (_str_):  A list of input values for parameter substitution.
        """
        self.DB_cursor.execute(cmd, inputs)

    def token_mapping(self, tkn):
        """
        Map the tokens from python to sql syntax.
        Args:
            tkn (_any_): Can be strings, types, or other objects that need mapping.

        Returns:
            _str_: strings validated for sql syntax
        """
        try:
            # If token is a tuple parse and return correct value.
            if type(tkn) == tuple and len(tkn) == 2:
                # If the call value is invalid return none.
                call_val = tkn[-1]
                if not isinstance(call_val, int):
                    print(f"Token type has invalid value type.")
                    return None
                # If valid return using lambda fn.
                else:
                    return self.DB_token_map[(tkn[0])](call_val)
            # Return normal tokens.
            else:
                # For a string type allow case-insensitive matching of keys.
                if type(tkn) == str:
                    return self.DB_token_map[tkn.casefold()]
                #  Otherwise just use the key as it is.
                else:
                    return self.DB_token_map[tkn]

        except TypeError as e:
            print(f"Token type {e} part of token map.")
        except KeyError as e:
            print(f"Token <{e}> isn't part of token map.")

    def commit(self):
        """
        Commit changes to the database.
        """
        self.DB_connection.commit()

    def __del__(self):
        """
        Destructor that closes the connection with the database when the object is deleted.
        """
        self.commit()
        self.DB_connection.close()

    def get_create_tbl_cmd(self, params: list):
        """
        Create SQL command for creating table in sqlite3 form.
        Args:
            params (list): list of params sample form:
            [
                ['create', 'table', '!exists', 'tbl_nm'],
                ['col_nm1', int, 'nnull', 'pk'],
                ['col_nm2', str, 'nnull'],
                ['col_nm3', int]
            ]

        Returns:
            str: Create cmd with ? in places to be replaced by values by execute command.
            list: List of the inputs for respective ? is create cmd.
        """
        # Set the table name.
        create_param = ""
        inputs_lst = []

        # Parse the create command.
        for crt_cmd in params[0][:-1]:
            create_param = create_param + self.token_mapping(crt_cmd) + ' '
        # Table name primed.
        create_param += '?'
        inputs_lst.append(params[0][-1])

        # Parse and validate parameters for cmd.
        col_cmd = ''
        for prm in params[1:]:
            prm = [
                params[0][-1] + '_' + prm[0]] + \
                [self.token_mapping(tkn) for tkn in prm[1:]
            ]
            col_cmd = col_cmd + ' '.join(prm) + ','

        # Prime the column inputs.
        create_param = create_param + ' (?)'
        inputs_lst.append(col_cmd)

        # Return the param and inputs.
        return create_param, inputs_lst


# # setting up Database
# def create_table():
    
#     # anime table
#     c.execute('''CREATE TABLE IF NOT EXISTS ANIME(
#               anime_id INTEGER PRIMARY KEY,
#               anime_name TEXT NOT NULL,
#               anime_rating INTEGER,
#               anime_aired DATE,
#               studio_id INTEGER,
#               cast_id INTEGER
#     )''')
#     # user account table
#     c.execute('''CREATE TABLE IF NOT EXISTS USER(
#               user_id INTEGER PRIMARY KEY,
#               user_tag TEXT NOT NULL,
#               user_email TEXT NOT NULL,
#               user_ph_no TEXT,
#               user_password TEXT NOT NULL
#     )''')
#     # rating table
#     c.execute('''CREATE TABLE IF NOT EXISTS RATING(
#               rating_id INTEGER PRIMARY KEY,
#               anime_id INTEGER,
#               user_id INTEGER,
#               rating INTEGER
#     )''')
#     # production studio table
#     c.execute('''CREATE TABLE IF NOT EXISTS STUDIO(
#               studio_id INTEGER PRIMARY KEY,
#               studio_name TEXT NOT NULL,
#               anime_id INTEGER,
#               cast_id INTEGER,
#               cast_storage TEXT
#     )''')

# # insert data into anime table
# def insert_anime(anime_name, anime_rating, anime_aired, studio_id, cast_id):
#     c.execute('''
#         INSERT INTO ANIME (anime_name, anime_rating, anime_aired, studio_id, cast_id)
#         VALUES (?, ?, ?, ?, ?)
#     ''', (anime_name, anime_rating, anime_aired, studio_id, cast_id))

# # remove data from anime table
# def remove_anime(anime_id):
#     c.execute('''DELETE FROM ANIME WHERE anime_id = ?''', (anime_id,))

# # update data in anime table
# def update_anime(anime_id, update_data_type, data):
#     if update_data_type == 'anime_name':
#         c.execute('''UPDATE ANIME SET anime_name = ? WHERE anime_id = ?''', (data, anime_id))
#     elif update_data_type == 'anime_rating':
#         c.execute('''UPDATE ANIME SET anime_rating = ? WHERE anime_id = ?''', (data, anime_id))
#     elif update_data_type == 'anime_aired':
#         c.execute('''UPDATE ANIME SET anime_aired = ? WHERE anime_id = ?''', (data, anime_id))
#     elif update_data_type == 'studio_id':
#         c.execute('''UPDATE ANIME SET studio_id = ? WHERE anime_id = ?''', (data, anime_id))
#     elif update_data_type == 'cast_id':
#         c.execute('''UPDATE ANIME SET cast_id = ? WHERE anime_id = ?''', (data, anime_id))
#     else:
#         print('Invalid data type')

# def fetch_anime_by_name(anime_name):

#     c.execute('SELECT * FROM ANIME WHERE anime_name = ?', (anime_name,))
    
#     anime_found = c.fetchone()
#     if anime_found:
#         return anime_found
#     else:
#         print(f"No anime found with anime_id: {anime_name}")

# # insert data into user table
# def insert_user_data(user_tag, user_email, user_ph_no, user_password):
#     c.execute('''
#         INSERT INTO USER (user_tag, user_email, user_ph_no, user_password)
#         VALUES (?, ?, ?, ?)
#     ''', (user_tag, user_email, user_ph_no, user_password))

# # remove data from user table
# def remove_user_data(user_id):
#     c.execute('''DELETE FROM USER WHERE user_id = ?''', (user_id,))

# # update data in user table
# def update_user_data(user_id, update_data_type, data):
#     if update_data_type == 'user_tag':
#         c.execute('''UPDATE USER SET user_tag = ? WHERE user_id = ?''', (data, user_id))
#     elif update_data_type == 'user_email':
#         c.execute('''UPDATE USER SET user_email = ? WHERE user_id = ?''', (data, user_id))
#     elif update_data_type == 'user_ph_no':
#         c.execute('''UPDATE USER SET user_ph_no = ? WHERE user_id = ?''', (data, user_id))
#     elif update_data_type == 'user_password':
#         c.execute('''UPDATE USER SET user_password = ? WHERE user_id = ?''', (data, user_id))
#     else:
#         print('Invalid data type')

# def clear_table(table_name):
#     table = table_name.upper()
#     query = f"DELETE FROM {table_name}"
#     c.execute(query)

db = Animagi_DB()

#     c.execute('''CREATE TABLE IF NOT EXISTS ANIME(
#               anime_id INTEGER PRIMARY KEY,
#               anime_name TEXT NOT NULL,
#               anime_rating INTEGER,
#               anime_aired DATE,
#               studio_id INTEGER,
#               cast_id INTEGER
#     )''')

cr_tb = [
    ['create', 'table', '!exists', 'Anime'],
    ['id', int, 'nnull', 'pk'],
    ['name', (str, 20), 'nnull'],
    ['rating', int],
    ['aired', datetime],
]

sc_str, inp = db.get_create_tbl_cmd(cr_tb)
print(sc_str)
print(inp)
