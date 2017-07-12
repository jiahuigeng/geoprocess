# -*- coding: utf-8 -*-
"""
Dieses Modul zeigt den grundlegenden Umgang mit "requests" und "BeautifulSoup"
fuer Web Scraping-Anwendungen.

Requests: Ausfuehren und Verarbeiten von HTTP-Requests (z.B. GET und POST).
BeautifulSoup: Parsing und Erstellung von (strukturierten) Texten wie z.B: XML, HTML...

http://docs.python-requests.org/en/master/
https://www.crummy.com/software/BeautifulSoup/

@author: schwerjo
"""

from bs4 import BeautifulSoup as bs
import requests


def myrequest(url):

    # HTTP request
    r = requests.get(url)
    # Raise Exception bei 404
    r.raise_for_status()
    return r

urls = ["http://httpbin.org/status/404", "https://www.geo.uni-augsburg.de/aktuelles/",
        "http://terrapreta.geo.uni-augsburg.de/airports.html"]

for u in urls[:2]:

    try:
        r = myrequest(u)
        print type(r)
        print r # HTTP Response, 200 is OK: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
        print r.headers # Header der HTTP Response
        print r.headers["Content-Type"]
        print r.apparent_encoding # Offenbar Unicode utf-8
        # print r.text
        # print r.content # binary response

    except requests.exceptions.HTTPError as e:
        print e


# Airports Parsen
r = myrequest(urls[2])
print r.text

# BeautifulSoup uebergeben wir diese Seite zur Verarbeitung
# Die Seite soll als Unicode-HTML interpretiert werden
soup = bs(r.text.encode("utf-8"), "html.parser")

# Durchsuche das Document Object Model (DOM) nach dem Tag "table"
soup_table = soup.find("table")

# Suche innerhalb der Tabelle alle Zeilen (<tr></tr>)
soup_rows = soup_table.find_all("tr")
print soup_rows

# Wie viele Zeilen hat Tabelle?
print len(soup_rows)

# Attributdaten stecken in table data <td></td>
for row in soup_rows:
    row_data = row.find_all("td")
    for td in row_data:
        print td.text

