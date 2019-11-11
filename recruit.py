import sqlite3
from message_info import key, user, password, subject, body
from utils import get_nations, get_noobs, filter_noobs, send


def main():
    """ Finds new players from the nations API, then sends and logs recruitment messages to them. """
    message = {'subject': subject, 'body': body}
    messenger = {'username': user, 'password': password}
    print('Starting script')
    if len(subject) > 50:
        print("Subject too long, must not exceed 50 characters")
        return 0
    nations = get_nations(key)
    noobs = get_noobs(nations)
    conn = sqlite3.connect('logs.db')
    with conn:
        contacts = filter_noobs(noobs, conn)
        send(messenger, message, contacts, conn)
        print('Success! You may close this window.')


if __name__ == '__main__':
    main()
