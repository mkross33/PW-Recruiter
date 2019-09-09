from urllib.request import Request, urlopen
import json
import sqlite3
from message_info import key, user, password, subject, body
from requests import Session

# CONSTANTS
message = {'subject': subject, 'body': body}
messenger = {'username': user, 'password': password}
header = {'User-Agent': 'Mozilla/5.0'}


def main():
    print('Starting script')
    # DB Connection
    conn = sqlite3.connect('logs.db')
    with conn:
        noobs = get_noobs(key)
        # filter into a list of only players we haven't messaged before
        print('Filtering previously messaged nations...')
        contacts = filter_noobs(noobs, conn)
        # message the contacts
        print('Sending messages...')
        send(messenger, message, contacts, conn)
        print('Success! You may close this window.')


def get_noobs(key):
    # get the list of all nation dicts from the API
    req = Request(f"https://politicsandwar.com/api/nations/?key={key}&alliance_id=0", headers=header)
    print('Calling the API...')
    response = urlopen(req).read()
    data = json.loads(response)
    # check if shit has gone south
    if data['success'] == 'false':
        print(data['general_message'])
    nations = data['nations']
    print('API Loaded')
    print('Finding new nations...')
    # list to store the 200 smallest active nations
    noobs = []
    # counter
    counter = 0
    # loop backwards through returned nations and pull out the first 200 hits who aren't VM
    for nation in nations[::-1]:
        # Anyone already 2+ days inactive is worthless
        inactive = 1500
        # Iterate the counter if we hit a non-VM, non-inactive nation
        if (nation['vacmode'] == 0) and (nation['minutessinceactive'] < inactive):
            counter += 1
            # if this nation is not in an alliance, add them to the list
            if nation['alliance'] == 'None':
                noobs.append(nation)
        # Stop after checking the bottom 100 active nations.
        if counter >= 500:
            break
    return noobs


### ADD SQL TO DO THIS OR SOME OTHER, LIKE CSV ###
def filter_noobs(noobs, conn):
    # list to store the filtered nation IDs
    filtered_noobs = []
    # connect to the database
    c = conn.cursor()
    # Filter out the list of noobs
    for noob in noobs:
        nation_id = noob['nationid']
        # check if an existing nation ID has been logged
        c.execute('''SELECT nation_id FROM logs WHERE nation_id=?''', (nation_id,))
        # skip if we already have a log for this nation
        result = c.fetchone()
        if result:
            continue
        # otherwise add them to the list
        filtered_noobs.append(noob)
    # close the cursor
    c.close()
    # return the finshed list of filtered nations
    return filtered_noobs


def personalize(text, contact):
    ruler = contact['leader']
    nation = contact['nation']
    new_text = text
    # Personalize any ruler and nation name fields in the message
    if '[[ruler]]' in new_text:
        new_text = new_text.replace('[[ruler]]', ruler)
    if '[[nation]]' in new_text:
        new_text = new_text.replace('[[nation]]', nation)
    return new_text


def send(messenger, message, contacts, conn):

    # open a request session to the PW server
    with Session() as s:
        # data params for the login page
        login_payload = {
            'email': messenger['username'],
            'password': messenger['password'],
            'rememberme': 1,
            'loginform': 'login'
        }
        # send the login request
        s.post('https://politicsandwar.com/login/', data=login_payload, headers={'User-Agent': 'Mozilla/5.0'})

        # loop through the contacts sending out the messages and creating logs
        c = conn.cursor()
        for contact in contacts:
            # personalize the message
            body = personalize(message['body'], contact)
            subject = personalize(message['subject'], contact)
            # set the POST payload
            payload = {
                'newconversation': 'true',
                'receiver': contact['leader'],
                'carboncopy': '',
                'subject': subject,
                'body': body,
                'sndmsg': 'Send+Message'
            }
            # send the request
            s.post('https://politicsandwar.com/inbox/message/', data=payload, headers={'User-Agent': 'Mozilla/5.0'})
            # log it
            c.execute('''INSERT INTO logs(nation_id) VALUES(?)''', (contact['nationid'],))
        c.close()


if __name__ == '__main__':
    main()