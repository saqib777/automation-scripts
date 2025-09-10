"""Simple Web Scraper"""
import requests
from bs4 import BeautifulSoup

def scrape_titles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return [title.get_text() for title in soup.find_all('h1')]

if __name__ == "__main__":
    titles = scrape_titles("https://example.com")
    print(titles)
