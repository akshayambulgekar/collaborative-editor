Setup Instructions
Local Setup

Clone the repository:git clone https://github.com/yourusername/collaborative-editor.git


Create and activate a virtual environment:python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac


Install dependencies:pip install -r requirements.txt


Create a .env file in the project root:FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/collaborative_editor
LANGUAGE_TOOL_API=https://api.languagetool.org/v2/check

Generate a secret key:python -c "import secrets; print(secrets.token_hex(16))"


Set up a local PostgreSQL database:
Install PostgreSQL (postgresql.org).
Create a database:createdb collaborative_editor


Update DATABASE_URL with your credentials.


Install and run a local LanguageTool server:
Download LanguageTool from languagetool.org/download (e.g., LanguageTool-6.5.zip).
Unzip and run:cd path/to/LanguageTool
java -cp languagetool-server.jar org.languagetool.server.HTTPServer --port 8081




Initialize the database:python -c "from app import create_app, db; app, _ = create_app(); with app.app_context(): db.create_all()"


Run the application:python run.py


Access at http://localhost:5000.

Deploy on Render

Push your project to a GitHub repository:git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/collaborative-editor.git
git push -u origin main


Sign up at render.com and connect your GitHub account.
Create a Web Service:
Select your repository (collaborative-editor) and branch (main).
Configure:
Name: collaborative-editor
Environment: Python
Region: Closest (e.g., Oregon)
Root Directory: Blank (since run.py is in the root)
Build Command: pip install -r requirements.txt
Start Command: gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 app:app
Instance Type: Free


Click Create Web Service.


Create a PostgreSQL database:
Click New > PostgreSQL.
Configure:
Name: collaborative-editor-db
Database: collaborative_editor
User: myuser
Region: Same as web service.


Copy the Internal Database URL.


Set environment variables in the web service:
FLASK_ENV: production
SECRET_KEY: <random-string> (generate with python -c "import secrets; print(secrets.token_hex(16))")
DATABASE_URL: <postgresql-url-from-step-4>
LANGUAGE_TOOL_API: https://api.languagetool.org/v2/check


Deploy and access at https://collaborative-editor.onrender.com.

Testing

Local: Run python run.py, test at http://localhost:5000.
Render: Access the Render URL, test login, AI suggestions, real-time collaboration, version history, and responsive UI.
Debugging:
Check Render logs for server errors.
Use browser DevTools (F12) for JavaScript errors and Network tab for API calls.
Verify LanguageTool API (https://api.languagetool.org/v2/check) for 429 errors.


