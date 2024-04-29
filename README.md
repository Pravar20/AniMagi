* run.py:

    Sample implementation of how to use the DB_Handler class to insert
    the anime into the database.

* handler.py:


    A handler class that will be the interface between DB and user.
    Able to insert and query whatever the driver file wants into the database.

* sqlite3_connector.py:


    A file handling the connection to the AniMagi database
    Has custom commands to create tables, allowing abbreviations.
    Create cmd: Finished. (to be tested)
    Other commands implementation TDB.

* _old_db_func.py:


    File made by @Felicity Zin used for the basis for sqlite3_connector.py
