import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_URI = os.environ.get('MONGODB_URI')
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')


config = Config()