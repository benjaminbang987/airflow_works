"""
Unit tests for game_1.py
"""

from setup.tasks import game_1 as g1
import pytest


@pytest.mark.parametrize("n_players,expected_list_1,expected_list_2", [
                                                                        (2, [1, 0], [0, 1])
                                                                       ]
                         )
def test_play_round(n_players, expected_list_1, expected_list_2):
    """
    Basic test for play_round function in game_1.py
    """
    verdict = g1.play_round(n_players=n_players)
    assert verdict == expected_list_1 or verdict == expected_list_2,  "The result list has to be consistent"


@pytest.mark.parametrize("n_players,expected", [
                                                (10, range(1, 10)),
                                                (4, range(1, 4))
                                                ]
                         )
def test_round_win_sum(n_players, expected):
    verdict = g1.play_round(n_players=n_players)
    assert sum(verdict) in expected, \
        "The sum of winners need to be in between 1 and total number of players - 1."


@pytest.mark.parametrize("inputs,expected", [
                                             (['r', 's', 'p'], []),
                                             (['r', 's'], [1, 0]),
                                             (['s', 'r'], [0, 1]),
                                            ]
                         )
def test_round_verdict(inputs, expected):
    """
    Basic test for round_verdict function in game_1.py
    """
    assert g1.round_verdict(inputs) == expected, "Verdict has to match possible values."
