# app/services/ai_suggestions.py
import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

def get_grammar_suggestions(text):
    api_url = os.getenv('LANGUAGE_TOOL_API', 'https://api.languagetool.org/v2/check')
    try:
        response = requests.post(api_url, data={
            'text': text,
            'language': 'en-US'
        }, timeout=5)
        response.raise_for_status()
        data = response.json()
        suggestions = []
        for match in data.get('matches', []):
            message = match.get('message', '')
            replacements = match.get('replacements', [])
            suggestion = {'message': message, 'replacements': [r.get('value', '') for r in replacements]}
            suggestions.append(suggestion)
        logger.info(f"Fetched {len(suggestions)} suggestions for text: {text[:50]}...")
        return suggestions
    except requests.RequestException as e:
        logger.error(f"Failed to fetch suggestions: {e}")
        return [{'message': 'Error fetching suggestions. Please try again later.'}]