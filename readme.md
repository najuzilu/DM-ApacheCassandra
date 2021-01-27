# Data Modeling with Cassandra

## Introduction

In this project, we will create an Apache Cassandra database which will host data collected on on songs and user activity on Sparkify's new music streaming app. The analysis team is interested in understanding what songs users are listening to; however, there is currently no easy way to query the data to generate the results given that the data resides in a directory of CSV files.

The main queries we will address when modeling the database tables include:
1. Give me the artist, song title and song's length in the music app history that was heard during  `sessionId = 338`, and `itemInSession = 4`.
2. Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for `userId = 10`, `sessionId = 182`.
3. Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'.


### Setup Environment

To run any of the files associated with this project, we will create an Anaconda environment. Before beginning, make sure you have an updated version of [Anaconda](https://anaconda.org/). Now, follow these steps on your terminal:

1. `conda create -n project2 python=3.8 cassandra-driver pandas ipykernel`
2. `source activate project2`

_Note_: As of this project, `cassandra-driver` is only supported on `python=3.8`.

If running the accompanying `.ipynb` notebook, make sure to also run this on your terminal

```bash
python -m ipykernel install --user --name project2
```

### Data Overview

For this project, we'll be working with one dataset: `event_data`. The directory of CSV files is partitioned by date. Here are examples of filepaths to two files in the dataset:

```
event_data/2018-11-08-events.csv
event_data/2018-11-09-events.csv
```

Each CSV file contains event data from users for a specific day. The CSV is comprised of the following information:
- `artist` - artist name
- `auth` - tracks whether the user logged in or logged out
- `firstName` - user first name
- `gender` - user gender
- `itemInSession` - number of items for a specific session
- `lastName` - user last name
- `length` - length of session/event
- `level` - tracks whether the user paid for the session or if the session was free
- `location` - user location
- `method` - HTTP methods
- `page` - tracks the page name such as 'NextSong', 'Home', 'Logout', 'Settings', 'Downgrade', 'Login', 'Help', 'Error', 'Upgrade'
- `registration` - registration timestamp
- `sessionId` - session id
- `song` - song name
- `status` - tracks the status of the request such as 200, 307, 404
- `ts` - timestamp in millisecond
- `userId` - user id

### Data Processing

Prior to populating the Apache Cassandra tables, we will merge all the CSV data under `event_datafile_new.csv`. To answer the questions presented in [Introduction](#Introduction), we will retrieve only the relevant information from each CSV file. This includes: `artist, firstName, gender, itemInSession, lastName, length, level, location, sessionId, song, userId`.

The image below is a screenshot of what the data looks like in the `event_datafile_new.csv`:
![image_event_datafile_new](./image.jpeg)

To minimize memory constraints, we will first create the file where we will dump all the data, and as we iterate over each CSV file, we will write each row in the main CSV file. This will allow us to bypass any memory errors from loading the entire data into memory.

Lastly, we will use this file to populate the Apache Cassandra tables.

## Designing the Apache Cassandra Data Model

Remember the questions we want to answer by modeling the tables:

1. Give me the artist, song title and song's length in the music app history that was heard during  `sessionId = 338`, and `itemInSession = 4`.
2. Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for `userId = 10`, `sessionId = 182`.
3. Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'.

When data modeling in Apache Cassandra, we must design the models to fit the query. This data model will assist in spreading the data evenly around the clusters. The components which we will use to design the tables consist of

* `PRIMARY KEY`
* `PARTITION KEY`
* `CLUSTERING COLUMNS`

Additionally, we will name each table according to the context of the respective queries: `artist_song_session`, `song_playlist_session`, and `user_by_song`. Apache Cassandra does not support duplicate rows, so this is something we need to address when creating the tables.

### Data Model Components

By specifying a `PRIMARY KEY` attribute, we are defining the fields that uniquely identify every record in the table and how the data is distributed across the nodes in our system. The `PRIMARY KEY` is made up of either just the `PARTITION KEY` or with the addition of `CLUSTERING COLUMNS`. The partition key's row value will be hashed and stored on the node in the system that holds that range of values. When picking the `PRIMARY KEY` we will pick a key that will evenly distribute the data.

### `artist_song_session` Table

The `artist_song_session` table will be designed to answer the first query. The table will have the following information:

| field name | field type | field attribute(s) |
| ---------- | ---------- | ------------------ |
| artist     | TEXT       |         |
| title      | TEXT       |         |
| length     | FLOAT      |         |
| session_id  | INT       | PRIMARY KEY, CLUSTERING COLUMN |
| item_in_session | INT   | PRIMARY KEY, PARTITION KEY |

When creating the table, we must decide which field will be used as a partition key. Provided the above information and with some simple statistics, we can make an informed decision.

Let's first look at the number of observations in `event_datafile_new.csv` grouped by `sessionId` and then `itemInSession`. The script to generate these numbers can be found under `stylized_facts.py`.

The total number of observations for the first table is 6820 with
* 776 unique `sessionId` values and an average of 8 values per `sessionId`
* 123 unique `itemInSession` values and an average of 55 values per `itemInSession`

From these observations, we can infer that the `itemInSession` field should be used as a partition key for the `artist_song_session` table since 123 partitions with an average of 55 observations each is better than 776 partitions with 8 values each.

### `song_playlist_session` Table

We will model the `song_playlist_session` table to answer the second query. The table will have the following information:

| field name | field type | field attribute(s) |
| ---------- | ---------- | ------------------ |
| artist     | TEXT       |  |
| title      | TEXT       |  |
| first_name | TEXT       |  |
| last_name  | TEXT       |  |
| user_id    | INT        | PRIMARY KEY , PARTITION KEY |
| session_id | INT        | PRIMARY KEY , PARTITION KEY |
| item_in_session | INT   | PRIMARY KEY, CLUSTERING COLUMN |

The fields that uniquely identify the table include `user_id`, `session_id`, and `item_in_session`. Because the query requires the results to be sorted by `item_in_session`, we can't use `item_in_session` as a `CLUSTERING KEY` when modeling this table. Furthermore, since the query asks us to filter by `userId` and `sessionId`, we will use both these fields as partition keys. The rest of the `PRIMARY KEY` fields will be used as `CLUSTERING COLUMNS`. The first clustering column field in the query will be the `item_in_session` field since the response from the query has to be sorted by this field.

### `user_by_song` Table

The `user_by_song` table will be designed to answer the last query and will include the following:

| field name | field type | field attribute(s) |
| ---------- | ---------- | ------------------ |
| user_id    | INT        |  PRIMARY KEY, CLUSTERING COLUMN |
| first_name | TEXT       |   |
| last_name  | TEXT       |   |
| title      | TEXT       |  PRIMARY KEY , PARTITION KEY |

The two `PRIMARY KEY`s are `user_id` and `title` because they uniquely identify every row. Since the query asks us to filter the data by `title`, it will be used as a `PARTITION KEY`, whereas `user_id` will consequently be the `CLUSTERING COLUMN`.

### Creating Tables

In order to create the tables, we will first look at `create_tables.py` file which does the following:
1. Merges all the CSV files under `event_datafile_new.csv` which will be used to insert data into the Apache Cassandra tables
2. Delete any existing tables with the same names
3. Create the tables using the constraints mentioned in [Designing the Apache Cassandra Data Model](#Designing-the-Apache-Cassandra-Data-Model)

The queries to drop any existing tables or create new tables are imported from `sql_queries.py`. Below is the syntax for creating each table.

**SQL syntax for creating the `artist_song_session` table**

```sql
CREATE TABLE IF NOT EXISTS artist_song_session (
    item_in_session INT, session_id INT, artist TEXT, \
    title TEXT, length FLOAT, 
    PRIMARY KEY(item_in_session, session_id)
);
```

**SQL syntax for creating the `song_playlist_session` table**

```sql
CREATE TABLE IF NOT EXISTS song_playlist_session (
    user_id INT, session_id INT, item_in_session INT, 
    first_name TEXT, last_name TEXT, artist TEXT, title TEXT,
    PRIMARY KEY((user_id, session_id), item_in_session)
);
```

**SQL syntax for creating the `user_by_song` table**

```sql
CREATE TABLE IF NOT EXISTS user_by_song (
    title TEXT, user_id INT, first_name TEXT, last_name TEXT,
    PRIMARY KEY(title, user_id)
);
```

We will create the tables by running `create_tables.py` on the terminal, like so:

```bash
python create_tables.py
```

## ETL Pipelines

In this section, we will develop pipelines for extracting, transforming, loading the data into the tables. We will start by first processing the data. We will read a chunk of the data from `event_datafile_new.csv` and while iterating over each row of the chunk, we will inserts the appropriate data into corresponding Apache Cassandra tables.

### Populating Tables

To insert records, we follow a similar query syntax `"INSERT INTO \<tableName\>, (/<fieldName1/>, /<fieldName2/>, ...) VALUES (%s, %s, ...)"`.

**SQL syntax for inserting records in `artist_song_session`**:

```sql
INSERT INTO artist_song_session (
    item_in_session, session_id, artist, title, length
    ) VALUES (%s, %s, %s, %s, %s);
```

**SQL syntax for inserting records in `song_playlist_session`**:

```sql
INSERT INTO song_playlist_session (
    user_id, session_id, item_in_session, first_name,
    last_name, artist, title
    ) VALUES (%s, %s, %s, %s, %s, %s, %s);
```

**SQL syntax for inserting records in `user_by_song`**:

```sql
INSERT INTO user_by_song (
    title, user_id, first_name, last_name
    ) VALUES (%s, %s, %s, %s);
```

All queries for inserting records can be found under `sql_queries.py`.

To execute all the ETL pipelines, run the following on your command line:

```bash
python etl.py
```

#### Error Handling

All `*.py` files use `logging` to document any exception handling on the terminal. If the script runs into any errors, the warning will be displayed on the user's terminal and will either terminate the program or continue to the next iteration. See all `*.py` files for detailed information.

### Testing ETL Pipelines

Once the tables have been populated, we can run the queries we used to model the database tables.

**QUERY 1**: Give me the artist, song title and song's length in the music app history that was heard during  `sessionId = 338`, and `itemInSession = 4`.

The SQL syntax used for extracting this information is

```sql
SELECT artist, title, length FROM artist_song_session
    WHERE session_id=338 AND item_in_session=4;
```

**QUERY 2**: Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for `userId = 10`, `sessionId = 182`.

The following SQL syntax is used

```sql
SELECT artist, title, first_name, last_name FROM song_playlist_session
    WHERE user_id=10 AND session_id = 182;
```

**QUERY 3**: Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'.

```sql
SELECT first_name, last_name FROM user_by_song
    WHERE title='All Hands Against His Own';
```

The results from each query are printed on the terminal when the `etl.py` file is executed.

## Authors

Yuna Luzi - @najuzilu
