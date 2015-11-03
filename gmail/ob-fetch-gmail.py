#!/usr/bin/env python
#
# Python script to read emails from gmail using imaplib.
# It retrieves NUMBER_OF_MAILS from gmail and store them in CACHE_FILE.
# This file is then used to display emails in a openbox pipe menu.
# Thanks to https://gist.github.com/robulouski/7441883 for the base of this script
# Edit the following variables EMAIL_ACCOUNT, PASSWORD and NUMBER_OF_MAILS
#

import sys
import imaplib
import email
import email.header
import datetime
import codecs
import os

EMAIL_ACCOUNT = "your.name@gmail.com"
PASSWORD = "your.password"
FOLDER = "INBOX"
NUMBER_OF_MAILS=20
CACHE_FILE=".ob-cache-gmail"
DIR=os.path.dirname(os.path.realpath(sys.argv[0]))
def process_mailbox(Mail):
    mailfile = codecs.open(DIR+'/'+CACHE_FILE,'w','utf-8')
    result, data = Mail.uid('search', None, "ALL")
    u_result, unread_mails = Mail.uid('search', None, "UNSEEN")
    Unread = len(unread_mails[0].split())
    mailfile.write("Unread Emails: {}\n".format(Unread))
    if result != 'OK':
        print("No messages found!")
        return

    for index, num in enumerate(data[0].split()[:-(NUMBER_OF_MAILS+1):-1]):
        result, data = Mail.uid('fetch', num, '(RFC822)')
        if result != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])
        Subject = email.header.decode_header(msg['Subject'])[0]
        Subject = Subject[0]
        if (not (type(Subject) is str)):
            Subject=Subject.decode("utf-8")
        Subject=Subject.replace('&','&amp;').replace('\"','&quot;').replace('\'','&apos;').replace('_','__')
        From=email.utils.parseaddr(msg['From'])
        mailfile.write("{0}. {1}\n".format(index+1, Subject))

        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            mailfile.write(local_date.strftime(" %d %b,%I:%M:%P")+"\n")
    mailfile.close()

Mail = imaplib.IMAP4_SSL('imap.gmail.com')

try:
    result, data = Mail.login(EMAIL_ACCOUNT, PASSWORD)
except imaplib.IMAP4.error:
    print("LOGIN FAILED")
    sys.exit(1)

print(result, data)

result, mailboxes = Mail.list()
"""
if result == 'OK':
    print("List of Mail Boxes:")
    print(mailboxes)
"""
result, data = Mail.select(FOLDER, readonly=True)
if result == 'OK':
    print("Processing mailbox")
    process_mailbox(Mail)
    Mail.close()
    print("Done")
else:
    print("ERROR: Accessing mailbox", result)

Mail.logout()
