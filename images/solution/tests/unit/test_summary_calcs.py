import codetest.main as codetest_main
from codetest.db.database import DB
import codetest.utils.log_utils as log_utils
from datetime import date
import os


class TestSummaryCalcs:
    db = DB()
    db.create_engine('codetest')
    logger = log_utils.get_custom_logger('TestSummaryCalcs')
    people = [
        {
            'given_name': 'John',
            'family_name': 'Smith',
            'date_of_birth': '1990-01-02',
            'place_of_birth': 'Springfield'
        },
        {
            'given_name': 'Mark',
            'family_name': 'Smith',
            'date_of_birth':'1990-02-02',
            'place_of_birth': 'Beijing'
        },
        {
            'given_name': 'Rachel',
            'family_name': 'Smith',
            'date_of_birth': '1990-03-02',
            'place_of_birth': 'Beijing'
        },
        {
            'given_name': 'Rachel',
            'family_name': 'Smith',
            'date_of_birth': '1990-02-02',
            'place_of_birth': 'Beijing'
        }
    ]
    places = [
        {'city': 'Springfield', 'county': "Fairfax", 'country': 'United States'},
        {'city': 'Beijing', 'county': 'Yanqing', 'country': 'China'}
    ]

    expected_a = { 'United States': 1, 'China': 3 }
    expected_b = { 'Yanqing': 2 }

    def test_count_people_by_country(self):
        """Function to test the count_people_by_country function in codetest
        """
        res = codetest_main.count_people_by_country(
            self.people, 
            self.places
        )
        assert self.expected_a == res

    def test_find_most_common_birth_month_by_county(self):
        """Function to test the find_most_common_birth_month_by_county function in codetest
        """
        res = codetest_main.find_most_common_birth_month_by_county(
            self.people, 
            self.places,
            target_country='China'
        )
        assert self.expected_b == res
