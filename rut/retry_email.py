#!/usr/bin/env python3
import csv
import sys
import requests
import requests.exceptions
import time
from random import randrange
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re

if (len(sys.argv) != 3) or ("-h" in sys.argv) or ("--help" in sys.argv):
    print("Usage: {} <input file> <output file>\nGenerates a list of unique positions in <input file> and outputs them in <output file>".format(sys.argv[0]))
    exit()

entries = []

proxies = []

past_queries = []
past_last_names = []
past_names = []

req = Request( "https://sslproxies.org/",
   data=None,
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)

page = urlopen(req)

proxysoup = BeautifulSoup(page,"html.parser")
proxies_table = proxysoup.find(id='proxylisttable')

for row in proxies_table.tbody.find_all('tr'):
    proxies.append( "http://" + row.find_all('td')[0].string + ":" +
      row.find_all('td')[1].string)

with open(sys.argv[1]) as csvfile:
    filereader = csv.reader(csvfile)
    for row in filereader:
        entries.append(row)

for row in entries:
    if row[1] == "" or row[2] == "":

        print("No email/position found for: {}".format(row[0]))

        directory_page = ("http://www.acs.rutgers.edu/pls/pdb_p/Pdb_Display.search_results")
        data = { "p_name_first":row[0].split(" ")[0],
                 "p_name_last" :row[0].split(" ")[-1]}

        for attempt in range(0,5):
            try:
                response = requests.post(directory_page, proxies = {"http":proxies[randrange(100)]}, data=data, timeout = 30)
                response.raise_for_status()
                soup = BeautifulSoup(response.text,"html.parser")
                row[1] = soup.find(href=re.compile("mailto")).text.strip()
                row[2] = soup.find("dd").text.strip()
            except requests.exceptions.RequestException:
                print("Page failed to open {}/5, retrying...".format(attempt+1,5))
                time.sleep(attempt)
                pass
            except:
                print("Other exception, skipping")
                break
            else:
                break
        else:
            print("Failed 5 times, skipping")


with open(sys.argv[2], 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for row in entries:
        writer.writerow(row)
