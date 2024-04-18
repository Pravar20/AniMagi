* sqlite3_connector.py:


    A file handling the connection to the AniMagi database
    Has custom commands to create tables, allowing abbreviations.
    Create cmd: Finished. (to be tested)
    Other commands implementation TDB.

* handler.py:


    A handler class that will be the interface between DB and user.
    Unfinished.
    FIRST_CREATE function has the create statements
    to make the database for the first time. 
    (Refer to the implementations for knowing the type
    of data required for storing an anime, user, comment, rating)

* \icons:


    A directory to hold all the pictures/icons used in the database.
        * \icons\Anime
        * \icons\User
        * \icons\VA

* db_func.py:


    File made by @Felicity Zin used for the basis for sqlite3_connector.py
