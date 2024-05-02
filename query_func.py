import _sqlite3 as sqlite3

connector = sqlite3.connect('animagi.db')
c = connector.cursor()
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
        c.execute('''UPDATE ANIME SET cast_id = ? WHERE anime_id = ?''', (data, anime_id))
    else:
        print('Invalid data type')

def fetch_anime_by_name(anime_name):

    c.execute('SELECT * FROM ANIME WHERE anime_name = ?', (anime_name,))
    
    anime_found = c.fetchone()
    if anime_found:
        return anime_found
    else:
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
        c.execute('''UPDATE USER SET user_password = ? WHERE user_id = ?''', (data, user_id))
    else:
        print('Invalid data type')

# pass table's name with filters as list of tuples
def find_with_filters(table_name, filters):
    query = " WHERE " + " AND ".join([f"{filter[0]} = ?" for filter in filters])    
    return f"SELECT * FROM {table_name} {query}"

# return all the columns that interact with both tables that has the specific ID
# L_shared_column = the name of the column in the left table that is shared with the left table
# Right table = the table that data will be return from
# R_shared_column = the name of the column in the right table that is shared with the left table
# R_table_ID = the name of column from Right table that has ID
# specific_ID the specific ID of the item we want to find
def find_data_from_another_table(L_table, R_table, L_shared_columns, R_shared_column, R_table_ID, specific_ID):
    return f"SELECT * FROM {R_table} LEFT JOIN {L_table} ON {L_table}.{L_shared_columns} = {R_table}.{R_shared_column}
     WHERE {R_table}.{R_table_ID} = {specific_ID}"

def show_table(cursor, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def clear_table(table_name):
    table = table_name.upper()
    return f"DELETE FROM {table_name}"

def find_VA_id(VA_name):
    return "SELECT id FROM VA_DB WHERE name = ?"

# 4. Search for the anime's done a Voice Actor.
def find_anime_by_voice_actor(actor_id):
    query = f"SELECT ANIME.* FROM ANIME INNER JOIN CAST ON ANIME.cast_id = CAST.cast_id WHERE CAST.actor_id = ?"
    # c.execute(query, (actor_id,))

def find_studio_id(studio_name):
    return "SELECT id FROM Studio_DB WHERE name = ?"

# 5. Search for anime's that was produced by a certain studio.
def find_anime_by_studio(studio_id):
    return f"SELECT * FROM ANIME WHERE studio_id = ?"
    # c.execute(query, (studio_id,))

