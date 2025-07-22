Real-Time Collaborative Document Editor
A web application built with Flask, Flask-SocketIO, Flask-Login, Flask-SQLAlchemy, and LanguageTool API for real-time collaborative document editing, user authentication, AI-powered grammar suggestions, version control, and a responsive UI.
Features

Homepage: Displays centered "Login" and "Register" buttons redirecting to authentication routes.
User Authentication: Secure login and registration using Flask-Login and Flask-WTF.
Real-Time Collaboration: Edit documents in real-time with WebSocket support via Flask-SocketIO.
AI Suggestions: Grammar and spelling suggestions powered by LanguageTool API.
Version Control: Save and restore document versions using Flask-SQLAlchemy and PostgreSQL.
Responsive UI: Styled buttons (blue #1a73e8, hover #174ea6) and mobile-friendly design.

Prerequisites

Python: 3.13 or higher
PostgreSQL: For the database
LanguageTool: For local AI suggestions
Git: For cloning the repository
Render Account: For deployment (optional)

Local Setup

Clone the Repository:
git clone https://github.com/yourusername/collaborative-editor.git
cd collaborative-editor


Create a Virtual Environment:
python -m venv venv

Activate it:

Windows:venv\Scripts\activate


Linux/Mac:source venv/bin/activate




Install Dependencies:
pip install -r requirements.txt


Set Up Environment Variables:Create a .env file in the project root:
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/collaborative_editor
LANGUAGE_TOOL_API=http://localhost:8081/v2/check

Generate a secret key:
python -c "import secrets; print(secrets.token_hex(16))"


Set Up PostgreSQL:

Install PostgreSQL: postgresql.org/download
Create a database:createdb collaborative_editor




Run LanguageTool Server:

Download LanguageTool: languagetool.org/download
Unzip and run:cd path/to/LanguageTool
java -cp languagetool-server.jar org.languagetool.server.HTTPServer --port 8081




Initialize the Database:
python -c "from app import create_app, db; app, _ = create_app(); with app.app_context(): db.create_all()"


Run the Application:
python run.py


Access the Application:

Open http://localhost:5000 in a browser.
The homepage displays "Login" and "Register" buttons.
Test features: login, registration, real-time editing, AI suggestions, version control, and responsive UI.



Deploy on Render

Push to GitHub:
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/collaborative-editor.git
git push -u origin main


Create a Render Account:Sign up at render.com and connect your GitHub repository.

Create a Web Service:

Select the collaborative-editor repository and main branch.
Configure:
Name: collaborative-editor
Environment: Python
Region: Closest (e.g., Oregon)
Root Directory: Leave blank
Build Command: pip install -r requirements.txt
Start Command: gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 wsgi:app
Instance Type: Free


Click Create Web Service.


Create a PostgreSQL Database:

Click New > PostgreSQL.
Configure:
Name: collaborative-editor-db
Database: collaborative_editor
User: myuser
Region: Same as web service


Copy the Internal Database URL.


Set Environment Variables:In Render’s dashboard, add:

FLASK_ENV: production
SECRET_KEY: <random-string> (generate with python -c "import secrets; print(secrets.token_hex(16))")
DATABASE_URL: <postgresql-url> (from step 4)
LANGUAGE_TOOL_API: https://api.languagetool.org/v2/check


Deploy:

Trigger a deployment via Manual Deploy.
Access at https://collaborative-editor-u7r6.onrender.com.



Testing

Homepage: Verify / shows "Login" and "Register" buttons redirecting to /auth/login and /auth/register.
Auto-Save: Edit a document in /doc/editor/<doc_id>, refresh, and confirm content persists.
AI Suggestions: Type “This is a test with grammer error.” in the editor, verify suggestions (e.g., “grammar”) in #suggestions.
Real-Time Collaboration: Edit in two browsers, confirm WebSocket sync.
Version Control: Check doc/versions/<doc_id>, restore a version.
Responsive UI: Test on mobile.

Debugging

Local:
Check app.log:type app.log  # Windows
cat app.log   # Linux/Mac


Verify LanguageTool server: curl -X POST -d "text=This is a test with grammer error.&language=en-US" http://localhost:8081/v2/check


Render:
Check Render logs in the dashboard for errors (e.g., WebSocket or API issues).
Use browser DevTools (F12) for JavaScript and network errors.
Monitor LanguageTool API for 429 errors (rate limits).



Dependencies
See requirements.txt:

Flask==2.3.3
Flask-SocketIO==5.3.6
Flask-Login==0.6.3
Flask-SQLAlchemy==3.0.5
Flask-WTF==1.2.1
psycopg[binary]==3.2.2
python-socketio==5.11.2
requests==2.31.0
python-dotenv==1.0.1
gunicorn==22.0.0
email_validator==2.2.0
gevent==24.2.1
gevent-websocket==0.10.1

Notes

Avoid running gunicorn locally on Windows due to fcntl errors; use python run.py instead.
The free LanguageTool API (https://api.languagetool.org/v2/check) may have rate limits. Use a local server for development.
