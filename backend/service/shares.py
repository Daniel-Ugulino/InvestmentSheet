from models.shares import Shares
from utils.connection import db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class sharesService:
    def __init__(self):
        if "shares" not in db.list_collection_names():
            db.create_collection("shares")
        self.db = db.shares
    
    async def findById(self, id):
        try:
            share = self.db.find_one({"_id": id})
            if share:
                return Shares(**share)
            else:
                return None
        except Exception as e:
            print(f"Error finding share by ID: {e}")
            return None
    
    async def getAll(self):
        try:
            shares = self.db.find().to_list(length=None)
            return [Shares(**share) for share in shares]
        except Exception as e:
            print(f"Error retrieving all shares: {e}")
            return []
        
    # async def getAllByCompanyId(self):
        
    async def getAllByPeriod(self, start, end, csv = False):
        try:
            shares = self.db.find({
                "insertedAt": {
                    "$gte": start,
                    "$lte": end
                }
            })
            shares = [Shares(**share) for share in shares]
            return [Shares(**share) for share in shares]
        except Exception as e:
            print(f"Error retrieving all shares: {e}")
            return []
        
    
    
    async def create(self, share):
        try:
            data = share.model_dump(by_alias=True)
            self.db.insert_one(data)
            return share
        except Exception as e:
            logger.info(f"Error creating share: {e}")
            return None

    async def createMany(self, shares):
        try:
            print(f"Inserting {len(shares)} shares")
            self.db.insert_many(shares)
            return shares
        except Exception as e:
            logger.info(f"Error creating share: {e}")
            return None