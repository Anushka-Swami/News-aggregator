from flask import Flask, jsonify
from flask_cors import CORS
from models import db, Article
from config import Config
import threading
from scheduler import start_periodic_scraping
from sqlalchemy import inspect
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    # Move all routes inside create_app
    @app.route('/api/articles')
    def get_articles():
        articles = Article.query.order_by(Article.created_at.desc()).all()
        return jsonify([article.to_dict() for article in articles])
    
    @app.route('/api/verify-db')
    def verify_db():
        try:
            # Check if tables exist using SQLAlchemy's inspect
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            # Test connection by making a simple query
            articles_count = Article.query.count()
            
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
