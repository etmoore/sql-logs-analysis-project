#!/usr/bin/env python3
'''This module queries the database to find the most popular
articles and authors, as well as the days in which more than
1% of requests resulted in errors'''

import psycopg2


def main():
    '''Executes log analysis functions'''
    print('Generating report - Please Wait...\n\n')

    print_top_three_articles()
    print_top_authors()
    print_error_days()


def get_query_results(query):
    '''Queries the news database and returns the result'''
    database = psycopg2.connect(database="news")
    cursor = database.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    database.close()
    return result


def print_top_three_articles():
    '''Print the three most popular articles.'''

    query = '''
    SELECT articles.title, COUNT(*) AS views
    FROM articles, log
    WHERE log.path = CONCAT('/article/', articles.slug)
       AND log.status = '200 OK'
    GROUP BY articles.title
    ORDER BY views DESC
    LIMIT 3;
    '''
    data = get_query_results(query)

    print('Top three popular articles of all time:')
    for (title, views) in data:
        print("\t'{0}' -- {1} views".format(title, views))
    print('\n')


def print_top_authors():
    '''Print the most popular authors.'''

    query = '''
    SELECT authors.name, COUNT(*) AS views
    FROM articles, log, authors
    WHERE log.path = CONCAT('/article/', articles.slug)
        AND log.status = '200 OK'
        AND authors.id = articles.author
    GROUP BY authors.name
    ORDER BY views DESC;
    '''
    data = get_query_results(query)

    print('Most popular authors of all time:')
    for (author, views) in data:
        print("\t{0} -- {1} views".format(author, views))
    print('\n')


def print_error_days():
    ''' Print the days on which more than 1 % of requests led to errors'''

    query = '''
    SELECT *
    FROM(
        SELECT views.log_date,
            ROUND(100.0 * errors.error_count / views.view_count, 1)
            AS percentage
        FROM(
            SELECT to_char(log.time, 'FMMonth FMDD, YYYY') as log_date,
                COUNT(*) as view_count
            FROM log
            GROUP BY log_date
        ) AS views, (
            SELECT to_char(log.time, 'FMMonth FMDD, YYYY') AS log_date,
                COUNT(*) as error_count
            FROM log
            WHERE log.status LIKE '4%' OR log.status LIKE '5%'
            GROUP BY log_date
        ) AS errors
        WHERE views.log_date=errors.log_date
    ) as error_rate
    WHERE error_rate.percentage > 1
    ORDER BY error_rate.percentage DESC;
    '''
    data = get_query_results(query)

    print('Days with >1% errors:')
    for (date, percentage) in data:
        print("\t{0} -- {1}% errors".format(date, percentage))
    print('\n')


if __name__ == "__main__":
    main()
