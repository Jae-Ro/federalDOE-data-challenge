from codetest.db.models.places import Places
from codetest.db.models.people import People
import codetest.utils.log_utils as log_utils
from datetime import date
from typing import List

class TestDatabaseModelTypeValidation:
    logger = log_utils.get_custom_logger('TestDatabaseModels')

    def db_model_class_validator(self, DBModelClass, test_cases: List[dict], expected_results: List[bool]):
        """Function to take in a sqlalchemy mapped dataclass
        and validate instantion of test_cases and the expected result outcomes 

        Args:
            DBModelClass (_type_): database model class that represents sql table
            test_cases (List[dict]): test_cases mapped to fields of db model class
            expected_results (List[bool]): boolean expected result outcomes of if test case is valid
        """
        print()
        for i, test in enumerate(test_cases):
            res, msg = True, ""
            try:
                _ = DBModelClass(**test)
            except Exception as e:
                msg = f" -- {e}"
                res = False

            self.logger.debug(f"Test {i+1}/{len(test_cases)}{msg}")
            assert res == expected_results[i]
    
    def test_data_model_people(self):
        """Testing database model class - People
        """
        test_cases = [
            { 'given_name': 'Jae', 'family_name': 'Ro', 'date_of_birth': date.today(), 'place_of_birth': 'Boston' },
            { 'given_name': None, 'family_name': None, 'date_of_birth': None, 'place_of_birth': None },
            { 'given_name':'Jae', 'family_name': 'Ro', 'date_of_birth': 'January 23, 2023', 'place_of_birth': 'Boston' },
            { 'given_name': 1, 'family_name': 'Ro', 'date_of_birth': date.today(), 'place_of_birth': 'Boston' },
            { 'Given_name': 'Jae', 'family_name': 'Ro', 'date_of_birth': date.today(), 'place_of_birth': 'Boston' },
        ]
        expected_results = [
            True,
            True,
            False,
            False,
            False
        ]
        self.db_model_class_validator(People, test_cases, expected_results)

    
    def test_data_model_places(self):
        """Testing database model class - Places
        """
        test_cases = [
            { 'city': 'Springfield', 'county': 'Fairfax', 'country': 'USA' },
            { 'city': None, 'county': None, 'country': None },
            { 'city': 1, 'county': 'Fairfax', 'country': 'USA' },
            { 'City': 'Springfield', 'county': 'Fairfax', 'country': 'USA' },
            { 'Lity': 'Springfield', 'county': 'Fairfax', 'country': 'USA' },
        ]
        expected_results = [
            True,
            True,
            False,
            False,
            False
        ]
        self.db_model_class_validator(Places, test_cases, expected_results)
    