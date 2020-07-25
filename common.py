# -*- coding: utf-8 -*-
from datetime import datetime,timedelta

def getDatetimeArr(dt):
    return {
        'dateTime': dt.isoformat(),
        'timeZone': 'Asia/Tokyo'
    }

def add_contest(contest, gc):
    edit=None

    # URL基準にすることで同名のコンテストを区別できる
    contest_inner_name = contest['url'].split('/')[-1]
    for item in gc.list_events(contest_inner_name):
        dsc=item["description"]
        dsc=dsc[4:dsc.find("\n")]
        if(dsc==contest['url']):
            differ=set()
            starttime=item['start']['dateTime']
            starttime=starttime[:-3]+starttime[-2:]
            starttime=datetime.strptime(starttime, '%Y-%m-%dT%H:%M:%S%z')

            endtime=item['end']['dateTime']
            endtime=endtime[:-3]+endtime[-2:]
            endtime=datetime.strptime(endtime, '%Y-%m-%dT%H:%M:%S%z')
            if starttime!=contest['start'] or endtime!=contest['end']  : differ.add('time')
            if item['summary']!=contest['name']:differ.add('name')
            if len(differ)>0:
                edit=(item, differ)
            else:
                return # 登録済み
            break
        elif 'beta' in dsc and dsc.split('/')[-1]==contest_inner_name:
            edit=(item, {'beta'})

    # APIのbody作成
    description="""URL:{url}
レート対象:{rateto}"""
    description=description.format(url=contest['url'],rateto=contest['rateto'])
    body = {
        'start': getDatetimeArr(contest['start']),
        'end':   getDatetimeArr(contest['end']),
        'summary': contest['name'],
        'description': description
    }
    if edit is None:
        res=gc.insert_event(body)
        print("added contest",contest['name'], "(",contest['start'],"~",contest['end'],")")
    else:
        res=gc.update_event(body, edit[0]['id'])
        print("edited contest",contest['name'])
        if 'time' in edit[1]:
            print(edit[0]['start']['dateTime'],'~',edit[0]['end']['dateTime'] ,'=>')
            print(contest['start'].isoformat(), '~', contest['end'].isoformat())
        if 'name' in edit[1]:
            print(edit[0]['summary'], '=>', contest['name'])
        if 'beta' in edit[1]:
            print('moved from beta')
