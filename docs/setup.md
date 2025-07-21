# Setup Instructions

## Prerequisites
- Python 3.8+
- PostgreSQL
- Node.js (for Vercel CLI)
- Vercel account

## Installation
1. Clone the repository: `git clone <repo-url>`
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Set up PostgreSQL database: `createdb collaborative_editor`
6. Create `.env` file with variables (see `.env.example`)
7. Run the app: `python run.py`

## Deployment
1. Install Vercel CLI: `npm install -g vercel`
2. Deploy: `vercel`
3. Set environment variables in Vercel dashboard