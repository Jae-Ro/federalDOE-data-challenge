from codetest.db.models.people import People
from codetest.db.models.places import Places
import os

class DatabaseConnector():
    def __init__(self) -> None:
        pass


    def get_db_creds(self) -> dict:
        """Function to get database credentials from environment  variables

        Returns:
            dict: dictionary of host, username, password credentials
        """
        # set default credentails based on env variables
        host = os.getenv('DB_HOST')
        username = os.getenv('DB_UN')
        password = os.getenv('DB_PW')

        return {"host": host, "username": username, "password": password}


    