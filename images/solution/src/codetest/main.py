#!/usr/bin/env python
from codetest.db.database import DB
from codetest.db.models.people import People
from codetest.db.models.places import Places
import codetest.utils.log_utils as log_utils
import codetest.utils.io_utils as io_utils
from dotenv import load_dotenv
from typing import List, Tuple
import os, argparse
load_dotenv()

def count_people_by_country(people:List[dict], places:List[dict]) -> dict:
    """Function to count number of people born in a country give people and places dict records

    Args:
        people (List[dict]): list of dictionaries of people data read from csv (note: dob is string not date)
        places (List[dict]): list of dictionarise of places data read from csv

    Notes:
    - Assumes no 2 countries can have the same city name given that 
    the only way to identify a person's location is by the city of birth
    and the prompt is asking to count people born by country

    Returns:
        dict: dictionary representing { <country: str>: <num people born in country: int> }
    """
    # Time Complexity - O(Places + People)
    count_dict, city2country = {}, {}
    for p_dict in places:
        city, county, country = p_dict['city'], p_dict['county'], p_dict['country']
        if city not in city2country:
            city2country[city] = country
    
    for p_dict in people:
        city = p_dict['place_of_birth']
        country = city2country[city]
        count_dict[country] = count_dict.get(country, 0) + 1
    
    return count_dict


def find_most_common_birth_month_by_county(
    people:List[dict], 
    places:List[dict], 
    target_country:str="Northern Ireland"
    ) -> dict:
    """Function to find the most common birth month by county for a target country

    Args:
        people (List[dict]): list of dictionaries of people data read from csv (note: dob is string not date)
        places (List[dict]): list of dictionarise of places data read from csv
        target_country (str, optional): target country to run algorithm on. Defaults to "Northern Ireland".

    Returns:
        dict: dictionary representing { <county: str>: <most common birth month: int> }
    """
    # Time Complexity - O(Places + People + Num Counties in Target Country)
    count_dict, city2county, res_dict = {}, {}, {}
    for p_dict in places:
        city, county, country = p_dict['city'], p_dict['county'], p_dict['country']
        if country != target_country: continue
        if city not in city2county: city2county[city] = county
    
    for p_dict in people:
        city = p_dict['place_of_birth']
        if city not in city2county: continue
        county = city2county[city]
        # birthday string parsing - Y, m, d
        _, month, _ = p_dict['date_of_birth'].split("-")
        if county not in count_dict: count_dict[county] = {}
        count_dict[county][month] = count_dict[county].get(month, 0) + 1
        curr_count = count_dict[county][month]

        if county not in res_dict:
            res_dict[county] = {"month": None, "count": 0}

        res_count = res_dict[county]['count']
        if curr_count > res_count:
            res_dict[county] = {"month": int(month), "count": curr_count }
        
    return { k: v['month'] for k, v in res_dict.items() }


def run(args:dict) -> Tuple[dict, dict]:
    """Top-Level Runner Function

    Args:
        args (dict): dictionary of argparse args

    Returns:
        Tuple[dict, dict]: report dicts of count_people_by_country, find_most_common_birth_month_by_county
    """

    # Create logger
    logger = log_utils.get_custom_logger("CodetestRun")
    logger.info(f"---------- [START] Data Load and Summary Calc for People and Places! ----------")
    try:
        # Instantiate DB
        logger.info('Creating database engine...')
        db = DB()
        db.create_engine('codetest')

        # Setup filepaths
        data_dir = args['data_dir']
        fpath_people = os.path.join(data_dir, 'people.csv')
        fpath_places = os.path.join(data_dir, 'places.csv')

        # load csv and convert to records
        logger.info('Reading Data from CSV files...')
        people = io_utils.read_csv_to_records(fpath_people)
        places = io_utils.read_csv_to_records(fpath_places)

        # Summarize Data -- program end
        logger.info('Calculating Summary Stats...')
        report_a = count_people_by_country(people, places)
        report_b = find_most_common_birth_month_by_county(people, places)

        # Write sumary jsons to file
        logger.info('Writing Summary Stats to Json Files...')
        io_utils.write_json(report_a, os.path.join(data_dir, "summary_output.json"))
        io_utils.write_json(report_b, os.path.join(data_dir, "summary_output_extra.json"))

        # Get list of People and Places instances 
        logger.info('Transforming Data into ORM Table Dataclasses...')
        people_li = io_utils.get_people_from_dict_records(people)
        places_li = io_utils.get_places_from_dict_records(places)

        # Insert instances of People and Places into DB
        logger.info('Inserting ORM Table Dataclasses into Database...')
        db.bulk_insert(people_li)
        db.bulk_insert(places_li)

    except Exception as e:
        # graceful exit
        logger.error(e)
        report_a, report_b = None, None

    logger.info(f"---------- [END] Data Load and Summary Calc for People and Places! ----------")
    return report_a, report_b


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Codetest Solution')
    parser.add_argument('--data_dir', default="/data", type=str, help="path to directory where data file I/O will happen")
    args = parser.parse_args()
    args = vars(args)
    run(args)