# News Aggregator Project

## Overview
The News Aggregator is a web-based application designed to deliver concise, summarized news content to users with a clean and modern interface. It focuses on aggregating and summarizing news articles from various sources, providing users with categorized news topics and insights.

## Features
- **Real-Time Summaries:** AI-generated summaries for articles, focusing on key points.
- **Categorization:** News grouped into various topics like Indian Economy, Global Economy, Commodities, Rural Economy, and Climate Change.
- **Dynamic Layout:** A minimalist, asymmetrical layout with dynamic cards and smooth transitions.
- **Interactive Sections:** Features like lead stories, sliding stories, and most-viewed pages for enhanced user experience.
- **Source Integration:** Displays news sources and authors.

## Technology Stack
### Frontend
- **React**: Core UI development.
- **TypeScript**: Type safety and improved developer experience.
- **Vite**: Fast build tool for the development environment.
- **Tailwind CSS**: Styling and responsiveness.
- **Framer Motion**: Smooth animations and transitions.

### Backend
- **Flask**: Backend API to serve data.
- **SQLite**: Database for storing scraped articles.
- **BeautifulSoup**: Web scraping library.

### Deployment
- **Frontend**: Hosted on [Vercel](https://pwj6cmajvbpzhnzo.vercel.app/).
- **Backend**: Hosted on [Render](https://news-aggregator-5tb1.onrender.com/api/articles).

## Installation

### Prerequisites
- Node.js
- Python (version 3.9 or above)

### Steps
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Anushka-Swami/News-aggregator.git
   cd news-aggregator
   ```

2. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Backend Setup:**
   ```bash
   cd backend
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```

4. **Run the Application:**
   Access the frontend at `http://localhost:3000` and the backend API at `http://localhost:5000`.

## Deployment Guide

### Frontend (Vercel)
1. Push your frontend code to a GitHub repository.
2. Go to [Vercel](https://vercel.com/) and create a new project.
3. Link your GitHub repository.
4. Configure build settings (default works for Vite).
5. Deploy.

### Backend (Render)
1. Push your backend code to a GitHub repository.
2. Go to [Render](https://render.com/) and create a new web service.
3. Link your GitHub repository.
4. Set the start command to `python app.py`.
5. Deploy.

## API Endpoints
- **`GET /articles`**: Fetch all articles.
- **`GET /articles/:id`**: Fetch a specific article by ID.
- **`POST /articles`**: Add a new article.
- **`DELETE /articles/:id`**: Delete an article by ID.

## Contributing
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Inspired by modern news platforms.
- Powered by Flask, React, and Vercel for seamless performance.

