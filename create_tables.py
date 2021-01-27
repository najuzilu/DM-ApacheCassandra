import os
import glob
import csv
import logging
from typing import Tuple
from cassandra.cluster import Cluster, Session
from sql_queries import drop_table_queries, create_table_queries


logger = logging.getLogger(__name__)

# name Keyspace
KEYSPACE = "project2"
# filename for merged data
FILENAME = "event_datafile_new.csv"


def preprocess_files(path: str) -> None:
    """
    Description: This method collects each file path, creates a new event data csv
        file called event_datafile_new that will be used to insert data into the
        Apache Cassandra tables, and iterates over each file to dump the data in
        `event_datafile_new.csv`

    Arguments:
        path (str): path to CSV files

    Returns: None
    """

    # collect each file path
    for root, dirs, files in os.walk(path):
        if "." not in root:
            file_path_list = glob.glob(os.path.join(root, "*"))

    csv.register_dialect("myDialect", quoting=csv.QUOTE_ALL, skipinitialspace=True)

    # create a new file and dump all data
    with open(FILENAME, "w", encoding="utf8", newline="") as f:
        f.truncate()
        writer = csv.writer(f, dialect="myDialect")
        writer.writerow(
            [
                "artist",
                "firstName",
                "gender",
                "itemInSession",
                "lastName",
                "length",
                "level",
                "location",
                "sessionId",
                "song",
                "userId",
            ]
        )

        # for every filepath in the file path list
        for file in file_path_list:
            # reading csv file
            with open(file, "r", encoding="utf8", newline="") as csvfile:
                # create csv reader object
                csvreader = csv.reader(csvfile)
                next(csvreader)

                # iterate over each line and dump in main csv file
                for row in csvreader:
                    if row[0] == "":
                        continue
                    writer.writerow(
                        (
                            row[0],
                            row[2],
                            row[3],
                            row[4],
                            row[5],
                            row[6],
                            row[7],
                            row[8],
                            row[12],
                            row[13],
                            row[16],
                        )
                    )
            csvfile.close()
    f.close()

    # Check to see if files have been preprocessed
    with open(FILENAME, "r", encoding="utf8") as f:
        csvreader = csv.reader(f)
        next(csvreader)
        row_count = sum(1 for row in csvreader)
        print(f"Total number of rows in `{FILENAME}` is", row_count)
    f.close()


def connect_to_cassandra() -> Tuple[Cluster, Session]:
    """
    Description: This method will connect to a Cassandra instance,
        create and set a keyspace, and will return a session to this
        connection

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

    # create a keyspace
    query = (
        """CREATE KEYSPACE IF NOT EXISTS """
        + KEYSPACE
        + """ WITH REPLICATION = { 'class' :
        'SimpleStrategy', 'replication_factor': 1}"""
    )
    try:
        session.execute(query)
    except Exception as e:
        msg = "ERROR: Could not create KeySpace"
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


def drop_tables(session: Session) -> None:
    """
    Description: This method drops the following tables if they exist:
        `artist_song_session`, `song_playlist_session`, and `user_by_song`

    Arguments:
        session (Session): session connection to Apache Cassandra cluster

    Returns:
        None
    """
    for query in drop_table_queries:
        try:
            session.execute(query)
        except Exception as e:
            msg = f"ERROR: Could not drop table with query: {query}"
            logger.warning(msg, e)
            continue


def create_tables(session: Session) -> None:
    """
    Description: This method will create the following tables:
        `artist_song_session`, `song_playlist_session`, and `user_by_song`

    Arguments:
        session (Session): session connection to Apache Cassandra cluster

    Returns:
        None
    """
    for query in create_table_queries:
        try:
            session.execute(query)
        except Exception as e:
            msg = f"ERROR: Could not create table with query: {query}"
            logger.warning(msg, e)
            continue


def main() -> None:
    """
    Description: This method preprocessed the data and established
        a connection to an Apache Cassandra cluster and session

    Returns:
        None
    """
    # Get your current folder and subfolder event data
    filepath = os.getcwd() + "/event_data"
    preprocess_files(filepath)

    # establish connection to Cassandra
    cluster, session = connect_to_cassandra()
    if session:
        # drop tables if they exists already
        drop_tables(session)

        # create tables
        create_tables(session)

    session.shutdown()
    cluster.shutdown()


if __name__ == "__main__":
    main()
