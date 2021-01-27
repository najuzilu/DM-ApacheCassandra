import pandas as pd
import logging
from typing import Tuple
from cassandra.cluster import Cluster, Session
from pandas.core.frame import DataFrame
from create_tables import KEYSPACE, FILENAME
from create_tables import drop_tables
from sql_queries import artist_song_sess_query, song_playlist_sess_query, user_by_song_query
from sql_queries import artist_song_sess_insert, song_playlist_sess_insert, user_by_song_insert


logger = logging.getLogger(__name__)


def connect() -> Tuple[Cluster, Session]:
    """
    Description: This method will connect to a Cassandra instance and
        set the keyspace

    Returns:
        Optional[Tuple[cassandra.cluster.Session], None]: Session to the
        connection to Cassandra. If method terminates prior to full
        execution, it will return `None`
    """
    # connect to Cassandra instance
    try:
        cluster = Cluster(["127.0.0.1"])
    except Exception as e:
        msg = """ERROR: Cannot make a connection to a Cassandra instance
            on your local machine"""
        logger.warning(msg, e)
        return

    # connect to a session to establish connection
    try:
        session = cluster.connect()
    except Exception as e:
        msg = """ERROR: Cannot connect to a session to begin executing
            queries"""
        logger.warning(msg, e)
        return

    # set Keyspace
    try:
        session.set_keyspace(KEYSPACE)
    except Exception as e:
        msg = "ERROR: Could not set Keyspace"
        logger.warning(msg, e)
        return

    return (cluster, session)


def process(session: Session, df: DataFrame) -> None:
    """
    Description: This method iterates over each row of
        `event_datafile_new.csv` and inserts the appropriate
        rows into corresponding Apache Cassandra tables

    Arguments:
        session (Session): session connection to Apache Cassandra cluster
        df (DataFrame): DataFrame object loading data from
            `event_datafile_new.csv`

    Returns:
        None
    """
    # iterate over row and insert in each table
    for index, row in df.iterrows():
        # extract table 1 data
        try:
            tbl1_data = (
                row["itemInSession"],
                row["sessionId"],
                row["artist"],
                row["song"],
                row["length"]
            )
        except Exception as e:
            msg = "ERROR: Could not extract table 1 data from chunk"
            print(msg, e)
            continue

        # insert extracted data into artist_song_session
        try:
            session.execute(artist_song_sess_insert, tbl1_data)
        except Exception as e:
            msg = "ERROR: Could not insert table 1 data into artist_song_session"
            print(msg, e)
            continue

        # extract table 2 data
        try:
            tbl2_data = (
                row["userId"],
                row["sessionId"],
                row["itemInSession"],
                row["firstName"],
                row["lastName"],
                row["artist"],
                row["song"]
            )
        except Exception as e:
            msg = "ERROR: Could not extract table 2 data from chunk"
            print(msg, e)
            continue

        # insert extracted data into song_playlist_session
        try:
            session.execute(song_playlist_sess_insert, tbl2_data)
        except Exception as e:
            msg = "ERROR: Could not insert table 2 data into song_playlist_session"
            print(msg, e)
            continue

        # extract table 3 data
        try:
            tbl3_data = (row["song"], row["userId"], row["firstName"], row["lastName"])
        except Exception as e:
            msg = "ERROR: Could not extract table 3 data from chunk"
            print(msg, e)
            continue

        # insert extracted data into user_by_song
        try:
            session.execute(user_by_song_insert, tbl3_data)
        except Exception as e:
            msg = "ERROR: Could not insert table 3 data into user_by_song"
            print(msg, e)
            continue


def process_data(session: Session) -> None:
    """
    Description: This method reads in chunks of data
        from `event_datafile_new.csv` and calls on
        method to process each chunk

    Arguments:
        session (Session): session connection to Apache Cassandra cluster

    Returns:
        None
    """
    chunksize = 10 ** 6
    for chunk in pd.read_csv(FILENAME, chunksize=chunksize):
        try:
            process(session, chunk)
        except Exception as e:
            msg = "ERROR: Issue processing chunk"
            print(msg, e)
            return


def run_queries(session: Session) -> None:
    """
    Description: This method runs queries to answer the
        following questions:

        1. Give me the artist, song title and song's length
        in the music app history that was heard during
        `sessionId = 338`, and `itemInSession = 4`.
        2. Give me only the following: name of artist, song
        (sorted by itemInSession) and user (first and last name)
        for `userId = 10`, `sessionId = 182`.
        3. Give me every user name (first and last) in my music
        app history who listened to the song 'All Hands Against
        His Own'.

    Arguments:
        session (Session): session connection to Apache Cassandra cluster

    Returns:
        None
    """
    try:
        rows = session.execute(artist_song_sess_query)
    except Exception as e:
        msg = f"ERROR: Could not query: {artist_song_sess_query}"
        print(msg, e)
        return

    print("\n==================== QUERY 1 ====================")
    print("Query the artist, song title and song's length in the music")
    print("app history that was heard during  sessionId = 338, and")
    print("itemInSession  = 4:\n")
    for row in rows:
        print(row)
    print("\n")

    try:
        rows = session.execute(song_playlist_sess_query)
    except Exception as e:
        msg = f"ERROR: Could not query: {song_playlist_sess_query}"
        print(msg, e)
        return

    print("==================== QUERY 2 ====================")
    print("Query only the following: name of artist, song (sorted by itemInSession)")
    print("and user (first and last name) for `userId = 10` and `sessionId = 182:\n`")
    for row in rows:
        print(row)
    print("\n")

    try:
        rows = session.execute(user_by_song_query)
    except Exception as e:
        msg = f"ERROR: Could not query: {user_by_song_query}"
        print(msg, e)
        return

    print("\n==================== QUERY 3 ====================")
    print("Query every user name (first and last) in my music app history")
    print("who listened to the song 'All Hands Against His Own'\n")
    for row in rows:
        print(row)
    print("\n")


def main() -> None:
    """
    Description: Calls on all main methods. First, established
        connection to Apache Cassandra cluster, processes the data,
        prints results to three queries, and lastly drops the tables

    Returns:
        None
    """

    cluster, session = connect()

    if session:
        # process data
        process_data(session)

        # prints answers to three queries
        run_queries(session)

        # drop tables
        drop_tables(session)

    session.shutdown()
    cluster.shutdown()


if __name__ == "__main__":
    main()
