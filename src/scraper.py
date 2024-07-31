import requests
from bs4 import BeautifulSoup
from typing import List
import zipfile
import logging


PAGE_URL = "https://www.scrapethissite.com/pages/forms/?page_num={}"

MAX_PAGES = 100

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_page_content(page_num: int) -> str:
    logging.debug(f"Fetching page {page_num}")
    try:
        response = requests.get(PAGE_URL.format(page_num), timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching page {page_num}: {e}")
        return ""

def parse_team_stats(html: str) -> List[dict]:
    soup = BeautifulSoup(html, 'html.parser')
    logging.debug("Parsing HTML content")
    
    table = soup.find('table', class_='table')
    if not table:
        logging.error("No table found with class 'table'")
        return []

    rows = table.find_all('tr')
    if not rows:
        logging.error("No table rows found")
        return []

    unique_data = set()
    data = []
    
    for row in rows[1:]:  # Skip header row
        cols = row.find_all('td')
        if not cols:
            logging.error(f"No columns found in row: {row}")
            continue
        
        columns_text = [col.text.strip() for col in cols]
        logging.debug(f"Columns in row: {columns_text}")
        
        if len(columns_text) < 9:
            logging.error(f"Unexpected number of columns in row: {len(columns_text)}")
            continue
        
        try:
            # Fetching data directly without additional calculations
            team = columns_text[0]
            year = int(columns_text[1]) if columns_text[1] else None
            wins = int(columns_text[2]) if columns_text[2] else 0
            losses = int(columns_text[3]) if columns_text[3] else 0
            ot_losses = int(columns_text[4]) if columns_text[4] else 0
            win_percentage = columns_text[5]  # Assuming this is provided as is
            goals_for = int(columns_text[6]) if columns_text[6] else 0
            goals_against = int(columns_text[7]) if columns_text[7] else 0
            plus_minus = int(columns_text[8]) if columns_text[8] else 0
            
            record = (team, year, wins, losses, ot_losses, win_percentage, goals_for, goals_against, plus_minus)
            
            if record not in unique_data:
                unique_data.add(record)
                data.append({
                    'team': team,
                    'year': year,
                    'wins': wins,
                    'losses': losses,
                    'ot_losses': ot_losses,
                    'win_percentage': win_percentage,
                    'goals_for': goals_for,
                    'goals_against': goals_against,
                    'plus_minus': plus_minus
                })
        except ValueError as e:
            logging.error(f"Error parsing row data: {e}")
    
    return data

def scrape_all_pages() -> List[dict]:
    all_data = []
    page_num = 1
    html_pages = []
    
    while True:
        html = fetch_page_content(page_num)
        if not html:
            logging.debug(f"No HTML content found on page {page_num}. Stopping.")
            break
        
        html_pages.append((f"page_{page_num}.html", html))
        data = parse_team_stats(html)
        if not data:
            logging.debug(f"No data parsed from page {page_num}. Stopping.")
            break
        
        all_data.extend(data)
        logging.debug(f"Scraped {len(data)} rows from page {page_num}")
        page_num += 1
    
    # Save HTML pages to zip
    with zipfile.ZipFile("data.zip", "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_name, content in html_pages:
            zip_file.writestr(file_name, content)
    
    logging.debug(f"Total scraped rows: {len(all_data)}")
    return all_data