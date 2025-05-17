from fastapi import FastAPI
from utils.dataloader import companyLoader
from utils.scraper import Scraper
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await companyLoader()
    await asyncio.sleep(5)
    scraper = Scraper()
    await scraper.run()
    

def cronJob():
    return {"Hello": "World"}
