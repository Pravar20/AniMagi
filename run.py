from handler import DB_Handler, Anime
from datetime import date


db_handle = DB_Handler()
# db_handle.sample_data_insert()
print("AOT rating:", db_handle.get_anime_rating('Attack on Titan'))

<<<<<<< HEAD
# Add type hint.
anime_aot: Anime
anime_aot = {
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
anime_naruto: Anime
anime_naruto = {
    'en_name': 'Naruto', 'jp_name': 'Naruto',
    'aired': date(2002, 10, 3),
    'episodes': 220, 'anime_icon': 'https://cdn.myanimelist.net/images/anime/13/17405.jpg',
    'genres': ['Action', 'Adventure', 'Comedy', 'Super Power'],
    'studios': ['Studio Pierrot'],
    'roles': [
        ('Takeuchi, Junko', 'Uzumaki, Naruto'),
        ('Inoue, Kazuhiko', 'Hatake, Kakashi'),
        ('Nakamura, Chie', 'Haruno, Sakura'),
        ('Sugiyama, Noriaki', 'Uchiha, Sasuke'),
    ]
}
anime_fma: Anime
anime_fma = {
    'en_name': 'Fullmetal Alchemist: Brotherhood', 'jp_name': 'Hagane no Renkinjutsushi: Fullmetal Alchemist',
    'aired': date(2009, 4, 5),
    'episodes': 64, 'anime_icon': 'https://cdn.myanimelist.net/images/anime/1223/96541.jpg',
    'genres': ['Action', 'Military', 'Adventure', 'Drama', 'Magic', 'Fantasy'],
    'studios': ['Bones'],
    'roles': [
        ('Paku, Romi', 'Elric, Edward'),
        ('Kugimiya, Rie', 'Elric, Alphonse'),
        ('Miki, Shinichiro', 'Mustang, Roy'),
        ('Han, Keiko', 'Hawkeye, Riza'),
    ]
}

anime_jjk: Anime
anime_jjk = {
    'en_name': 'Jujutsu Kaisen', 'jp_name': 'Jujutsu Kaisen',
    'aired': date(2020, 10, 3),
    'episodes': 24, 'anime_icon': 'https://cdn.myanimelist.net/images/anime/6/109302.jpg',
    'genres': ['Action', 'Horror', 'Supernatural', 'Mystery', 'School', 'Shounen'],
    'studios': ['MAPPA'],
    'roles': [
        ('Enoki, Junya', 'Itadori, Yuuji'),
        ('Uchida, Yuuma', 'Fushiguro, Megumi'),
        ('Seto, Asami', 'Kugisaki, Nobara'),
        ('Nakamura, Yuichi', 'Gojou, Satoru'),
        ('Hanae, Natsuki', 'Zenin, Maki'),
        ('Kaji, Yuuki', 'Inumaki, Toge'),
        ('Okitsu, Kazuyuki', 'Nanami, Kento'),
        ('Ishida, Akira', 'Getou, Suguru'),
    ]
}

db_handle.insert_anime(anime_aot)
db_handle.insert_anime(anime_naruto)
db_handle.insert_anime(anime_fma)
db_handle.insert_anime(anime_jjk)

view_tbl_cmd = '''SELECT * FROM Anime'''
cmd_out = db_handle.exec_cmd(view_tbl_cmd)
db_handle.show_table(cmd_out, [cmd_out.description[0][0]])
=======
# view_tbl_cmd = '''SELECT * FROM Casting'''
# cmd_out = db_handle.exec_cmd(view_tbl_cmd)
# db_handle.show_table(cmd_out, ['Casting_id', 'Casting_VA_DB_id'])
>>>>>>> c9e8cd1008c8157758a85b155570dae66c006b16
