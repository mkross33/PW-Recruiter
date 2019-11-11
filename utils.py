# Per a request from the user who commissioned the standalone recruiter, all functions print out
# status info to the console, so the user can see what is happening. These can be removed if desired.
from requests import Session
from urllib.request import Request, urlopen
import json


def get_nations(key):
    req = Request(f"https://politicsandwar.com/api/nations/?key={key}&alliance_id=0", headers={'User-Agent': 'Mozilla/5.0'})
    print('Calling the API...')
    response = urlopen(req).read()
    data = json.loads(response)
    # Handle any errors reported by the PW API
    if data['success'] == 'false':
        print(data['general_message'])
    nations = data['nations']
    print('API Loaded')
    return nations


def get_noobs(nations):
    """ Finds new players from API data. Because the API contains no age information, the function
    pulls the 500 smallest nations who are not in alliances, not in vacation mode, and logged in in the past 2 days"""
    print('Finding new nations...')
    noobs = []
    noobs_found = 0
    # The nations API is sorted from largest to smallest, hence looping backwards to get new players
    for nation in nations[::-1]:
        # I consider nations inactive and not worth messaging if it has been more than 2 days (1500 minutes using the
        # API's units) since they last logged in. Feel free to change to suit your alliance's standards.
        inactive_threshold = 1500
        if (nation['vacmode'] == 0) and (nation['minutessinceactive'] < inactive):
            noobs_found += 1
            noobs.append(nation)
        if noobs_found >= 500:
            break
    return noobs


def filter_noobs(noobs, conn):
    print('Filtering previously messaged nations...')
    filtered_noobs = []
    c = conn.cursor()
    # check if the player already has a message log
    for noob in noobs:
        nation_id = noob['nationid']
        c.execute('''SELECT nation_id FROM logs WHERE nation_id=?''', (nation_id,))
        result = c.fetchone()
        if result:
            continue
        filtered_noobs.append(noob)
    c.close()
    return filtered_noobs


def personalize(text, contact):
    ruler = contact['leader']
    nation = contact['nation']
    new_text = text

    if '[[ruler]]' in new_text:
        new_text = new_text.replace('[[ruler]]', ruler)
    if '[[nation]]' in new_text:
        new_text = new_text.replace('[[nation]]', nation)
    return new_text


def send(messenger, message, contacts, conn):
    with Session() as s:
        login_payload = {
            'email': messenger['username'],
            'password': messenger['password'],
            'loginform': 'login'
        }
        s.post('https://politicsandwar.com/login/', data=login_payload, headers={'User-Agent': 'Mozilla/5.0'})

        c = conn.cursor()
        # send and log messages
        for contact in contacts:
            body = personalize(message['body'], contact)
            subject = personalize(message['subject'], contact)
            payload = {
                'newconversation': 'true',
                'receiver': contact['leader'],
                'carboncopy': '',
                'subject': subject,
                'body': body,
                'sndmsg': 'Send+Message'
            }
            s.post('https://politicsandwar.com/inbox/message/', data=payload, headers={'User-Agent': 'Mozilla/5.0'})
            c.execute('''INSERT INTO logs(nation_id) VALUES(?)''', (contact['nationid'],))
        c.close()

