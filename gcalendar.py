from __future__ import print_function
import httplib2
import os

import dateutil.parser

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

flags = 'noauth_local_webserver'

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def getbusydays(dy=15):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    print(CLIENT_SECRET_FILE)
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    current_time = datetime.datetime.utcnow()+ datetime.timedelta(days=1)
    further_time = current_time + datetime.timedelta(days=dy)#daysfromabove
    now = current_time.isoformat() + 'Z' # 'Z' indicates UTC time
    then = further_time.isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, timeMax=then, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])


    busydays = set()
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        d = dateutil.parser.parse(start)
        busydays.add(str(d)[0:10])

    return busydays


def all_days(dy=15):
    avalibledts = set()

    current_time = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    for i in range(dy):
        avalibledts.add(str(current_time+datetime.timedelta(days=i))[0:10])

    return avalibledts


def getfreedays():
    alld = all_days()
    busyd = getbusydays()
    print(len(alld.difference(busyd)))
    return (alld.difference(busyd))

if __name__ == '__main__':
    print(getfreedays())