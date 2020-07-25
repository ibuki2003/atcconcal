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

import config

def getFutureContestList():
    contests=[]

    contestsurl='https://atcoder.jp/contests/?lang=ja'
    html=urllib.request.urlopen(contestsurl)
    soup=BS(html,"lxml")
    div = soup.find('div', id='contest-table-upcoming')
    table=div.find('table')
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
    gc=GoogleCalendar(config.ACCOUNT_ID,config.CALENDAR_ID)

    contests=getFutureContestList()
    if(len(contests)==0):return # no upcoming contest
    for contest in contests:
        common.add_contest(contest, gc)
if __name__ == '__main__':
    main()
