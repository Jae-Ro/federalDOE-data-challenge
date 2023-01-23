from codetest.db.database import DB
from codetest.db.models.people import People
from codetest.db.models.places import Places
import codetest.utils.log_utils as log_utils
from datetime import date
from dotenv import load_dotenv
load_dotenv()


class TestDatabaseQuery:
    db = DB()
    db.create_engine('codetest')
    logger = log_utils.get_custom_logger('TestDatabaseQuery')

    def test_query_people_table(self):
        """Function to test querying people table in database
        """
        # configure test data
        results = self.db.select_one('people')
        if len(results) < 1:
            self.db.insert_iterative([
                People(
                    given_name="Jae", 
                    family_name="Ro", 
                    date_of_birth= date.today(), 
                    place_of_birth="Springfield"
                )
            ])
            results = self.db.select_one('people')
        self.logger.debug(f"{results[0]}")
        # assertion tests
        assert len(results) == 1
        assert isinstance(results[0], People)
        # cleanup
        id = results[0].id
        self.db.delete_by_id('people', id)


    def test_query_places_table(self):
        """Function to test querying places table in database
        """
        # configure test data
        results = self.db.select_one('places')
        if len(results) < 1:
            self.db.insert_iterative([
                Places(
                    city="Springfield",
                    county="Fairfax",
                    country="United States"
                )
            ])
            results = self.db.select_one('places')
        self.logger.debug(f"{results[0]}")
        # assertion tests
        assert len(results) == 1
        assert isinstance(results[0], Places)
        # cleanup
        id = results[0].id
        self.db.delete_by_id('places', id)


    


