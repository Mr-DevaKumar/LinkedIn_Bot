import os
from dotenv import load_dotenv

load_dotenv()

# LinkedIn credentials
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

# Search parameters
SEARCH_URL = "https://www.linkedin.com/search/results/people/?keywords=recruiter&origin=SWITCH_SEARCH_VERTICAL"
CONNECTION_NOTE = "Hi {name}, I came across your profile and thought we might share common interests in the tech industry. I'd love to connect and learn from your experiences."

# Bot settings
MAX_CONNECTIONS = 10  # Limit to prevent rate limiting
SCROLL_PAUSE_TIME = 2
PAGE_LOAD_WAIT = 5