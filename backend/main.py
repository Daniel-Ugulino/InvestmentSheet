from fastapi import FastAPI
from utils.scraper import Scraper
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

    


