from codetest.db.models.people import People
from codetest.db.models.places import Places
from datetime import date
from typing import List
import csv, json

def read_csv_to_records(csv_path:str) -> List[dict]:
    """Fucntion to read in data from csv file
    and return list of dictionary records

    Args:
        csv_path (str): path to csv file

    Returns:
        List[dict]: data dictionary records
    """
    records = []
    with open(csv_path) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader: records.append(row)
    
    return records


def read_json(json_fpath:str) -> dict:
    """Function to read json file 
    and return dictionary equivalent

    Args:
        json_fpath (str): path to .json file

    Returns:
        dict: python dictionary equivalent to json file
    """
    with open(json_fpath, 'r') as fh:
        data = json.load(fh)
    return data


def write_json(data:dict, json_fpath:str):
    """Function to take in dictionary and write to
    equivalent json file store in given json_fpath

    Args:
        data (dict): data dictionary to be written
        json_fpath (str): path to desired .json file
    """
    with open(json_fpath, 'w') as fh:
        json.dump(data, fh, separators=(',', ':'))


def get_people_from_dict_records(people_records:List[dict]) -> List[People]:
    """Function to convert list of dictionaries with fields
    that map to People class and return a list of People instances

    Args:
        people_records (List[dict]): list of dicts mapped to People class

    Returns:
        List[People]: list of People instances
    """
    # Transform Data into appropriate data classes
    people_li = []
    for p_dict in people_records:
        # get y, m, d strings
        year, month, day = p_dict['date_of_birth'].split("-")
        # validate length of each date component
        assert len(year) == 4 and len(month) == 2 and len(day) == 2
        # create date object
        p_dict['date_of_birth'] = date(int(year), int(month), int(day))
        # create instance of dataclass and append to list
        people_li.append(People(**p_dict))
    
    return people_li


def get_places_from_dict_records(places_records:List[dict]) -> List[Places]:
    """Function to convert list of dictionaries with fields
    that map to Places class and return a list of Places instances

    Args:
        places_records (List[dict]): list of dicts mapped to Places class

    Returns:
        List[People]: list of Places instances
    """
    return [Places(**place) for place in places_records]


def get_people_from_csv(csv_path:str) -> List[People]:
    """Function to get list of People instances from csv file
    with columns that map to the People class

    Args:
        csv_path (str): _description_

    Returns:
        List[People]: list of People instances
    """
    records = read_csv_to_records(csv_path)
    res = get_people_from_dict_records(records)
    return res


def get_places_from_csv(csv_path:str) -> List[Places]:
    """Function to get list of Places instances from csv file
    with columns that map to the Places class

    Args:
        csv_path (str): path to csv file

    Returns:
        List[Places]: list of Places instances
    """
    records = read_csv_to_records(csv_path)
    res = get_places_from_dict_records(records)
    return res
