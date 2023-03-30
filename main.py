#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import email
import imaplib
import os
import smtplib
import sys
import time
import traceback
import webbrowser

import html2text
from decouple import config

from utils.helper import *

FROM_EMAIL = config("FROM_EMAIL")
ORG_EMAIL = config("ORG_EMAIL")
FULL_EMAIL = FROM_EMAIL + "@" + ORG_EMAIL
FROM_PWD = config("FROM_PWD")
SMTP_SERVER = config("SMTP_SERVER")
SMTP_PORT = config("SMTP_PORT", cast=int, default=587)

if sys.version_info[0] >= 3:
    unicode = str


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)


def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        # mailboxes = mail.list() # tuple
        mail.select(mailbox="INBOX", readonly=True)

        data = mail.search(None, "ALL")
        mail_ids = data[1]
        id_list = mail_ids[0].split()
        # first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        printInfo("Total Emails", latest_email_id)
        lineBreak("#")

        for i in range(latest_email_id, latest_email_id - 10, -1):
            printBody = False
            html_text = html2text.HTML2Text()
            html_text.ignore_links = True
            html_text.images_to_alt = True
            html_text.ignore_tables = True
            html_text.single_line_break = True

            data = mail.fetch(str(i), "(RFC822)")
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1], "utf-8", "ignore"))
                    email_subject = msg["subject"]
                    email_from = msg["from"]
                    printInfo("From", email_from)
                    printInfo("Subject", email_subject)
                    # printInfo("Msg Keys", msg.items())
                    printInfo("Content Type", msg.get_content_type())
                    # print(msg)
                    # exit(0)
                    if msg.is_multipart():
                        # iterate over email parts
                        for part in msg.walk():
                            # extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                # get the email body
                                body = part.get_payload(None, decode=True).decode()
                            except:
                                body = "<empty>"
                                pass
                            if (
                                content_type == "text/plain"
                                and "attachment" not in content_disposition
                                and printBody == False
                            ):
                                # print text/plain emails and skip attachments
                                printInfo("Email Body", body[:100])
                                printBody = True
                            elif "attachment" in content_disposition:
                                # download attachment
                                filename = part.get_filename()
                                printInfo("Attachment", filename)
                            elif content_type == "text/html" and printBody == False:
                                try:
                                    body = part.get_body().get_payload(None, decode=True)
                                    printInfo("Email Body", body[:100])
                                    printBody = True
                                except:
                                    pass
                    else:
                        # extract content type of email
                        content_type = msg.get_content_type()
                        # get the email body
                        body = msg.get_payload(None, decode=True).decode()
                        if content_type == "text/plain" and printBody == False:
                            # print only text email parts
                            printInfo("Email Body", body[:100])
                            printBody = True

                        # elif content_type == "text/html":
                        #     try:
                        #         body = part.get_body(
                        #             preferencelist=("plain", "html")
                        #         ).get_payload(None, decode=True)
                        #         printInfo("Email Body", body[:100])
                        #     except:
                        #         pass
                    if content_type == "text/html" and printBody == False:
                        # # if it's HTML, create a new HTML file and open it in browser
                        # folder_name = clean(email_subject)  # type: ignore
                        # if not os.path.isdir(folder_name):
                        #     # make a folder for this email (named after the subject)
                        #     os.mkdir(folder_name)
                        # filename = "index.html"
                        # filepath = os.path.join(folder_name, filename)
                        # # write the file
                        # open(filepath, "w").write(body)
                        # # open in the default browser
                        # webbrowser.open(filepath)
                        printInfo("html2text", html_text.handle(body)[:100])
                        printBody = True

            lineBreak("#")

    except Exception as e:
        traceback.print_exc()
        print(str(e))


read_email_from_gmail()
