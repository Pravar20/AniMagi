from handler import DB_Handler, Anime
from datetime import date


DB_name = 'animagi.db'
request_string = 'Enter your choice: '


def print_options():
    f = f"""
    You are connected to '{DB_name}'.
    ************************************************************************************************
    You can perform any of the following actions by typing the command number or 'quit'.
        1. Search for an anime and display it on screen.
        2. View an anime's comment section.
        3. Search for anime's of a certain genre.
        4. Search for the anime's done a Voice Actor.
        5. Search for anime's that was produced by a certain studio.
        6. Display top 10 anime rankings.
    ************************************************************************************************
    """
    print(f)


def display_anime(DB):
    print(
        """
        Choice: 1. Search for an anime and display it on screen.
        Please insert anime to find:
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
    )
    anime_name = input(request_string)
    anime_idx = DB.get_anime_idx(anime_name)
    anime_cmd = '''
    SELECT
        Anime_en_name, Anime_jp_name, Anime_icon, Anime_aired, Anime_episodes 
    FROM Anime WHERE Anime_id = ?'''

    anime_genre_cmd = ''' 
    SELECT G.Genre_DB_name FROM 
    (
        SELECT Genre_DB.Genre_DB_name
        FROM
            Genre
            INNER JOIN Genre_DB
            WHERE Genre_Anime_id = ?
    ) G'''

    anime_out = DB.exec_cmd(anime_cmd, (anime_idx,))
    genre_out = DB.exec_cmd(anime_genre_cmd, (anime_idx,))
    DB.show_table(anime_out)
    DB.show_table(genre_out)


if __name__ == '__main__':
    db_handle = DB_Handler(DB_name=DB_name)
    user_exit = False
    while user_exit is False:
        print_options()
        u_input = input(request_string)
        if u_input in ['1', '2', '3', '4', '5', '6']:
            # Run respective functions
            match int(u_input):
                case 1:
                    display_anime(db_handle)
                    break
                case 2:
                    break
                case 3:
                    break
                case 4:
                    break
                case 5:
                    break
                case 6:
                    break
                case _:
                    break

        elif u_input in ['quit', 'q']:
            user_exit = True
        else:
            print('Invalid input, please only insert valid inserts')
