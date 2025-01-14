import time
from scraper import scrape_articles
from models import db, Article
import logging
from flask import current_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_periodic_scraping(interval=18000):  # 5 hours
    while True:
        logger.info("Starting scraping process...")
        try:
            # Get the Flask app instance
            from app import create_app
            app = create_app()
            
            # Run scraping within application context
            with app.app_context():
                articles = scrape_articles()
                count = 0
                for article in articles:
                    try:
                        existing_article = Article.query.filter_by(url=article['url']).first()
                        if not existing_article:
                            new_article = Article(
                                title=article['title'],
                                url=article['url'],
                                description=article['content'],
                                published_at=article['date'],
                                source=article['source']
                            )
                            db.session.add(new_article)
                            count += 1
                            logger.info(f"New article queued: {article['title']}")
                    except Exception as e:
                        logger.error(f"Error saving article {article.get('title', 'Unknown')}: {e}")
                        continue
                
                if count > 0:
                    db.session.commit()
                    logger.info(f"Successfully saved {count} new articles")
                else:
                    logger.info("No new articles to save")
                    
        except Exception as e:
            logger.error(f"Scraping error: {e}")
        
        logger.info(f"Scraping cycle completed. Next scrape in {interval/3600} hours")
        time.sleep(interval)