# DROP TABLES

artist_song_sess_drop = "DROP TABLE IF EXISTS artist_song_session;"
song_playlist_sess_drop = "DROP TABLE IF EXISTS song_playlist_session;"
user_by_song_drop = "DROP TABLE IF EXISTS user_by_song;"


# CREATE TABLES

artist_song_sess_create = """CREATE TABLE IF NOT EXISTS artist_song_session ( \
    item_in_session INT, session_id INT, artist TEXT, \
    title TEXT, length FLOAT, PRIMARY KEY( \
    item_in_session, session_id));"""

song_playlist_sess_create = """CREATE TABLE IF NOT EXISTS song_playlist_session ( \
    user_id INT, session_id INT, item_in_session INT, first_name TEXT, \
    last_name TEXT, artist TEXT, title TEXT, \
    PRIMARY KEY((user_id, session_id), item_in_session));"""

user_by_song_create = """CREATE TABLE IF NOT EXISTS user_by_song ( \
    title TEXT, user_id INT, first_name TEXT, last_name TEXT, \
    PRIMARY KEY(title, user_id));"""


# INSERT RECORDS

artist_song_sess_insert = """INSERT INTO artist_song_session (item_in_session, session_id,\
    artist, title, length) VALUES (%s, %s, %s, %s, %s);"""

song_playlist_sess_insert = """INSERT INTO song_playlist_session ( \
    user_id, session_id, item_in_session, first_name, \
    last_name, artist, title) VALUES (%s, %s, %s, %s, %s, %s, %s);"""

user_by_song_insert = """INSERT INTO user_by_song (title, user_id, first_name, last_name) VALUES \
    (%s, %s, %s, %s);"""

# QUERIES!

artist_song_sess_query = """SELECT artist, title, length FROM artist_song_session WHERE \
    session_id=338 AND item_in_session=4;"""

song_playlist_sess_query = """SELECT artist, title, first_name, last_name FROM \
    song_playlist_session WHERE user_id=10 AND session_id = 182;"""

user_by_song_query = """SELECT first_name, last_name FROM user_by_song WHERE \
    title='All Hands Against His Own';"""


# query lists
create_table_queries = [artist_song_sess_create, song_playlist_sess_create, user_by_song_create]

drop_table_queries = [artist_song_sess_drop, song_playlist_sess_drop, user_by_song_drop]
