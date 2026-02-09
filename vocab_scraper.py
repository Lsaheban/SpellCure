
import requests
from bs4 import BeautifulSoup
import re
import time
import sys
import os
import urllib.parse

def get_page_text(url):
    """Fetches a URL and returns the visible text."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        print(f"  Fetching {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"  Failed with status {response.status_code}")
            return ""
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
            script.decompose()
            
        text = soup.get_text()
        return text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def search_ddg_html(query, max_results=3):
    """Searches DuckDuckGo HTML version."""
    url = "https://html.duckduckgo.com/html/"
    data = {'q': query}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://html.duckduckgo.com/'
    }
    
    try:
        print(f"Searching DDG for: '{query}'")
        res = requests.post(url, data=data, headers=headers, timeout=10)
        res.raise_for_status()
        
        soup = BeautifulSoup(res.text, 'html.parser')
        results = []
        
        # Parse text-heavy results
        for link in soup.find_all('a', class_='result__a'):
            href = link.get('href')
            if href:
                # DDG wraps links? usually in html version it might be direct or wrapped
                # result__a href is usually the target URL
                results.append(href)
                if len(results) >= max_results:
                    break
        return results
    except Exception as e:
        print(f"DDG Search error: {e}")
        return []

def clean_text(text):
    """Extracts unique valid English words from text."""
    # Regex for words: 3+ letters, starts with letter
    # Exclude common garbage
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    return set(words)

def scrape_vocabulary():
    queries = [
        "1000 most common english words list",
        "common english verbs list",
        "essential english vocabulary for students",
        "oxford 3000 word list text",
        "academic vocabulary list"
    ]
    
    all_words = set()
    
    print("Starting scraping process (Lightweight Mode)...")
    
    for query in queries:
        urls = search_ddg_html(query, max_results=2)
        
        for url in urls:
            text = get_page_text(url)
            words = clean_text(text)
            print(f"    Found {len(words)} words.")
            all_words.update(words)
            
            # Be polite
            time.sleep(2)
        time.sleep(1)
                
    print(f"Total unique words scraped: {len(all_words)}")
    
    # Save to file
    output_path = os.path.join(os.path.dirname(__file__), 'scraped_data.py')
    print(f"Saving to {output_path}...")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Auto-generated from web scraping\n")
            f.write("# Source: DuckDuckGo Search -> Web Pages\n\n")
            word_list = sorted(list(all_words))
            f.write(f"SCRAPED_VOCAB = {word_list}\n")
    except Exception as e:
        print(f"Error saving file: {e}")
        
    print("Done.")

if __name__ == "__main__":
    scrape_vocabulary()
