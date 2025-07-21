# app/models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize db here

from .user import User
from .document import Document
from .version import Version