from applicant_messenger import message_applicants
from unaligned_messenger import recruit
from time import sleep
from message_info import key


def main():
    message_applicants(key)
    recruit(key)
    sleep(180)


if __name__ == '__main__':
    while True:
        main()
