from utils.connection import db
from models.company import Company

class companyService:
    
    def __init__(self):
        self.db = db.company
        
    # async def get_all(self):
        
    async def findById(self, id):
        """
        Find a company by its ID.
        """
        try:
            company = await self.db.find_one({"_id": id})
            if company:
                return Company(**company)
            else:
                return None
        except Exception as e:
            print(f"Error finding company by ID: {e}")
            return None
        
    async def getAll(self):
        """
        Get all companies from the database.
        """
        try:
            companies = list(self.db.find())
            return [Company(**company) for company in companies]
        except Exception as e:
            print(f"Error retrieving all companies: {e}")
            return []
    