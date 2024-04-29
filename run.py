from handler import DB_Handler, Anime
from datetime import date

db_handle = DB_Handler()

# Add type hint.
anime_dict: Anime
anime_dict = {
    'en_name': 'Attack on Titan', 'jp_name': 'Shingeki no Kyojin',
    'aired': date(2013, 4, 7),
    'episodes': 25, 'anime_icon': 'https://cdn.myanimelist.net/images/anime/10/47347.jpg',
    'genres': ['Action', 'Award Winning', 'Drama', 'Suspense'], 'studios': ['Wit Studio'],
    'roles': [
        ('Kaji, Yuuki', 'Yeager, Eren'),
        ('Ishikawa, Yui', 'Ackerman, Mikasa'),
        ('Inoue, Marina', 'Arlert, Armin'),
        ('Kamiya, Hiroshi', 'Levi'),
        ('Ono, Daisuke', 'Smith, Erwin'),
        ('Park, Romi', 'Zoë, Hange'),
        ('Kobayashi, Yuu', 'Blouse, Sasha'),
        ('Shimamura, Yuu', 'Leonhart, Annie'),
    ]
}
db_handle.insert_anime(anime_dict)

# view_tbl_cmd = '''SELECT * FROM Casting'''
# cmd_out = db_handle.exec_cmd(view_tbl_cmd)
# db_handle.show_table(cmd_out, ['Casting_id', 'Casting_VA_DB_id'])
