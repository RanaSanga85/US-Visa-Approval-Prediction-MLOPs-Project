from US_Visa.configuration.mongo_db_connection import MongoDBClient
from US_Visa.constants import DATABASE_NAME
from US_Visa.exception  import USVisaException
import pandas as pd
from typing import Optional
import numpy as np
import sys

class USVisaData:
    """
    this class help to export entire mongo db recorde as pandas dataframe
    """

    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise USVisaException(e, sys)
        
    def export_collection_as_dataframe(self, collection_name:str, database_name:Optional)
        