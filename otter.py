#!/usr/bin/env python3
"""
Author : Brent Clark <brentgclark@gmail.com>
Purpose: This is something I wrote to keep track of the sanparks (i.e. https://www.sanparks.org).
         website, to track spots / availability of the Otter Trail.
         Anyone who knows the Otter, its incredibly difficult to get in.
"""

import argparse
from requests_html import HTMLSession
from prettytable import PrettyTable
from datetime import date

def main():
    today = date.today()
    session = HTMLSession()
    data = {
      'from_date': today,
      'to_date': '2029-07-30',
      'resort': 26,
      'unit_id': 26,
      'id': 396,
      'action': 'submit'
    }

    url = f'https://www.sanparks.org/parks/garden_route/camps/storms_river/tourism/availability_dates.php?id=396&resort=26&only_trails=otter&range=month#fromToAvailabilityCheck'
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
        if td[1].text == 'Yes':
          row = [
            td[0].text, # 'Date'
            td[1].text, # 'Available'
            td[2].text, # 'Nr'
          ]
          x.add_row(row)

    print("Today date is: ", today) 
    print(x)
        
if __name__ == '__main__':
    main()
