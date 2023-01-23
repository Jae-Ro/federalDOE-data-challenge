#!/usr/bin/env python
from codetest.db.database import DB
from codetest.db.models.people import People
from codetest.db.models.places import Places
import codetest.utils.log_utils as log_utils
import codetest.utils.io_utils as io_utils
from datetime import date
from dotenv import load_dotenv
from typing import List
import os, argparse
load_dotenv()


def count_people_places(people:List[dict], places:List[dict]) -> dict:
    """_summary_

    Args:
        people (List[dict]): _description_
        places (List[dict]): _description_

    Notes:
    - Assumes no 2 countries can have the same city name given that 
    the only way to identify a person's location is by the city of birth
    and the prompt is asking to count people born by country

    Returns:
        dict: _description_
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
    """_summary_

    Args:
        people (List[dict]): _description_
        places (List[dict]): _description_
        target_country (str, optional): _description_. Defaults to "Northern Ireland".

    Returns:
        dict: _description_
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


def run(args:dict):

    # Create logger
    logger = log_utils.get_custom_logger("Main")

    # Instantiate DB
    db = DB()
    db.create_engine('codetest')

    # Setup filepaths
    data_dir = args['data_dir']
    fpath_people = os.path.join(data_dir, 'people.csv')
    fpath_places = os.path.join(data_dir, 'places.csv')

    # load csv and convert to records
    people = io_utils.read_csv_to_records(fpath_people)
    places = io_utils.read_csv_to_records(fpath_places)

    # Summarize Data -- program end
    report_a = count_people_places(people, places)
    report_b = find_most_common_birth_month_by_county(people, places)

    # Write sumary jsons to file
    io_utils.write_json(report_a, os.path.join(data_dir, "summary_output.json"))
    io_utils.write_json(report_b, os.path.join(data_dir, "summary_output_extra.json"))

    # Transform Data into appropriate data classes
    people_li = []
    for p_dict in people:
        # get y, m, d strings
        year, month, day = p_dict['date_of_birth'].split("-")
        # validate length of each date component
        assert len(year) == 4 and len(month) == 2 and len(day) == 2
        # create date object
        p_dict['date_of_birth'] = date(int(year), int(month), int(day))
        # create instance of dataclass and append to list
        people_li.append(People(**p_dict))
    
    places_li = [Places(**place) for place in places]

    # Insert Data into Relevant Tables
    # db.bulk_insert(people_li)
    # db.bulk_insert(places_li)


    logger.info(f"Complete!")


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Codetest Solution')
    parser.add_argument('--data_dir', default="/data", type=str, help="path to directory where data file I/O will happen")
    args = parser.parse_args()
    args = vars(args)
    run(args)