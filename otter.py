#!/usr/bin/env python3
"""
Author : Brent Clark <brentgclark@gmail.com>
Purpose: This is something I wrote to keep track of the sanparks (i.e. https://www.sanparks.org).
         website, to track spots / availability of the Otter Trail.
         Anyone who knows the Otter, its incredibly difficult to get in.
"""

import os
import smtplib
import ssl
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from requests_html import HTMLSession
from prettytable import PrettyTable

def mailgmail(text, todaysdate):
    """ smtp function """

    sender_email = os.getenv('GMAILADDRESS')
    password = os.getenv('GMAILPASSWORD')
    receiver_email = os.getenv('GMAILRCPT')

    mail_content = f'{text}'
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = f'Otter script - {todaysdate}'
    message.attach(MIMEText(mail_content, _charset='UTF-8'))
    text = message.as_string()

    context = ssl.create_default_context()

    with smtplib.SMTP(host='smtp.gmail.com', port=587, timeout=10) as server:
        #server.set_debuglevel(1)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

def main():
    """ Main function """

    today = date.today()
    session = HTMLSession()
    data = {
        #'from_date': today,
        'from_date': '2022-08-30',
        'to_date': '2029-07-30',
        'resort': 26,
        'unit_id': 26,
        'id': 396,
        'action': 'submit'
    }

    url = 'https://www.sanparks.org/parks/garden_route/camps/storms_river/tourism/availability_dates.php?id=396&resort=26&only_trails=otter&range=month#fromToAvailabilityCheck'
    headers = {
        'User-Agent': 'My User Agent 1.0',
    }

    try:
        r = session.post(url, headers=headers, data=data)
    except Exception as e:
        print(e)

    x = PrettyTable()
    x.field_names = ['Date', 'Available', 'Nr']
    div = r.html.find('div#results', first=True)

    for tr in div.find('tr'):
        td = tr.find('td')
        if len(td) >= 1:
            #if td[1].text == 'Yes':
            row = [
                td[0].text, # 'Date'
                td[1].text, # 'Available'
                td[2].text, # 'Nr'
            ]
            x.add_row(row)

    rates = '\n'
    base = r.html.xpath('/html/body/main/div/div/div/div/section[1]/div/div/div[1]/div[1]/table')
    for element in base:
        for tr in element.find('tr'):
            td = tr.find('td')
            rates += f"{td[0].text:24}: {td[1].text}\n"

    searchdate = f"Search from: {data['from_date']}\nSearch to:{data['to_date']}\n"
    result = searchdate + x.get_string() + rates
    mailgmail(result, today)
if __name__ == '__main__':
    main()
