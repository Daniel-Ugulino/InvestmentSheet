from utils.connection import db
import os
import json
from models.company import Company
from utils.scraper import Scraper
from service.shares import sharesService
from service.company import companyService
from utils.email_sender import EmailSender
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sharesService = sharesService()
companyService = companyService()

async def companyLoader():
    """
    Load company data into the database using the Company model.
    """

    file_path = os.path.join(os.path.dirname(__file__), "../data/data.json")

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            raw_data = json.load(file)

        if "company" not in db.list_collection_names():
            db.create_collection("company")
            
        companies = await companyService.getAll()
        
        if len(companies) > 0:
            print("Company data already exists in the database.")
            return companies
        
        companies_dump = []
        
        for item in raw_data:
            try:
                company = Company(**item)      
                companies_dump.append(company.to_dump())
                companies.append(company)
            except Exception as e:
                print(f"Validation error: {e} for item: {item}")

        if companies:
            await companyService.createMany(companies_dump)
            print(f"{len(companies_dump)} companies inserted.")
        else:
            print("No valid company data to insert.")
    else:
        print(f"File {file_path} not found.")
        
    return companies

async def sharesLoader(companies):
    scraper = Scraper()
    shares = await scraper.run(companies)
    await sharesService.createMany(shares)
    shares_file = scraper.shares_csv(shares)
    EmailSender().send_email(
        recipient='danielugulino46@gmail.com',
        subject="Data Loader Completed",
        body=f"{len(shares)} shares loaded successfully.",
        attachments=[shares_file]
    )

async def runLoader():
    while True:
        companies = await companyLoader() 
        await sharesLoader(companies)   

if __name__ == "__main__":
    asyncio.run(runLoader())
    