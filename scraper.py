import threading
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import spacy
import pytextrank
import asyncio
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize spaCy with the en_core_web_sm model
try:
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textrank", last=True)
except Exception as e:
    logger.error(f"Error loading spaCy model: {e}")
    raise

# List of websites and general CSS selectors
WEBSITES = [
    {
        'name': 'The Hindu Business Line',
        'url': 'https://www.thehindubusinessline.com/economy/',
        'link_selector': 'h3.title a[href]',
        'title_selector': 'h1, h2',
        'content_selector': 'div p',
        'image_selector': 'img[src]',
        'date_selector': '.bl-by-line',
    },
    {
        'name': 'Mint',
        'url': 'https://www.livemint.com/economy',
        'link_selector': 'h2.headline a[href]',
        'title_selector': 'h1, h2',
        'content_selector': 'div p',
        'image_selector': 'img[src]',
        'date_selector': '.storyPage_date__JS9qJ span',
    },
    {
        'name': 'The Hindustan Times',
        'url': 'https://www.hindustantimes.com/business/',
        'link_selector': 'a.storyLink.articleClick[href]',
        'title_selector': 'h1, h2',
        'content_selector': ' p',
        'image_selector': 'img[src]',
        'date_selector': 'span.jsx-ace90f4eca22afc7.strydate',
    },
    {
        'name': 'India Today',
        'url': 'https://www.indiatoday.in/business',
        'link_selector': "h2 a[href]",
        'title_selector': 'h1',
        'content_selector': 'p',
        'image_selector': '.imgBox img',
        'date_selector': 'span.jsx-ace90f4eca22afc7.strydate',
    }
]

def get_headers():
    """Return headers for requests"""
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

def summarize_content(content, num_sentences=5):
    """Summarize content using TextRank"""
    try:
        doc = nlp(content)
        
        if len(doc) < 10:
            return content if len(content) < 1000 else content[:1000]

        summary_sentences = []
        for sent in doc._.textrank.summary(limit_phrases=10, limit_sentences=num_sentences):
            summary_sentences.append(sent.text)

        summary = " ".join(summary_sentences)
        
        if not summary.endswith(('.', '!', '?')):
            summary += '.'

        return summary
    except Exception as e:
        logger.error(f"Error during summarization: {e}")
        return content[:1000]  # Return truncated content as fallback

def fetch_article_content(website, article_url):
    """Fetch content for a single article"""
    try:
        response = requests.get(article_url, headers=get_headers(), timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Get title
        title_elem = soup.select_one(website['title_selector'])
        if not title_elem:
            logger.warning(f"No title found for {article_url}")
            return None
        
        title = title_elem.text.strip()
        if not title:
            return None

        # Get content
        content_elements = soup.select(website['content_selector'])
        if not content_elements:
            logger.warning(f"No content found for {article_url}")
            return None
            
        content = " ".join([p.text.strip() for p in content_elements])
        if not content:
            return None

        # Get date
        date_elem = soup.select_one(website['date_selector'])
        date = date_elem.get_text(strip=True) if date_elem else 'No Date'

        return {
            'title': title,
            'url': article_url,
            'content': summarize_content(content),
            'date': clean_date(date, website['name']),
            'source': website['name']
        }

    except requests.Timeout:
        logger.error(f"Timeout fetching {article_url}")
        return None
    except requests.RequestException as e:
        logger.error(f"Error fetching {article_url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error processing {article_url}: {e}")
        return None

def clean_date(raw_date, source):
    """Clean and format dates"""
    try:
        if source == 'The Hindu Business Line':
            if "Updated - " in raw_date:
                raw_date = raw_date.split("Updated - ")[1]
            return raw_date.split(" at")[0].strip()
        if source == 'Mint':
            return raw_date
        if source == 'The Hindustan Times':
            return raw_date
        if source == 'India Today':
            return raw_date
        return raw_date
    except Exception as e:
        logger.error(f"Error cleaning date for {source}: {e}")
        return raw_date

def fetch_articles(website):
    """Fetch articles from a website"""
    articles = []
    try:
        response = requests.get(website['url'], headers=get_headers(), timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        article_links = soup.select(website['link_selector'])
        logger.info(f"Found {len(article_links)} articles on {website['name']}")

        for link in article_links[:10]:  # Limit to 10 articles per source to avoid overload
            try:
                article_url = urljoin(website['url'], link.get('href'))
                article_details = fetch_article_content(website, article_url)
                if article_details:
                    articles.append(article_details)
                    logger.info(f"Successfully processed article: {article_details['title']}")
            except Exception as e:
                logger.error(f"Error processing article from {website['name']}: {e}")
                continue

    except requests.Timeout:
        logger.error(f"Timeout fetching articles from {website['name']}")
    except requests.RequestException as e:
        logger.error(f"Error fetching articles from {website['name']}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error processing {website['name']}: {e}")

    return articles

def scrape_articles():
    """Main function to scrape articles from all websites"""
    all_articles = []
    logger.info("Starting article scraping process...")
    
    for website in WEBSITES:
        try:
            logger.info(f"Scraping articles from {website['name']}...")
            articles = fetch_articles(website)
            all_articles.extend(articles)
            logger.info(f"Successfully scraped {len(articles)} articles from {website['name']}")
        except Exception as e:
            logger.error(f"Error scraping {website['name']}: {e}")
            continue

    logger.info(f"Total articles scraped: {len(all_articles)}")
    return all_articles

if __name__ == "__main__":
    # Test the scraper
    articles = scrape_articles()
    for article in articles:
        print(f"\nTitle: {article['title']}")
        print(f"Source: {article['source']}")
        print(f"Date: {article['date']}")
        print(f"Content: {article['content']}")
        print(f"URL: {article['url']}")
        print("-" * 80)