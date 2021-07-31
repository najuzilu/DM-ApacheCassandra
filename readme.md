![Language](https://img.shields.io/badge/language-python--3.7-blue) [![Contributors][contributors-shield]][contributors-url] [![Stargazers][stars-shield]][stars-url] [![Forks][forks-shield]][forks-url] [![Issues][issues-shield]][issues-url] [![MIT License][license-shield]][license-url] [![LinkedIn][linkedin-shield]][linkedin-url]

<br />
<p align="center">
    <a href="https://github.com/najuzilu/DM-ApacheCassandra">
        <img src="./images/logo.png" alt="Logo" width="200" height="200">
    </a>
    <h2 align="center">Data Modeling with Cassandra</h2>
    <br />
    <br />
</p>

> apache cassandra, data engineering, ETL, star database schema, data modeling

## About The Project

Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analysis team is particularly interested in understanding what songs users are listening to. Currently, there is no easy way to query the data to generate the results, since the data reside in a directory of CSV files on user activity on the app.

They'd like a data engineer to create an Apache Cassandra database which can create queries on song play data to answer the questions, and wish to bring you on the project. Your role is to create a database for this analysis. You'll be able to test your database by running queries given to you by the analytics team from Sparkify to create the results.

## Description

In this project, you will create an Apache Cassandra database which will host data collected on songs and user activity on Sparkify's new music streaming app.

### Tools

* python
* Apache Cassandra
* Jupyter notebooks

## Datasets

You will work with one dataset: `event_data/`. The directory of CSV files is partitioned by date. Here are examples of filepaths to two files in the dataset:

```
event_data/2018-11-08-events.csv
event_data/2018-11-09-events.csv
```

Each CSV file contains event data from users for a specific day. The CSV is comprised of the following fields:

| Field          |   Description              |
| :------------- | :------------------------- |
| artist        | artist name               |
| auth          | tracks whether the user logged in or logged out |
| firstName     |   user first name |
| gender |  user gender |
| itemInSession | number of items for a specific session |
| lastName | user last name |
| length | length of session/event |
| level | tracks whether the user paid for the session or if the session was free |
| location | user location |
| method | HTTP methods |
| page | tracks the page name such as 'NextSong', 'Home', 'Logout', 'Settings', 'Downgrade', 'Login', 'Help', 'Error', 'Upgrade' |
| registration | registration timestamp |
| sessionId | session id |
| song | song name |
| status | tracks the status of the request such as 200, 307, 404 |
| ts | timestamp in millisecond |
| userId | user id |

**[Note:](#)**
Prior to populating the tables, you will merge all the CSV data under `event_datafile_new.csv`. This merged data includes

![image_event_datafile_new](./images/image.jpeg)

<!-- ## ERD Model-->

<!-- ## Project Structure -->

## Getting Started

Clone this repository

```bash
git clone https://github.com/najuzilu/DM-ApacheCassandra.git
```

### Prerequisites

* conda
* python 3.8
* cassandra-driver
* pandas

Create a virtual environment through Anaconda using

```bash
conda env create --file environment.yml
```

## Project Steps

1. Run `create_tables.py` to create the tables
    ```bash
    python create_tables.py
    ```
2. Run `etl.py` to execute the ETL pipeline and load the data in the database
    ```bash
    python etl_tables.py
    ```
3. Run `stylized_facts.py` to make sure that all the tables have been populated successfully.
    ```bash
    python stylized_facts.py
    ```

## Authors

Yuna Luzi - @najuzilu

## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- Links --->

[contributors-shield]: https://img.shields.io/github/contributors/najuzilu/DM-ApacheCassandra.svg?style=flat-square
[contributors-url]: https://github.com/najuzilu/DM-ApacheCassandra/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/najuzilu/DM-ApacheCassandra.svg?style=flat-square
[forks-url]: https://github.com/najuzilu/DM-ApacheCassandra/network/members
[stars-shield]: https://img.shields.io/github/stars/najuzilu/DM-ApacheCassandra.svg?style=flat-square
[stars-url]: https://github.com/najuzilu/DM-ApacheCassandra/stargazers
[issues-shield]: https://img.shields.io/github/issues/najuzilu/DM-ApacheCassandra.svg?style=flat-square
[issues-url]: https://github.com/najuzilu/DM-ApacheCassandra/issues
[license-shield]: https://img.shields.io/badge/License-MIT-yellow.svg
[license-url]: https://github.com/najuzilu/DM-ApacheCassandra/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/yuna-luzi/
