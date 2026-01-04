import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_website(url, target='links'):
    """
    Scrapes data from a website.
    Args:
        url (str): The URL to scrape.
        target (str): 'links', 'images', or 'text'.
    Returns:
        list: List of strings (found items)
    """
    if not url.startswith('http'):
        url = 'https://' + url
        
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        if target == 'links':
            # Extract all hrefs
            for a in soup.find_all('a', href=True):
                full_url = urljoin(url, a['href'])
                results.append(full_url)
                
        elif target == 'images':
            # Extract src from img tags
            for img in soup.find_all('img', src=True):
                full_url = urljoin(url, img['src'])
                results.append(full_url)
                
        elif target == 'text':
            # Extract text from p, h1-h6 tags
            for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                text = tag.get_text(strip=True)
                if text:
                    results.append(text)
        
        return results if results else ["No items found."]

    except Exception as e:
        raise Exception(f"Scraping failed: {str(e)}")
