from codetest.db.models.people import People
from codetest.db.models.places import Places
from datetime import date
from typing import List
import csv, json

def read_csv_to_records(csv_path:str) -> List[dict]:
    """_summary_

    Args:
        csv_path (str): _description_

    Returns:
        List[dict]: _description_
    """
    records = []
    with open(csv_path) as csv_file:
        reader = csv.reader(csv_file)
        headers = next(reader)
        headers = [h.strip() for h in headers]
        for row in reader: 
            rec = {}
            for i in range(len(row)):
                rec[headers[i]] = row[i].strip()
            records.append(rec)
    
    return records


def read_json(json_fpath:str) -> dict:
    """_summary_

    Args:
        json_fpath (str): _description_

    Returns:
        dict: _description_
    """
    with open(json_fpath, 'r') as fh:
        data = json.load(fh)
    return data


def write_json(data:dict, json_fpath:str):
    """_summary_

    Args:
        data (dict): _description_
        json_fpath (str): _description_
    """
    with open(json_fpath, 'w') as fh:
        json.dump(data, fh, separators=(',', ':'))


def get_people_from_dict_records(people_records:dict) -> List[People]:
    """_summary_

    Args:
        people_records (dict): _description_

    Returns:
        List[People]: _description_
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


def get_places_from_dict_records(places_records:dict) -> List[People]:
    """_summary_

    Args:
        people_records (dict): _description_

    Returns:
        List[People]: _description_
    """
    return [Places(**place) for place in places_records]


def get_people_from_csv(csv_path:str) -> List[People]:
    """_summary_

    Args:
        csv_path (str): _description_

    Returns:
        List[People]: _description_
    """
    records = read_csv_to_records(csv_path)
    res = get_people_from_dict_records(records)
    return res


def get_places_from_csv(csv_path:str) -> List[People]:
    """_summary_

    Args:
        csv_path (str): _description_

    Returns:
        List[People]: _description_
    """
    records = read_csv_to_records(csv_path)
    res = get_places_from_dict_records(records)
    return res
