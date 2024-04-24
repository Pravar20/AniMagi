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
            '!null':  'NOT NULL',
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
            'is !null': 'IS NOT NULL',
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
            '!exists': 'IF NOT EXISTS',
            'ref': 'REFERENCES',
            'references': 'REFERENCES',
            'unsigned': 'UNSIGNED',
            'autoincrement': 'AUTOINCREMENT',
            'autoinc': 'AUTOINCREMENT',
            '++': 'AUTOINCREMENT',
            'ck': 'CHECK',
            'check': 'CHECK',
            'between': 'BETWEEN',
            'btwn': 'BETWEEN',
        }
        # End of init.

    def exec_cmd(self, cmd, inputs=None):
        """
        Execute a SQL command in the database.
        Args:
            cmd (_str_): The sanitized command.
            inputs (_str_):  A list of input values for parameter substitution.
        """
        if inputs is None:
            self.DB_cursor.execute(cmd)
        else:
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
            if isinstance(tkn, tuple) and len(tkn) == 2:
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
                if isinstance(tkn, str):
                    return self.DB_token_map[tkn.casefold()]
                #  Otherwise just use the key as it is.
                else:
                    return self.DB_token_map[tkn]

        except TypeError as e:
            print(f"Token type {e} part of token map.")
        except KeyError as e:
            print(f"Token <{e}> isn't part of token map.")

    def valid_token(self, token):
        return token in self.DB_token_map.keys()

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
            prm_parsed = []
            # Parse the integrity key commands separately.
            if self.valid_token(prm[0]) and self.token_mapping(prm[0]) in ['FOREIGN KEY', 'PRIMARY KEY', 'CHECK']:
                for tkn in prm:
                    if isinstance(tkn, list):
                        # If valid token map it else leave it.
                        map_tkn = [self.token_mapping(t) if self.valid_token(t) else t for t in tkn]
                        prm_parsed.append('(' + ','.join(map_tkn) + ')')
                    elif self.valid_token(tkn):
                        prm_parsed.append(self.token_mapping(tkn))
                    else:
                        prm_parsed.append(tkn)
            else:
                prm_parsed = [params[0][-1] + '_' + prm[0]] + \
                        [self.token_mapping(tkn) for tkn in prm[1:]]
            
            # If it's last element then don't add a comma.
            if prm == params[-1]:
                col_cmd = col_cmd + ' '.join(prm_parsed)
            else:
                col_cmd = col_cmd + ' '.join(prm_parsed) + ', '

        # Prime the column inputs.
        create_param = create_param + ' (\n?\n)'
        inputs_lst.append(col_cmd)

        # Added specially for create cmds, since ? doesn't work for creates.
        for rep in inputs_lst:
            create_param = create_param.replace('?', rep, 1)

        # Return the param and inputs.
        return create_param
