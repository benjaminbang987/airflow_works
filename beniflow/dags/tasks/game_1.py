"""
Setting up the simulation for running the 'Rock, Paper Scissors' game.
For simplicity, let's do a single game with 2 people, but later scale to allow for n people for n rounds.
"""

import logging
import random as random
import pandas as pd
import datetime
import psycopg2
import csv
from io import StringIO


def psql_insert_copy(table_schema, table_name, conn, keys, data_iter):
    # gets a DBAPI connection that can provide a cursor
    # code from https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-sql-method
    with conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ', '.join('"{}"'.format(k) for k in keys)
        if table_schema:
            _table_name = '{}.{}'.format(table_schema, table_name)
        else:
            _table_name = table_name

        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
            _table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)


CHOICE_LIST = ["r", "p", "s"]


def rock_paper_scissors(n_players=2, n_games=1):
    """
    Function to run the rock_paper_scissors game. Returns the dictionary of the results
    """
    try:
        win_dict = dict(zip(range(0, n_players), [0] * n_players))
        for round in range(1, n_games+1):
            # first round
            logging.info("Round %s" % round)
            verdict = play_round(n_players)  # list of 1/0 for win/loss
            for key in win_dict:
                win_dict[key] += verdict[key]
            logging.info("Win dict is %s" % win_dict)
        return win_dict
    except TypeError:
        logging.info("The number of players and number of rounds need to be integers. Try again")


def play_round(n_players):
    """
    Function to run a single round of rock_paper_scissors game. Returns a list of 1/0 for win/loss for each player.
    """
    if n_players <= 1:
        raise KeyError('The number of players needs to be greater than 1.')
    if not isinstance(n_players, int):
        raise KeyError('The number of players has to be an integer.')
    verdict = []
    while not verdict:
        result = ['a' for _ in range(0, n_players)]
        for player in range(0, n_players):
            result[player] = random.choice(CHOICE_LIST)
        logging.info("The choices of this round are %s" % result)
        verdict = round_verdict(result)  # returns an empty list of the round is a draw

    return verdict


def round_verdict(game_choice_result_list):
    """
    Function to determine the verdict of a given round. Returns a list of verdict for a given list of choices.
    """
    if "r" in set(game_choice_result_list) and "p" in set(game_choice_result_list) and "s" in set(
            game_choice_result_list):
        return []
    elif "r" in set(game_choice_result_list) and "p" in set(game_choice_result_list):
        verdict = [1 if x == 'p' else 0 for x in game_choice_result_list]
        return verdict
    elif "r" in set(game_choice_result_list) and "s" in set(game_choice_result_list):
        verdict = [1 if x == 'r' else 0 for x in game_choice_result_list]
        return verdict
    elif "p" in set(game_choice_result_list) and "s" in set(game_choice_result_list):
        verdict = [1 if x == 's' else 0 for x in game_choice_result_list]
        return verdict
    else:
        return []


def insert_results(game_result_dict, db_url, n_players, n_games):
    """
    Function to insert the game_result_dict into the database
    """

    query_create_schema = 'create schema if not exists sandbox;'
    query_create_table = 'create table if not exists sandbox.game_1_results (' \
                         'player_num  int,' \
                         'win_count int,' \
                         'n_players int,' \
                         'n_games int,' \
                         'timestamp timestamp' \
                         ');'

    player_num = game_result_dict.keys()
    win_count = [game_result_dict[x] for x in player_num]
    n_players_list = [n_players] * len(win_count)
    n_games_list = [n_games] * len(win_count)

    data_export = dict(
        player_num=list(player_num),
        win_count=win_count,
        n_players=n_players_list,
        n_games=n_games_list,
        timestamp=datetime.datetime.now()
    )

    df_export = pd.DataFrame.from_dict(data_export)
    with psycopg2.connect(database=db_url) as conn:
        with conn.cursor() as cur:
            logging.info('creating schema if not exists')
            cur.execute(query_create_schema)
            logging.info('creating table if not exists')
            cur.execute(query_create_table)
        logging.info('inserting game results to the table')
        psql_insert_copy(table_name='game_1_results',
                         table_schema='sandbox',
                         conn=conn,
                         keys=df_export.keys(),
                         data_iter=df_export.values)


def game_1_main(database_url, n_players=2, n_games=1):
    """
    Main function that plays the game and stores the results in the specified postgresql database
    """
    win_dict = rock_paper_scissors(n_players, n_games)
    insert_results(win_dict, database_url, n_players, n_games)


if __name__ == "__main__":
    game_1_main()
