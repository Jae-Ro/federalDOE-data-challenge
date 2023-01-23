# from codetest.db.models.people import People
# from codetest.db.models.places import Places
import codetest.utils.log_utils as log_utils
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os
from typing import List

logger = log_utils.get_custom_logger("DBLogger")

class DB:
    """Singleton pattern"""
    __instance = None
    
    def __new__(cls, *args, **kwargs):
        """Class method to return single instance 
        of class if already instantiated

        Returns:
            DB: instance of DB class
        """
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        """Initialization method
        """
        self.engine = None

    def get_db_creds(self) -> dict:
        """Instance method to get database credentials from environment  variables

        Returns:
            dict: dictionary of host, username, password credentials
        """
        # set default credentails based on env variables
        logger.debug("Obtaining DB Credentials")
        host = os.getenv('DB_HOST')
        username = os.getenv('DB_UN')
        password = os.getenv('DB_PW')
        creds = { "host": host, "username": username, "password": password }
        # check for null fields
        null_fields = [k for k,v in creds.items() if v is None]
        if len(null_fields) > 0: logger.warning(f"The following DB Credential fields were not found: {null_fields}")

        return creds
    
    def create_engine(self, db_name:str):
        """Instance method to create sqlalchemy db engine based on a given database name

        Args:
            db_name (str): database name
        """
        creds = self.get_db_creds()
        self.engine = create_engine(f"mysql://{creds['username']}:{creds['password']}@{creds['host']}/{db_name}")
    

    def bulk_insert(self, data:List[any]):
        with Session(self.engine) as session, session.begin():
            success = 0
            for i, obj in enumerate(data):
                try:
                    session.add(obj)
                except Exception as e:
                    logger.error(f"Encountered Error When attempting to insert {obj}.\n\t{e}")
                    raise e
                success +=1
        logger.debug(f"Successfully Inserted {success}/{len(data)} into {data[0].__tablename__} Table")
    

if __name__=="__main__":
    db1 = DB()
    db2 = DB()
    db3 = DB()
    db4 = DB()
    db3.create_engine('test')
    print(db1==db2==db3)

