import os
from zipfile import ZipFile
from openpyxl import Workbook
from typing import List, Dict

def save_html_to_zip(html_pages: List[str], zip_filename: str):
    with ZipFile(zip_filename, 'w') as zipf:
        for i, html in enumerate(html_pages, start=1):
            filename = f"{i}.html"
            zipf.writestr(filename, html)

def save_data_to_excel(raw_data: List[Dict], summary_data: List[Dict], excel_filename: str):
    wb = Workbook()
    
    ws1 = wb.active
    ws1.title = "NHL Stats 1990-2011"
    ws1.append(["Year", "Team", "Wins", "Losses", "OT Losses", "Win %", "Goals For (GF)", "Goals Against (GA)", "+ / -"])
    for entry in raw_data:
        ws1.append([
            entry['year'], entry['team'], entry['wins'], entry['losses'], entry['ot_losses'], 
            entry['win_percentage'], entry['goals_for'], entry['goals_against'], entry['plus_minus']
        ])
    
    ws2 = wb.create_sheet(title="Winner and Loser per Year")
    ws2.append(["Year", "Winner", "Winner Num. of Wins", "Loser", "Loser Num. of Wins"])
    
    yearly_summary = {}
    for entry in raw_data:
        year = entry['year']
        if year not in yearly_summary:
            yearly_summary[year] = {'winner': None, 'winner_wins': -1, 'loser': None, 'loser_wins': float('inf')}
        
        if entry['wins'] > yearly_summary[year]['winner_wins']:
            yearly_summary[year]['winner'] = entry['team']
            yearly_summary[year]['winner_wins'] = entry['wins']
        
        if entry['wins'] < yearly_summary[year]['loser_wins']:
            yearly_summary[year]['loser'] = entry['team']
            yearly_summary[year]['loser_wins'] = entry['wins']
    
    for year, data in yearly_summary.items():
        ws2.append([year, data['winner'], data['winner_wins'], data['loser'], data['loser_wins']])
    
    wb.save(excel_filename)