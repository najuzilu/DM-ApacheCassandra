from create_tables import FILENAME
from pandas.core.frame import DataFrame
import pandas as pd
import logging
import warnings
from pandas.core.common import SettingWithCopyWarning

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
logger = logging.getLogger(__name__)


def stylized_facts_tbl1(df: DataFrame) -> None:
    """
    Description: This method calculates basic stats for
        determining which field should be used as a partition
        key when designing the data model for the `artist_song_session`
        table

    Arguments:
        df (DataFrame): DataFrame object loading data from
            `event_datafile_new.csv`

    Returns:
        None
    """
    sessionId_unique = len(df["sessionId"].unique())
    sessionId_count = df.groupby("sessionId")["artist"].count()
    sessionId_mean = sessionId_count.mean()
    itemInSession_unique = len(df["itemInSession"].unique())
    itemInSession_count = df.groupby("itemInSession")["artist"].count()
    itemInSession_mean = itemInSession_count.mean()
    print("\n==================== INFO artist_song_session TABLE ====================")
    print(f"There are a total of {df.shape[0]} observations.")
    print(f"There are {sessionId_unique} unique `sessionId` values", end=" ")
    print(f"with an average of {sessionId_mean} values per sessionId.")
    print(f"There are {itemInSession_unique} unique `itemInSession`", end=" ")
    print(f"values with an average of {itemInSession_mean} values per itemInSession.\n")


def process_data() -> None:
    """
    Description: This method reads in data from `event_datafile_new.csv`
        and calls on methods which generate simple stats for `artist_song_session`

    Returns:
        None
    """
    try:
        df = pd.read_csv(FILENAME)
    except Exception as e:
        msg = "ERROR: Issue loading data from CSV file"
        logger.warning(msg, e)
        return

    # Let's look at the first table, `artist_song_session`
    stylized_facts_tbl1(
        df[["artist", "song", "length", "sessionId", "itemInSession"]]
    )


if __name__ == "__main__":
    process_data()
