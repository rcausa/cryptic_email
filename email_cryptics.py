import requests
from bs4 import BeautifulSoup 
import sqlite3
import smtplib 
from email.message import EmailMessage
import sys
# import mailchimp3
# from mailchimp3 import MailChimp



"""
TASKS:
------
Create MailChimp contacts list
Use Mailchip API to get contacts
Access db, figure out what want to send people(?).
Create and send email via SMTP server.

Other options - Google Forms
"""

# Collecting contacts from MailChimp
with open('mailchimp_api_key.txt') as g, open('test_details.txt','r') as test_deets:
    API_KEY = g.read()
    deets = test_deets.readlines()

deets = [d.rstrip('\n') for d in deets]

# Problems here:
client = MailChimp(deets[0], API_KEY)
a = client.lists.members.all('EmperorsClothes', get_all=True, fields="members.email_address")
print(a)

# Emailing the mailing list
SENDER_EMAIL = deets[2]
RECEIVER_EMAILS = [deets[0], deets[1]]
with open('mailserver_password.txt','r') as f:
    GMAIL_PASSWORD = f.read()

SUBJECT = "Testing email.."
BODY = f'''
    Dear receivers, \n
    Here are your cryptic crossword clues and answers. \n
    R.        
    '''
SUBJECT_AND_BODY = f"Subject: {SUBJECT}\n\n{BODY}"
# print(GMAIL_PASSWORD, type(GMAIL_PASSWORD))


# with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
#     email_obj = EmailMessage()
#     # email_obj['Subject'] = SUBJECT
#     email_obj['From'] = SENDER_EMAIL
#     email_obj['To'] = RECEIVER_EMAILS

#     smtp_server.login(SENDER_EMAIL, GMAIL_PASSWORD)
#     smtp_server.sendmail(SENDER_EMAIL, RECEIVER_EMAILS, SUBJECT_AND_BODY)