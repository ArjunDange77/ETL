import pytest
from unittest.mock import patch
from src.transformer import calculate_win_percentage, calculate_plus_minus, summarize_wins_losses

def test_calculate_win_percentage():
    assert calculate_win_percentage(10, 5, 15) == 1.0
    assert calculate_win_percentage(0, 0, 0) == 0.0
    assert calculate_win_percentage(10, 0, 10) == 1.0
    assert calculate_win_percentage(5, 5, 10) == 1.0

def test_calculate_plus_minus():
    assert calculate_plus_minus(20, 10) == 10
    assert calculate_plus_minus(0, 0) == 0
    assert calculate_plus_minus(10, 20) == -10
    assert calculate_plus_minus(30, 25) == 5

def test_summarize_wins_losses():
    sample_data = [
        {'year': 1990, 'team': 'Team A', 'wins': 10, 'losses': 20, 'ot_losses': 5},
        {'year': 1990, 'team': 'Team B', 'wins': 5, 'losses': 25, 'ot_losses': 5},
        {'year': 1991, 'team': 'Team C', 'wins': 15, 'losses': 15, 'ot_losses': 5},
        {'year': 1991, 'team': 'Team D', 'wins': 8, 'losses': 22, 'ot_losses': 5}
    ]
    
    result = summarize_wins_losses(sample_data)
    expected = [
        {'year': 1990, 'winner': 'Team A', 'winner_wins': 10, 'loser': 'Team B', 'loser_wins': 5},
        {'year': 1991, 'winner': 'Team C', 'winner_wins': 15, 'loser': 'Team D', 'loser_wins': 8}
    ]
    
    assert result == expected
