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
    c.execute('''INSERT INTO ANIME(anime_name, anime_rating, anime_aired, studio_id, cast_id) ''', (anime_name, anime_rating, anime_aired, studio_id, cast_id))

# remove data from anime table
def remove_anime(anime_id):
    c.execute('''DELETE FROM ANIME WHERE anime_id = ?''', (anime_id,))

    
connector.commit()
connector.close()

