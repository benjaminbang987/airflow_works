"""
Setting up the simulation for running the 'Rock, Paper Scissors' game.
For simplicity, let's do a single game with 2 people, but later scale to allow for n people for n rounds.
"""

import random as random


CHOICE_LIST = ["r", "p", "s"]


def rock_paper_scissors(n_players=2, n_rounds=1):
    """
    Function to run the rock_paper_scissors game. Returns the dictionary of the results
    """
    try:
        win_dict = dict(zip(range(0, n_players), [0] * n_players))
        for round in range(1, n_rounds+1):
            # first round
            print("Round %s" % round)
            verdict = play_round(n_players)  # list of 1/0 for win/loss
            for key in win_dict:
                win_dict[key] += verdict[key]
            print("Win dict is %s" % win_dict)
        return win_dict
    except TypeError:
        print("The number of players and number of rounds need to be integers. Try again")



def play_round(n_players):
    """
    Function to run a single round of rock_paper_scissors game. Returns a list of 1/0 for win/loss for each player.
    """
    verdict = []
    while verdict == []:
        result = ['a' for _ in range(0,n_players)]
        for player in range(0, n_players):
            result[player] = random.choice(CHOICE_LIST)
        print("The choices of this round are %s" % result)
        verdict = round_verdict(result)  # returns an empty list of the round is a draw

    return verdict


def round_verdict(game_choice_result_list):
    """
    Function to determine the verdict of a given round. Returns the list of verdict for a given list of choices.
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
