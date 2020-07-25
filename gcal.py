# -*- coding: utf-8 -*-

import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import logging
import os
import sys
import traceback


class GoogleCalendar(object):

    def __init__(self,account_id,calendar_id):
        self.service_account_id = account_id
        self.calendar_id=calendar_id
        self.creds=False
        self.get_credentials()
        self.http = self.creds.authorize(httplib2.Http())
        self.service = discovery.build('calendar','v3',http=self.http)


    def get_credentials(self):
        if(not self.creds) or self.creds.invalid:
            scopes = 'https://www.googleapis.com/auth/calendar'

            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                'gcal_token.json',
                scopes=scopes
            )

            self.creds=credentials

    def insert_event(self,data):
        created_calendar = self.service.events().insert(calendarId=self.calendar_id,body=data).execute()
        return created_calendar

    def list_events(self,query):
        credentials = self.get_credentials()

        events = self.service.events().list(
            calendarId=self.calendar_id,
            q=query
        ).execute()

        items = events['items']

        return items
    def update_event(self, data, eventId):
        updated_calendar = self.service.events().update(calendarId=self.calendar_id,eventId=eventId, body=data).execute()
        return updated_calendar
