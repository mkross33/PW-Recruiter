def personalize(text, contact):
    ruler = contact['leader']
    nation = contact['nation']
    new_text = text

    if '[[ruler]]' in new_text:
        new_text = new_text.replace('[[ruler]]', ruler)
    if '[[nation]]' in new_text:
        new_text = new_text.replace('[[nation]]', nation)
    return new_text


def send(contact, message, session):
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
    session.post('https://politicsandwar.com/inbox/message/', data=payload, headers={'User-Agent': 'Mozilla/5.0'})

