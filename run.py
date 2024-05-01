from handler import DB_Handler, Anime
from datetime import date
from IPython.display import display
import pandas as pd


DB_name = 'animagi.db'
request_string = 'Enter your choice: '


def print_options():
    f = f"""
    You are connected to '{DB_name}'.
    ************************************************************************************************
    You can perform any of the following actions by typing the command number or 'quit'.
        1. Search for an anime and display it on screen.
        2. Display an anime's comment section.
        3. Search for anime's of a certain genre.
        4. Search for the anime's done a Voice Actor.
        5. Search for anime's that was produced by a certain studio.
        6. Display top 10 anime rankings.
    ************************************************************************************************
    """
    print(f)


def add_list_to_table(tbl, list_as_tbl):
    list_as_tbl = list_as_tbl.to_dict(orient='list')
    # print(list_as_tbl)
    for ky in list_as_tbl.keys():
        tbl.insert(tbl.size, ky, ['; '.join(list_as_tbl[ky])])
    return tbl


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
    if anime_idx is None:
        print('Anime name not found!')
        return

    anime_cmd = '''SELECT Anime_en_name, Anime_jp_name, Anime_icon, Anime_aired, Anime_episodes FROM Anime WHERE Anime_id = ?'''

    anime_genre_cmd = '''SELECT Genre_DB.Genre_DB_name FROM 
                    Genre INNER JOIN Genre_DB ON Genre.Genre_Genre_DB_id = Genre_DB.Genre_DB_id
                    WHERE Genre.Genre_Anime_id = ?'''

    anime_studio_cmd = '''SELECT Studio_DB.Studio_DB_name FROM 
                    Studio INNER JOIN Studio_DB ON Studio.Studio_Studio_DB_id = Studio_DB.Studio_DB_id
                    WHERE Studio.Studio_Anime_id = ?'''

    anime_cast_cmd = '''SELECT VA_DB_name, Casting_role FROM
                    Cast INNER JOIN Casting ON Cast_Casting_id = Casting_id
                    INNER JOIN VA_DB ON VA_DB_id = Casting_VA_DB_id
                    WHERE Cast_Anime_id = ?'''

    anime_out = DB.exec_cmd(anime_cmd, (anime_idx,))
    anime_out = DB.get_table(anime_out, ['Anime_en_name', 'Anime_jp_name'])

    # Get the genres and add to anime_table.
    genre_out = DB.exec_cmd(anime_genre_cmd, (anime_idx,))
    genre_out = DB.get_table(genre_out)

    # Get studio and add to table.
    studio_out = DB.exec_cmd(anime_studio_cmd, (anime_idx,))
    studio_out = DB.get_table(studio_out)

    cast_out = DB.exec_cmd(anime_cast_cmd, (anime_idx,))
    cast_out = DB.get_table(cast_out)
    cast_out = [': '.join(val) for val in cast_out.values]
    cast_out = pd.DataFrame(cast_out, columns=['Voice Actors & Characters'])

    anime_out = add_list_to_table(anime_out, genre_out)
    anime_out = add_list_to_table(anime_out, studio_out)
    anime_out = add_list_to_table(anime_out, cast_out)

    pd.set_option('display.max_colwidth', 320)
    display(anime_out)


def view_comment_section(DB):
    print(
        """
        Choice: 2. Display an anime's comment section.
        Please insert anime to find:
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
    )
    anime_name = input(request_string)
    anime_idx = DB.get_anime_idx(anime_name)
    if anime_idx is None:
        print('Anime name not found!')
        return

    thread_cmd = '''SELECT Thread_id, User_tag, Comment_DB_post_time, Comment_DB_text FROM Thread
                    INNER JOIN Comment_DB ON Thread_Comment_DB_id = Comment_DB.Comment_DB_id
                    INNER JOIN User ON Comment_DB_User_id = User_id
                    WHERE Thread_Anime_id = ?'''
    thread = DB.exec_cmd(thread_cmd, (anime_idx,))
    thread = DB.get_table(thread, ['Thread_id'])

    reply_cmd = '''SELECT User_tag, Comment_DB_post_time, Comment_DB_text FROM Reply
                    INNER JOIN Comment_DB ON Reply_Comment_DB_id = Comment_DB_id
                    INNER JOIN User ON Comment_DB_User_id = User_id
                    WHERE Reply_Thread_id = ?'''

    for t_id, t_out in thread.iterrows():
        display(t_out.values)
        reply_out = DB.exec_cmd(reply_cmd, (t_id,))
        reply_out = DB.get_table(reply_out)
        for reply in reply_out.values:
            display('\t\t', reply)
        print('________________________________')


def demo():
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
                case 2:
                    view_comment_section(db_handle)
                    pass
                case 3:
                    pass
                case 4:
                    pass
                case 5:
                    pass
                case 6:
                    pass
        elif u_input in ['quit', 'q']:
            user_exit = True
        else:
            print('Invalid input, please only insert valid inserts')


# demo()
