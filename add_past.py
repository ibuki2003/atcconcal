# -*- coding: utf-8 -*-

# HTML Parser
import requests
import urllib.request
from bs4 import BeautifulSoup as BS

#URL parser
from urllib.parse import urljoin

# Datetime lib
from datetime import datetime,timedelta

# Google Calendar API Lib (made by me)
from gcal import *

import common

import sys

import config

pages=-1

def getPastContestList(page):
    global pages
    contests=[]

    contestsurl='https://atcoder.jp/contests/archive/?lang=ja&page={page}'.format(page=page)
    html=urllib.request.urlopen(contestsurl)
    soup=BS(html,"lxml")

    if(pages<0):
        pages=int(soup.select_one('.pagination').findAll('li')[-1].text)

    table=soup.find('table')

    cs=table.select('tbody > tr')
    for c in cs:
        contest=c.findAll('td')

        starttime=datetime.strptime(contest[0].text,'%Y-%m-%d %H:%M:%S%z')

        length=contest[2].text
        hour,minute=length.split(':')
        length=timedelta(hours=int(hour),minutes=int(minute))
        endtime=starttime+length

        name=contest[1].find('a').text

        url=contest[1].a['href']
        url=urljoin(contestsurl, url)

        rateto=contest[3].text

        contests.append({
            'start': starttime,
            'end': endtime,
            'name': name,
            'url': url,
            'rateto': rateto
        })
    return contests

def main():
    global pages

    print("Add past contests to calendar script")
    print("run ok?[Y/N]")
    if(input()!='Y'):
        return
    gc=GoogleCalendar(config.ACCOUNT_ID,config.CALENDAR_ID)

    i=1
    if len(sys.argv)>1:
        i=int(sys.argv[1])

    while True:
        if(pages>0 and i>pages):
            break
        print("getting page",i,'/',pages)
        contests=getPastContestList(i)
        print("found",len(contests),"contests")
        for contest in contests:
            common.add_contest(contest, gc)
        i+=1

if __name__ == '__main__':
    main()
