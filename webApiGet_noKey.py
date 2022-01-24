"""
author: evan fedorko, evanjfedorko@gmail.com
date: 3/2019

This script was written for a project where we needed to map and further process
(with GIS software) a specific data point stored in a DB by NREL. I accessed it using
this script and created the output
"""

import requests
import pandas as pan
import csv
import time

# VARIABLES #

# API service URL
URL = "https://developer.nrel.gov/api/pvwatts/v6.json?parameters"
# my NREL API key
KEY = 'Your API key goes here.'
# excel file of sites
sites = 'CountyCentroids_test.xlsx'
# dict of sheets to loop through, waiting with time.sleep between each
sheets = ['Sheet1', 'Sheet2', 'Sheet3', 'Sheet4']
# output file
output = 'out.csv'


def process(dataframe):
    for index, row in dataframe.iterrows():
        in_lat = row.cent_lat
        in_lon = row.cent_lon
        in_oid = row.FIPS_Num
        # parameters of the API request per API specification
        PARAMS = {'api_key': KEY, 'system_capacity': 1, 'module_type': 2, 'losses': 20, 'array_type': 2,
                  'tilt': 0, 'azimuth': 180, 'lat': in_lat, 'lon': in_lon, 'dataset': 'nsrdb', 'radius': 0,
                  'timeframe': 'monthly', 'dc_ac_ratio': 1.2, 'gcr': 0.4, 'inv_eff': 96}
        call(PARAMS, in_oid)


def call(data, oid):
    # produces a request object
    r = requests.get(url=URL, params=data)
    # returns the request json data
    data = r.json()
    # read the parameter we need, which is nested
    value = data["outputs"]["ac_annual"]
    write(value, oid)


def write(data, oid):
    with open(output, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow([str(oid), str(data)])


# THIS IS THE MAIN PROGRAM
# running a single request through this script takes about 1.6 seconds
# 1,000 will take roughly 27 minutes
for sheet in sheets:
    sites_df = pan.read_excel(sites, sheet_name=sheet, index_col=0)
    process(sites_df)
    print("asleep...")
    time.sleep(3660)
    print("awake!")
