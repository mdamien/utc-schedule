#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
from icalendar import *
from datetime import datetime,tzinfo,timedelta
import extractToJson
import os

start_year,start_month,start_day = "2012","02","27"
end_year,end_month,end_day = "2012","06","27"
month_number_of_days = 29

class FrenchTimeZone(tzinfo):
    """UTC/GMT +1"""

    def utcoffset(self, dt):
        return timedelta(hours=1)

    def tzname(self, dt):
        return "GMT+1"

    def dst(self, dt):
        return timedelta(0)

def tocsv(): #event not repeatable...
    global start_year,start_month,start_day,end_year,end_month,end_day,month_number_of_days
    DAYS = ['LUNDI','MARDI','MERCREDI','JEUDI','VENDREDI','SAMEDI']
    arr = extractToJson.main()
    with open('utc.csv', 'wb') as f:
	writer = csv.writer(f)
	writer.writerow(["Subject","Start Date","Start Time","End Date","End Time","All Day Event","Description","Location","Private"])
	for uv in arr['uvs']:
	    name = uv['name']
	    hors = uv['hors']
	    place = uv['place']
	    typ = uv['type']
	    num = str((int(start_day)+DAYS.index(uv['day'])) % month_number_of_days)
	    arr = [name,num+"/"+start_month+"/"+start_year,hors[0],end_day+"/"+end_month+"/"+end_year,hors[1],"False",typ,place,"True"]
	    writer.writerow(arr)
	    
def toical():
    global start_year,start_month,start_day,end_year,end_month,end_day,month_number_of_days
    cal = Calendar()
    cal.add('prodid', '-//script Damien Marie//fr')
    cal.add('version', '2.0')
    DAYS = ['LUNDI','MARDI','MERCREDI','JEUDI','VENDREDI','SAMEDI']
    arr = extractToJson.main()
    for uv in arr['uvs']:
	event = Event()
	event['summary'] = uv['name'] + " , " + uv['type']
	if 'grp' in uv.keys():
	    event['summary'] = uv['name'] + " , " + uv['type'] + ", Groupe " + uv['grp']
	start_hor,end_hor = uv['hors']
	i = start_hor.find(':')
	start_h,start_m = int(start_hor[:i]),int(start_hor[i+1:])
	i = end_hor.find(':')
	end_h,end_m = int(end_hor[:i]),int(end_hor[i+1:])
	num = (int(start_day)+DAYS.index(uv['day']))
	month = int(start_month)
	if num > month_number_of_days:
	    num = (num % month_number_of_days) + 1
	    month += 1
	start_d = datetime(int(start_year),month,num,start_h,start_m)
	end_d = datetime(int(start_year),month,num,end_h,end_m)
	event.add('dtstart',start_d)
	event.add('dtend',end_d)
	event['location'] = uv['place']
	event['rrule'] = 'FREQ=WEEKLY'
	cal.add_component(event)
    f = open('utc.ics', 'wb')
    f.write(cal.as_string())
    f.close()
	
    
if __name__ == '__main__':
    toical()
