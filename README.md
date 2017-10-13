# Udacity Logs Analysis Project
![A Udacity Full Stack Nanodegree Project](https://img.shields.io/badge/Udacity-Full%20Stack%20Nanodegree-lightgrey.svg)

## Description:
The LogAnalyzer script queries a database containing 'authors', 'articles', and 'log' tables and prints answers to the following questions:
1. What are the three most popular articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Requirements
* Python 3.5.3
* psycopg2
* Postgresql 9.5.8

## Configuration
1. Make sure you have requirements listed above installed.
2. Create the `news` Postgres database by running:   
`$ createdb news`
3. [Download the data here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and unzip it to extract the `newsdata.sql` file.
4. Load the data into the database with:  
`$ psql -d news -f newsdata.sql`

## How to run

From the root of this project, run:  
`$ python3 LogAnalyzer.py`

You should see the output contained in [output.txt](./output.txt) in your terminal.