from typing import List, Dict

def calculate_win_percentage(wins: int, ot_losses: int, total_games: int) -> float:
    return (wins + ot_losses) / total_games if total_games > 0 else 0.0

def calculate_plus_minus(goals_for: int, goals_against: int) -> int:
    return goals_for - goals_against

def summarize_wins_losses(data: List[Dict]) -> List[Dict]:
    summary = []
    year_summary = {}
    
    for entry in data:
        year = entry['year']
        if year not in year_summary:
            year_summary[year] = {'winner': entry, 'loser': entry}
        else:
            if entry['wins'] > year_summary[year]['winner']['wins']:
                year_summary[year]['winner'] = entry
            if entry['wins'] < year_summary[year]['loser']['wins']:
                year_summary[year]['loser'] = entry
    
    for year, teams in year_summary.items():
        summary.append({
            'year': year,
            'winner': teams['winner']['team'],
            'winner_wins': teams['winner']['wins'],
            'loser': teams['loser']['team'],
            'loser_wins': teams['loser']['wins']
        })
    
    return summary
