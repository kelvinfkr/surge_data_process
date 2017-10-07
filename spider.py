# -*- coding: utf-8 -*-
import requests
import sys
import os
import csv

home = 'https://tidesandcurrents.noaa.gov/api/datagetter'

word = 'Date'

payload = {
    'application': 'NOS.COOPS.TAC.WL',
    'station': '8518750',
    'datum': 'NAVD',
    'units': 'metric',
    'action': 'data',
    'format': 'csv',
    'time_zone': 'GMT',
    'interval':'h'
}

def getyear(date):
    return int(date / 10000)

def add(payload, year):
    r = requests.get(home, params=payload)
    fp.write(r.content)

def solve(tmp):
    payload['product'] = tmp
    ya = getyear(over_begin_date) 
    yb = getyear(over_end_date)
    if ya == yb:
        payload['begin_date'] = over_begin_date
        payload['end_date'] = over_end_date
        add(payload, ya)
    else:
        payload['begin_date'] = over_begin_date
        payload['end_date'] = str(ya)+'1231'
        add(payload, ya)
        
    for i in range(ya+1, yb):
        print(str(i)+'finished')
        payload['begin_date'] = str(i)+'0101'
        payload['end_date'] = str(i)+'1231'
        add(payload, i)
        
        payload['begin_date'] = str(yb)+'0101'
        payload['end_date'] = over_end_date
        add(payload, yb)
    
    fp.close()

    print('Finished,Processing')

    reader = csv.reader(open('tmp.csv','rb'))
    writer = csv.writer(open(name + '.csv','ab'))
    
    fir = 0;
    for row in reader:
        if(row[0][0] != 'D' and row[0][0] != 'E'):
            writer.writerow(row)
        if(not fir):
            writer.writerow(row)
            fir = 1
                    
    print('Have intergrated ' + name + '.csv')

fp = open('tmp.csv','ab') 

over_begin_date = int(input('begin_date(sample: 19200101) ? '))
over_end_date = int(input('end_date(sample: 20160628) ? '))
tmp = input("datums? hourly_height? predictions? ")
name = input("enter the file name(sample: data): ")

word = ['datums', 'hourly_height', 'predictions']

while(not tmp in word):
    tmp = input("error, input again: \n")

solve(tmp)

os.remove('tmp.csv')
