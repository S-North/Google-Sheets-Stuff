#!/usr/bin/python3

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from datetime import datetime, timedelta
from collections import defaultdict

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
client = gspread.authorize(creds)

gsheet = client.open('Python test data - cleaning').sheet1
col0 = gsheet.col_values(1)
col1 = gsheet.col_values(2)
col2 = gsheet.col_values(3)

unique_chores = []                                                              # create a list of unique chores in col2
for c in col2[1:]:
    if c not in unique_chores:
        unique_chores.append(c)

def unique_names():
    names = []                                                                  # create a list of unique names in col1
    for n in col1[1:]:
        if n not in names:
            names.append(n)
    return names

def get_list_minus_days(name, days):
    record = []
    records = []
    for d,n,c in zip(col0,col1,col2):                                           # create a set of columns to iterate over using zip
        if d != 'Timestamp':                                                    # exclude the first row headers
            date = datetime.strptime(d.split(' ').pop(0), '%d/%m/%Y')           # fornat the 1st column into a valid datetime type
            if (date > (datetime.today() - timedelta(days=days))) and (n == name):
                record = [d,n,c]                                                # create a list
                records.append(record)                                          # create a list of lists
    return records

def get_list_from_date(name, date):
    record = []
    records = []
    for d,n,c in zip(col0[1:],col1[1:],col2[1:]):                                           # create a set of columns to iterate over using zip
        # if d != 'Timestamp':                                                    # exclude the first row headers
        dd = datetime.strptime(d.split(' ').pop(0), '%d/%m/%Y')           # fornat the 1st column into a valid datetime type
        if (dd > date) and (n == name):
            record = [d,n,c]                                                # create a list
            records.append(record)                                          # create a list of lists
    return records

def get_categories_since_date(name, date):                                      # count of each chore for name since specified date
    tasks = defaultdict(int)                                                    # create a ditionary
    for d,n,c in zip(col0,col1,col2):
        if d != 'Timestamp':
            dd = datetime.strptime(d.split(' ').pop(0), '%d/%m/%Y')
            if (dd > date) and (n == name):
                tasks[c] += 1                                                   # create dict keys and count occurances
    return tasks

def get_earliest():                                                             # calc the most recent first entry of all participents
    earliest_dates = defaultdict(lambda : datetime.today())
    for n in unique_names():
        for d,n in zip(col0[1:],col1[1:]):
            date = datetime.strptime(d.split(' ').pop(0), '%d/%m/%Y')
            if earliest_dates[n] > date:
                earliest_dates[n] = date
    return (max(earliest_dates.values()))

def results_by_task(task, date):
    results = defaultdict(lambda : datetime.today())
    for name, chore in (name, chore for name, chore in zip(col0[1:],col1[1:]) if chore == task:
        print('{}, {}'.format(chore, name))



# pprint(get_list_from_date('Stuart', get_earliest()))
# pprint(get_list_minus_days('Stuart', 90))
# pprint(get_categories_since_date('Stuart', get_earliest()))
# pprint(unique_names())
# pprint(get_earliest())
pprint(results_by_task('Clean cooker top', get_earliest()))
