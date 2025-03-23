import os
from googleapiclient.discovery import build
from gooogleapplicant.errors import HttpError
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

class YouTubeAPI:
  def __init__(self):
    