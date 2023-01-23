from codetest.db.models.people import People
from codetest.db.models.places import Places
import codetest.utils.log_utils as log_utils
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typing import List
import os


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
        self.db_name = None
        self.table_types = {
            'people': People,
            'places': Places
        }

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
        connection_str = f"mysql://{creds['username']}:{creds['password']}@{creds['host']}/{db_name}"
        self.engine = create_engine(f"mysql://{creds['username']}:{creds['password']}@{creds['host']}/{db_name}")
        self.db_name = db_name

    def select_one(self, table_name:str) -> List[any]:
        """_summary_

        Args:
            table_name (str): _description_

        Returns:
            List[any]: _description_
        """
        result = []
        data_class = self.table_types[table_name]
        with Session(self.engine) as session:
            result = session.query(data_class).limit(1).all()
        if len(result) >0: logger.debug(f"Successfully Retreived: {len(result)} Row from '{table_name}' Table")
        return result
    
    def delete_by_id(self, table_name:str, id:any):
        """_summary_

        Args:
            table_name (str): _description_
            id (any): _description_
        """
        data_class = self.table_types[table_name]
        with Session(self.engine) as session, session.begin():
            res = session.get(data_class, id)
            session.delete(res)
            if len(session.deleted) > 0:
                logger.debug(f"Successfully Deleted 1 Row from '{table_name}' Table")
        return res
    
    def truncate_table(self, table_name:str) -> int:
        """_summary_

        Args:
            table_name (str): _description_

        Returns:
            int: _description_
        """
        data_class = self.table_types[table_name]
        with Session(self.engine) as session, session.begin():
            num_rows_deleted = session.query(data_class).delete()
            if num_rows_deleted > 0:
                logger.debug(f"Successfully Deleted {num_rows_deleted} Row(s) from '{table_name}' Table")
        return num_rows_deleted

    def bulk_insert(self, data:List[any]):
        """_summary_

        Args:
            data (List[any]): _description_

        Raises:
            e: _description_
        """
        with Session(self.engine) as session, session.begin():
            success = 0
            for i, obj in enumerate(data):
                try:
                    session.add(obj)
                except Exception as e:
                    logger.error(f"Encountered Error When attempting to insert {obj}.\n\t{e}")
                    raise e
                else: success +=1
        logger.debug(f"Successfully Inserted {success}/{len(data)} into {data[0].__tablename__} Table")
    

if __name__=="__main__":
    db1 = DB()
    db2 = DB()
    db3 = DB()
    db4 = DB()
    db3.create_engine('test')
    print(db1==db2==db3)

