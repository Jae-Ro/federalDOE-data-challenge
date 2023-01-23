from codetest.db.database import DB
from codetest.db.models.people import People
from codetest.db.models.places import Places
import codetest.utils.log_utils as log_utils
import codetest.utils.io_utils as io_utils
from dotenv import load_dotenv
import os
load_dotenv()

class TestDatabaseModelsData:
    db = DB()
    db.create_engine('codetest')
    logger = log_utils.get_custom_logger('TestDatabaseModelsData')
    data_dir = "/data"
    if not os.path.exists(os.path.join(data_dir, 'people.csv')):
        data_dir = '../../data'
    
    def test_people_data_from_csv(self):
        """Function to read in data from csv, transform to People instance and check if valid
        """
        people = io_utils.get_people_from_csv(os.path.join(self.data_dir, 'people.csv'))
        for i, p in enumerate(people):
            assert isinstance(p, People)
    
    def test_places_data_from_csv(self):
        """Function to read in data from csv, transform to Places instance and check if valid
        """
        places = io_utils.get_places_from_csv(os.path.join(self.data_dir, 'places.csv'))
        for i, place in enumerate(places):
            assert isinstance(place, Places)

