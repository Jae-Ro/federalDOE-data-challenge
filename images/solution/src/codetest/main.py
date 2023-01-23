#!/usr/bin/env python

import csv
import json
import sqlalchemy
import pandas as pd
from codetest.db.database import DB
from codetest.db.models.people import People
from codetest.db.models.places import Places
import codetest.utils.log_utils as log_utils
import argparse
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()


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

    # load csv into dataframe and convert to records
    df_people = pd.read_csv(fpath_people)
    df_places = pd.read_csv(fpath_places)
    people = df_people.to_dict('records')
    places = df_places.to_dict('records')
    
    # Transform Data into appropriate data classes
    people_li = []
    for p_dict in people:
        year, month, day = p_dict['date_of_birth'].split("-")
        assert len(year) == 4 and len(month) == 2 and len(day) == 2
        p_dict['date_of_birth'] = date(int(year), int(month), int(day))
        people_li.append(People(**p_dict))
    
    places_li = [Places(**place) for place in places]

    # Insert Data into Relevant Tables
    db.bulk_insert(people_li)
    db.bulk_insert(places_li)

    logger.info(f"Complete!")


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Codetest Solution')
    parser.add_argument('--data_dir', default="/data", type=str, help="path to directory where data file I/O will happen")
    args = parser.parse_args()
    args = vars(args)
    run(args)