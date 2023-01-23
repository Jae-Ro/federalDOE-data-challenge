import csv, json
from typing import List


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


def write_json(data:dict, json_fpath:str):
    """_summary_

    Args:
        data (dict): _description_
        json_fpath (str): _description_
    """
    with open(json_fpath, 'w') as fh:
        json.dump(data, fh, separators=(',', ':'))