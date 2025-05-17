from utils.connection import db
import os
import json
from models.company import Company 
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            
        companies = list(db.company.find())
        
        if len(companies) > 0:
            print("Company data already exists in the database.")
            return
    
        for item in raw_data:
            try:
                company = Company(**item)      
                companies.append(company.model_dump(by_alias=True))
            except Exception as e:
                print(f"Validation error: {e} for item: {item}")

        if companies:
            db.company.insert_many(companies)
            print(f"{len(companies)} companies inserted.")
        else:
            print("No valid company data to insert.")
    else:
        print(f"File {file_path} not found.")
