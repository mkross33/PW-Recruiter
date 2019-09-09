# PW-Recruiter
Recruitment bot for Politics and War. Requires python and the requests package.

Calls the nations API and pulls the smallest 500 nations that aren't in an alliance and are less than two days inactive. This approxomates to new nations, as the API does not return nation age. It then filters out any nation ID's that have already been messaged, and sends them your recruitment message, logging recipients to the logs database. It will print status messages to the terminal so you can follow what it's doing. 

You must edit message_info.py with a text editor. Include your details in the appropriate places between the quotation marks (API key, user credentials, subject, body). Subject cannot be more than 50 characters per PW rules. [[ruler]] and [[nation]] can be used as standins for a players ruler and nation name, which will be swapped in when sending the message. 

Windows Usage: run message.bat to launch the script. 

Linux: python recruit.py 

I recommend using Cron/Task Scheduler to have it run daily.
