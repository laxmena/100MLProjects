#!/usr/bin/env python
# coding: utf-8

import requests
import os
import yaml
import zipfile
import pandas as pd
import datetime
import numpy as np
import pickle
from os import path
import csv


CRICSHEET_URL = 'https://cricsheet.org/downloads/ipl.zip'
TARGET_PATH = os.path.abspath(os.getcwd()) + '//data//ipl.zip'
MATCH_CSV_PATH = os.path.abspath(os.getcwd()) + '//data//match_data.csv'
DELIVERIES_CSV_PATH = os.path.abspath(os.getcwd()) + '//data//deliveries_data.csv'
PROCESSED_FILES_LOG = os.path.abspath(os.getcwd()) + '//data//processed.pkl'
CHUNK_SIZE = 128


def download_data():    
    """
    Description
    -----------
    Downloads data from Cricsheet website and saves in 
    the current working directory
    """
    r = requests.get(CRICSHEET_URL, stream=True)
    with open(TARGET_PATH, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
            fd.write(chunk)
            


def initialize():    
    """
    Description
    -----------
    Initalizes the python script to download and update 
    latest IPL match information.
    
    global variables
    ----------------
    ipl_zip    : Reference to downloaded IPL Data ZIP file
    match_list : List of files within ipl_zip, where each file 
        contains data of one IPL match 
    files_processed : Set Object, that contains list of all the 
        files that are already processed.
    matches_df : Pandas Dataframe, it creates and updates IPL Match 
        overview in MATCH_CSV_PATH
    match_id   : Unique ID that corresponds to each match record
    deliveries_df : Pandas Dataframe, creates and updates ball 
        by ball information of an IPL Match. 
    """
    global ipl_zip, match_list, files_processed, matches_df, match_id, deliveries_df
    download_data()
    ipl_zip = zipfile.ZipFile(TARGET_PATH)
    match_list = ipl_zip.namelist()
    print("Total Match Records: ", len(match_list))

    # Load Files Processed List
    if(path.isfile(PROCESSED_FILES_LOG) == False):
        with open(PROCESSED_FILES_LOG, "wb") as file_handle:
            pickle.dump({"README.txt"}, file_handle)

    with open(PROCESSED_FILES_LOG, "rb") as file_handle:
        files_processed = pickle.load(file_handle)
    
    # Load Match File Data
    matches_columns = ['dates','city','season','host_team','visiting_team', 'toss_winner','toss_decision','venue','result','winner','player_of_match']
    if(path.isfile(MATCH_CSV_PATH) == False):
        matches_df = pd.DataFrame(columns=matches_columns)
        match_id = int(0)
    else:
        matches_df = pd.read_csv(MATCH_CSV_PATH)
        match_id = int(matches_df['match_id'].max())
        
    # Load Deliveries File data
    deliveries_columns = ['batting_team','bowling_team','batsman','bowler','over','ball','non_striker','total_runs','batsman_runs','extras_runs']
    if(path.isfile(MATCH_CSV_PATH) == False):
        deliveries_df = pd.DataFrame(columns=deliveries_columns)
    else:
        deliveries_df = pd.read_csv(DELIVERIES_CSV_PATH)
    



def save_processed_files():
    """
    Description:
    ------------
    This method is called at the end after processing the data to
    store the newly created or updated records to memory.
    """
    with open(PROCESSED_FILES_LOG, "wb") as file_handle:
        pickle.dump(files_processed, file_handle)
    matches_df.to_csv (MATCH_CSV_PATH, index = False, header=True)
    deliveries_df.to_csv (DELIVERIES_CSV_PATH, index = False, header=True)



def get_data(obj, key):
    """
    Returns np.nan if the requested value is not 
    present withiin the object
    """
    try:
        if isinstance(key, list):
            for each in key:
                obj = obj[each]
            return obj
        else:
            if key in obj:
                return obj[key]
    except:
        print('ERROR: key: ',key, ' | obj: ', obj)
        return np.nan



def get_match_data(match_id, info):
    """
    Extracts information from the info object and returns 
    structured information about the match.
    
    Returns
    -------
    A dictionary with values for the following keys
    
    Keys:
    --------
    match_id : int, Unique ID associated with each IPL match
    dates : DateTime, Date of the match
    city : String, City where the match is played
    season : int, year the match is played
    host_team : str, name of the host team
    visiting_team : str, name of the visiting team
    toss_winner : str, name of the team which won the toss
    toss_decision : str, either 'bat' or 'field'
    venue : str, name of the cricket ground
    result : int, 0 - No Result, 1 - One team won, 2 - Tie
    winner : str, Name of the team which won
        In case of No result, 'no result'
        In case of Tie, Team which won the eliminator
    player_of_match : str, Name of player who won the 
        Man of the match award
    """
    
    data = {}

    data['match_id'] = int(match_id)

    data['dates'] = get_data(info, ['dates', 0])
    if(isinstance(data['dates'], datetime.date) != True):
        data['dates'] = datetime.datetime.strptime(data['dates'], '%Y-%m-%d')

    data['city'] = get_data(info,'city')
    data['season'] = data['dates'].year
    data['host_team'] = get_data(info,['teams', 0])
    data['visiting_team'] = get_data(info, ['teams', 1])
    data['toss_winner'] = get_data(info, ['toss', 'winner'])
    data['toss_decision'] = get_data(info, ['toss', 'decision'])
    data['venue'] = get_data(info, 'venue')
    if 'winner' in info['outcome']:
        data['winner'] = get_data(info, ['outcome','winner'])
        # Result : 0 - no result, 1 - winner, 2 - tie
        data['result'] = 1
        if(data['winner'] == 'no result'):
            data['result'] = 0

    elif 'eliminator' in info['outcome']:
            data['result'] = 2
            data['winner'] = get_data(info, ['outcome', 'eliminator'])
    else:
        data['winner'] = 'no result'
        data['result'] = 0

    if 'player_of_match' in info:
        data['player_of_match'] = get_data(info, ['player_of_match', 0])
    
    return data


def get_delivery_data(match_id, reader, batting_team, bowling_team):
    """
    Extract ball by ball information about a match and return a 
    detailed structured information about the match.
    
    Returns:
    --------
    A dictionary filled with values for following keys
    
    Keys:
    -----
    match_id : int, Unique ID associated with each IPL match
    batting_team : str, Name of the batting team
    bowling_team: str, Name of the bowling team
    over : int, Over associated with the record
    ball : int, ball number associated with the record
    batsman : str, Name of Batsman in strike
    bowler : str, Name of Bowler bowling the over
    non_striker : str, Name of the Non Striker Batsman
    total_runs : int, Total runs scored including extras for 
        the delivery
    batsman_runs : int, Runs scored by batsman
    extras_runs : int, Runs as extras for the given delivery
    wicket : int, either 0 or 1
        0 - No wicket has fallen in the given delivery
        1 - Wicket has fallen for the given delivery
    wicket_kind: Possible values: 'lbw', 'caught', 'bowled', 
        'run out', 'retired hurt', 'stumped', 'hit wicket',  
        'caught and bowled', 'obstructing the field'
    wicket_fielders : List, list of fielders involved
    player_out : str, Name of the player that got out
    """
    
    data = {}
    delivery = list(reader.keys())[0]
    delivery_obj = get_data(reader, delivery)
    data['match_id'] = match_id
    data['batting_team'] = batting_team
    data['bowling_team'] = bowling_team
    data['over'], data['ball'] = str(delivery).split('.')
    data['over'],data['ball'] = int(data['over']),int(data['ball'])
    data['batsman'] = get_data(delivery_obj, 'batsman')
    data['bowler'] = get_data(delivery_obj, 'bowler')
    data['non_striker'] = get_data(delivery_obj, 'non_striker')
    data['total_runs'] = get_data(delivery_obj, ['runs', 'total'])
    data['batsman_runs'] = get_data(delivery_obj, ['runs', 'batsman'])
    data['extras_runs'] = get_data(delivery_obj, ['runs', 'extras'])
    
    if 'wicket' in delivery_obj:
        data['wicket'] = 1
        data['wicket_kind'] = get_data(delivery_obj, ['wicket', 'kind'])
        data['wicket_player_out'] = get_data(delivery_obj, ['wicket', 'player_out'])
        if 'fielders' in delivery_obj['wicket']:
            data['wicket_fielders'] = get_data(delivery_obj, ['wicket', 'fielders'])
    else:
        data['wicket'] = 0
    return data
    
    
def get_deliveries_data(match_id, reader): 
    collection = []
    
    innings = reader['innings']
    first_innings = get_data(innings, [0, '1st innings'])
    second_innings = get_data(innings, [1, '2nd innings'])
    
    teams = get_data(reader, ['info', 'teams'])
    if((get_data(reader, ['info', 'toss', 'winner']) == teams[0] and get_data(reader, ['info', 'toss', 'decision']) == 'bat') or 
       (get_data(reader, ['info', 'toss', 'winner']) == teams[1] and get_data(reader, ['info', 'toss', 'decision']) == 'field')):
        team1, team2 = teams[0], teams[1]
    else:
        team1, team2 = teams[1], teams[0]
    
    if isinstance (first_innings, dict):
        for each_delivery in get_data(first_innings, 'deliveries'):
            collection.append(get_delivery_data(match_id, each_delivery, team1, team2))
    if isinstance(second_innings, dict):
        for each_delivery in get_data(second_innings, 'deliveries'):
            collection.append(get_delivery_data(match_id, each_delivery, team2, team1))
        
    return collection




initialize()

for match in match_list:
    if(match in files_processed):
        continue

    match_id = int(match_id + 1)

    with ipl_zip.open(match) as yamlfile:
        reader = yaml.safe_load(yamlfile)

        print(match_id,". Processing File : ", match)
        info = reader['info']
        
        match_data = get_match_data(match_id, info)
        matches_df = matches_df.append([match_data])
        
        deliveries_data = get_deliveries_data(match_id, reader)
        deliveries_df = deliveries_df.append(deliveries_data)
        
        files_processed.add(match)

save_processed_files()




