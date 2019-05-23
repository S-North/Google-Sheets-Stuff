#!/usr/bin/python3

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from datetime import datetime, timedelta
from collections import defaultdict

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
client = gspread.authorize(creds)

sheet = client.open('Python test data - cleaning').sheet1
col0 = sheet.col_values(1)
col1 = sheet.col_values(2)
col2 = sheet.col_values(3)

def get_list(name, days):
    record = []
    records = []
    for d,n,c in zip(col0,col1,col2):                                           # create a set of columns to iterate over using zip
        if d != 'Timestamp':                                                    # exclude the first row headers
            date = datetime.strptime(d.split(' ').pop(0), '%d/%m/%Y')           # fornat the 1st column into a valid datetime type
            if (date > (datetime.today() - timedelta(days=days))) and (n == name):
                record = [d,n,c]                                                # create a list
                records.append(record)                                          # create a list of lists
    return records

def get_categories(name, days):
    tasks = defaultdict(int)                                                    # create a ditionary
    for d,n,c in zip(col0,col1,col2):
        if d != 'Timestamp':
            date = datetime.strptime(d.split(' ').pop(0), '%d/%m/%Y')
            if date > (datetime.today() - timedelta(days=days)) and (n == name):
                tasks[c] += 1                                                   # create dict keys and count occurances
    return tasks

pprint(get_list('Stuart', 90))
pprint(get_categories('Stuart', 90))
