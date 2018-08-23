import requests as req
import time
import json
from api import answers


def auth_amo(USER_LOGIN = '***',
             USER_HASH = '***'):
    s = req.Session()

    link = 'https://soulfulloft.amocrm.ru/private/api/auth.php?type=json'
    h = {'user-agent': 'amoCRM-API-client/1.0'}
    payload = {'USER_LOGIN': USER_LOGIN, 'USER_HASH': USER_HASH}

    resp = s.get(url=link, params=payload, headers=h)
    data = json.loads(resp.text)

    return data, s


def create_contact(session, phone, name):
    link = 'https://soulfulloft.amocrm.ru/api/v2/contacts'
    s = session

    payload = {
        'add': [
            {
                'name': name,
                'created_at': int(time.time()),
                'custom_fields': [{
                    'id': 262500,
                    'is_system': True,
                    'name': 'Телефон',
                    'values': [{
                        'value': phone,
                        'enum': '598058'
                    }]
                },
                ]
            }
        ]
    }

    h = {'user-agent': 'amoCRM-API-client/1.0'}
    resp = s.post(url=link, data=json.dumps(payload), headers=h)
    data = json.loads(resp.text)
    cid = data['_embedded']['items'][0]['id']

    return cid


def commit_lead(session, contact,
                name, pipeline=232140, phone,
                date, event_type, members):

    s = session
    created_at = int(time.time())

    link = 'https://soulfulloft.amocrm.ru/api/v2/leads'
    h = {'user-agent': 'amoCRM-API-client/1.0'}

    payload = {
        'add': [{
            'name': event_type,
            'created_at': created_at,
            'pipeline_id': pipeline,
            'contacts_id': contact,
            'custom_fields': [{'id': 431732, 'values': [{'value': date}]},
                              {'id': 432298, 'values': [{'value': 'Telegram'}]},
                              {'id': 431908, 'values': [{'value': event_type}]},
            ],
            'tags': 'Telegram, '+str(members)
        }]
    }

    resp = s.post(url=link, data=json.dumps(payload), headers=h)
    data = json.loads(resp.text)

    return data


def get_leads():
    data, s = auth_amo()
    h = {'user-agent': 'amoCRM-API-client/1.0'}
    link = 'https://soulfulloft.amocrm.ru/api/v2/leads'
    link = 'https://soulfulloft.amocrm.ru/api/v2/contacts'
    limit_rows = 1

    payload = {
        'limit_rows': limit_rows,
        'limit_offset': 2,
    }

    resp = s.get(url=link, params=payload, headers=h)
    data = json.loads(resp.text)

    return data


def send_lead(phone, loft, date, name='null', event_type='null', members='40-80'):
    data, session = auth_amo()
    pipeline = answers.pipelines[loft]
    contact = create_contact(session, phone=phone, name=name)
    commit_lead(session,
                date=date,
                contact=contact,
                event_type=event_type,
                members=members,
                pipeline=pipeline)

    return True