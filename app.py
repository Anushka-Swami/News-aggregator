from flask import Flask, jsonify
from flask_cors import CORS
from models import db, Article
from config import Config
import threading
from scheduler import start_periodic_scraping
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Database verification route
@app.route('/api/verify-db')
def verify_db():
    try:
        # Check if tables exist
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        # Create tables if they don't exist
        Base.metadata.create_all(engine)
        
        # Test connection by making a simple query
        db = SessionLocal()
        # Try to query the articles table
        articles_count = db.query(Article).count()
        
        return jsonify({
            "status": "success",
            "database_connected": True,
            "existing_tables": existing_tables,
            "articles_count": articles_count,
            "message": "Database connection verified and tables created"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "database_connected": False,
            "error": str(e),
            "message": "Database connection failed"
        }), 500
    finally:
        db.close()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    @app.route('/api/articles')
    def get_articles():
        articles = Article.query.order_by(Article.created_at.desc()).all()
        return jsonify([article.to_dict() for article in articles])

    return app

def start_app():
    app = create_app()
    
    # Start scraper in background
    scraper_thread = threading.Thread(target=start_periodic_scraping)
    scraper_thread.daemon = True
    scraper_thread.start()
    
    return app

if __name__ == '__main__':
    app = start_app()
    app.run(debug=True)
