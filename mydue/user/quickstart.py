from __future__ import print_function
import pickle
import os.path
import os
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import date
import datetime
import re
import base64
def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6})')
	cleantext = re.sub(cleanr, '' , raw_html)
	return cleantext
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
def parse():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    mail = {}
    list = []
    yesterday = date.today() - datetime.timedelta(days=1)
    results = service.users().messages().list(userId='me', labelIds=['IMPORTANT'],q='after:'+str(yesterday)).execute()
    messages = results.get('messages', [])
    if not messages:
        return None
    else:
        for message in messages[:]:
            msg = service.users().messages().get(userId='me',format='full',id=message['id']).execute()
            lst = re.findall("'From', 'value': \S+ \S+ <\S+@\S+", str(msg['payload']['headers']))
            for sender in lst:
                fromemail = str(re.findall('\S+@\S+', sender))
            fromemail = fromemail[3:-6]
            mail['from'] = fromemail
            mail['id'] = msg['id']
            msg = service.users().messages().get(userId='me',format='raw',id=message['id']).execute()
            msg1 = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
            cleaned = cleanhtml(str(msg1))
            cleaned_amount = re.findall('=E2=82=B9\s*[0-9]+' , cleaned)
            if len(cleaned_amount) > 0:
                cleaned_amount = str(cleaned_amount[0])
            cleaned_amount = cleaned_amount[9:]
            mail['amt'] = cleaned_amount
            cleaned_date = re.findall('=E2=82=B9\s*[0-9]+' , cleaned)
            all2 = re.findall(r"due\s*\S+\s*[\d]{1,2}/[\d]{1,2}/[\d]{4}", cleaned)
            if(len(all2) > 0):
                all2 = all2[0]
                all2 = (all2[-10:])
            mail['date'] = all2
            vendors = ['Netflix' , 'Amazon Prime', 'Hotstar', 'Voot' , 'Viu', 'Zee 5', 'SonyLiv' , 'ALTBalaji', 'Hulu', 'BSNL', 'Airtel' ,'Vodafone', 'Jio','Idea', 'KSEB', 'Kerala Water Authority','']
            for vendor in vendors:
                if vendor in cleaned:
                    cleaned_vendor = vendor
                    break
            mail['vendor'] = cleaned_vendor
            cleaned_id = re.findall('ID\s*:\s[0-9]+' , cleaned)
            if(len(cleaned_id) > 0 ):
                cleaned_id = cleaned_id[0]
                cleaned_id = cleaned_id[5:]
            mail['invoiceid'] = cleaned_id
            list.append(mail.copy())
        return list
#if __name__ == '__main__':
#    print(main())
	
