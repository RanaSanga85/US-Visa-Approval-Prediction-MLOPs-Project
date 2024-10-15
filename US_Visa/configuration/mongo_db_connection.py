import sys
from US_Visa.exception import USVisaException
from US_Visa.logger import logging

import os
from US_Visa.constants import DATABASE_NAME, MONGODB_URL_KEY
import pymongo
import certifi

ca = certifi.where()

class MongoDBClient:
    """
    Class Name  : MongoDBClient
    Description : This class establishes a connection to a MongoDB database.

    Output      : Connection to the MongoDB database.
    On Failure  : Raises a USVisaException.
    """
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                #mongo_db_url = os.environ[MONGODB_URL_KEY]  # Ensures env var exists
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB connection successful")
        except KeyError as e:
            raise USVisaException(f"Environment key: {MONGODB_URL_KEY} is not set.", sys)
        except Exception as e:
            raise USVisaException(e, sys)
      