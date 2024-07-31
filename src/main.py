import logging
from scraper import scrape_all_pages, fetch_page_content
from transformer import summarize_wins_losses
from file_handler import save_html_to_zip, save_data_to_excel

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.debug("Starting the ETL process.")
    
    raw_data = scrape_all_pages()
    if not raw_data:
        logging.error("Failed to scrape any data.")
        return
    
    summary_data = summarize_wins_losses(raw_data)
    logging.debug("Data transformation complete.")
    
    html_pages = []
    for page_num in range(1, 25): 
        html = fetch_page_content(page_num)
        if html:
            html_pages.append(html)
    save_html_to_zip(html_pages, "data.zip")
    
    save_data_to_excel(raw_data, summary_data, "NHL_Stats.xlsx")
    logging.debug("ETL process complete.")

if __name__ == "__main__":
    main()
