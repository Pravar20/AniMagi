import _sqlite3 as sqlite3

connector = sqlite3.connect('animagi.db')
# setting up Database
def create_table():
    
    c = connector.cursor()
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

    # rating table

    # production studio table

connector.commit()
connector.close()

