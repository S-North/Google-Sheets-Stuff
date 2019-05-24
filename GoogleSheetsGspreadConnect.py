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

# get a list of unique values in the "chores" cloumn
def unique_chores():
    chores = []
    for c in col2[1:]:
        if c not in chores:
            chores.append(c)
    return chores

# get a list of unique values in the "names" cloumn
def unique_names():
    names = []
    for n in col1[1:]:
        if n not in names:
            names.append(n)
    return names

#return a list of all columns, filtered by name & todays date minus the "days" value e.g. last 30 days
def get_list_minus_days(name, days):
    record = []
    records = []
    for d,n,c in zip(col0[1:],col1[1:],col2[1:]):                               # create a set of columns to iterate over using zip
        date = datetime.strptime(d.split(' ').pop(0), '%d/%m/%Y')               # fornat the 1st column into a valid datetime type
        if (date > (datetime.today() - timedelta(days=days))) and (n == name):
            record = [d,n,c]                                                    # create a list
            records.append(record)                                              # create a list of lists
    return records

#return a list of all columns, filtered by name & by earliest date permitted e.g. from x date
def get_list_from_date(name, date):
    record = []
    records = []
    for d,n,c in zip(col0[1:],col1[1:],col2[1:]):
        dd = datetime.strptime(d.split(' ').pop(0), '%d/%m/%Y')
        if (dd > date) and (n == name):
            record = [d,n,c]
            records.append(record)
    return records

# count of each chore for name since specified date
def get_categories_since_date(name, date):
    tasks = defaultdict(int)                                                    # create a default dictionary to hold the count
    for d,n,c in zip(col0[1:],col1[1:],col2[1:]):
        dd = datetime.strptime(d.split(' ').pop(0), '%d/%m/%Y')
        if (dd > date) and (n == name):
            tasks[c] += 1                                                       # create dict keys and count occurances
    return tasks

# gets the oldest date, for each names set of records
# Then compare earliest dates for each person and returns the most recent date
# this is used to get the oldest date that includes the most recent name
def get_earliest():
    earliest_dates = defaultdict(lambda : datetime.today())
    for n in unique_names():
        for d,n in zip(col0[1:],col1[1:]):
            date = datetime.strptime(d.split(' ').pop(0), '%d/%m/%Y')
            if earliest_dates[n] > date:
                earliest_dates[n] = date
    return (max(earliest_dates.values()))

# returns a dictionary containing the number of times each name has recorded the passed taskname
# name rankings by task
def results_by_task(task, date):
    results = defaultdict(int)
    for d,n,c in zip(col0[1:],col1[1:], col2[1:]):
        d = datetime.strptime(d.split(' ').pop(0), '%d/%m/%Y')
        if (d > date) and (c == task):
            results[n] += 1
    return results

# pprint(get_list_from_date('Stuart', get_earliest()))
# pprint(get_list_minus_days('Stuart', 90))
# pprint(get_categories_since_date('Stuart', get_earliest()))
# pprint(unique_names())
# pprint(get_earliest())
# pprint(results_by_task('Clean cooker top', get_earliest()))

for i in unique_chores()[1:]:
    pprint('Results for "{}"'.format(i))
    pprint(results_by_task(i, get_earliest()))
