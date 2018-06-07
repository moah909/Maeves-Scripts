# import libraries
import time
import re
import sys
from multiprocessing import Pool, Queue
sys.path.insert(0,'../')
from common.common import *
from urllib.request import urlopen, Request
from random import randrange
import requests
from bs4 import BeautifulSoup
import csv
import itertools

class NoPositionException(Exception):
    pass

class NoDepartmentException(Exception):
    pass

def processEmail(person):
    ALPHA = '+-.0123456789@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz'
    person.script.string
    map, email = re.findall("var [ac]=\\\\\"(.+?)\\\\\"",person.script.string)
    ttable = str.maketrans(dict(zip(map,ALPHA)))
    return email.translate(ttable)

def getInfoFromSubpage(link):
    soup = None
    for attempt in range(0,5):
        try:
            proxy_num = randrange(100)
            response = requests.get(link, proxies = {"http":proxies[proxy_num],"https":proxies[proxy_num]}, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text,"html.parser")
            name = soup.find(id="indv-name-title").text
            name = cleanName(name, delim=",")
        except:
            proxies.pop(proxy_num)
            print("{} failed to open {}/5, retrying...".format(query,attempt,))
            time.sleep(attempt)
            pass
        else:
            break
    else:
        raise NoPositionException("Failed 5 times")

    try:
        position = soup.find(text="Title:").next.strip().title()
        position  = cleanPosition(position)
    except:
        raise NoPositionException()

    try:
        dept = soup.find(text="Department:").next.next.text.strip().title()
    except:
        raise NoDepartmentException(name)

    return (name,position,dept)

def readPage(query):
    print("Query: {}".format(query))
    retval = []
    directory_page = "https://directory.ufl.edu/search/?f=&l={}&e=&spa=&a=staff".format(query)

    for attempt in range(0,5):
        try:
            proxy_num = randrange(100)
            response = requests.get(directory_page, proxies = {"http":proxies[proxy_num],"https":proxies[proxy_num]})
            response.raise_for_status()
            soup  = BeautifulSoup(response.content,"html.parser")
        except:
            proxies.pop(proxy_num)
            print("{} failed to open {}/5, retrying...".format(query,attempt))
            time.sleep(attempt)
            pass
        else:
            break
    else:
        raise Exception("Failed 5 times")

    faculty = soup(class_="result")

    for idx, person in enumerate(faculty):

        name = person.find(class_="full-name").text

        try:
            email = processEmail(person)
        except:
            print("\rEmail not found for {}, skipping...".format(name))
            continue

        try:
            link = re.sub("/search/[^/]*$",person.a['href'][2:],directory_page)
            name, position, dept = getInfoFromSubpage(link)
        except NoPositionException:
            print("No position found for {}, skipping".format(name))
            continue

        print("\r{}/{}".format(idx,len(faculty)), flush=True, end="")
        past_queries.append(query)
        retval.append([name,email,position,dept])


    if soup.find(text=re.compile("first 100")) != None:
        last_name = faculty[-1].h4.text.strip().split(",")[0]
        if len(query) + 1 < len(last_name):
            new_query = last_name[0:len(query)+1]
        else:
            new_query = last_name
        while True:

            if new_query not in past_queries:
                readPage(new_query)

            if new_query[-1] not in ALPHABET[:-1]:
                break
            new_query = new_query[:-1] + ALPHABET[ord(new_query[-1])-ord("a")+1]


    print("\r{}/{} {}".format(len(faculty),len(faculty),query), flush=True)

    return retval

pages          = []
directory_page = []
processes      = []


EMAIL_FROM_HREF = True

container_tag   = None # Can be None to not sort by tag
container_attrs = { "class_" : "dir-Listing"}

faculty_tag     = None # Can be None to not sort by tag
faculty_attrs   = { "class_" : "dir-Listing-item"}

name_tag        = "h2" # Can be None to not sort by tag
name_attrs      = { }

email_tag       = None # Can be None to not sort by tag
email_attrs     = { "text" : mailto_pat}

position_tag    = None # Can be None to not sort by tag
position_attrs  = { "text" : "Title:"}

dept_tag        = None # Can be None to not sort by tag
dept_attrs      = { "text" : "Dept:"}

output_file = "ufl.csv"

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

CHUNK_SIZE  = 26
START_INDEX = 0

queries = [ "".join(tup) for tup in itertools.product(ALPHABET,repeat=2) ]
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

for i in range(0,26):
    proxies = []

    past_queries = []
    past_last_names = []

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

    try:
        with Pool() as pool:
            result = pool.map(readPage, queries[i*CHUNK_SIZE:(i+1)*CHUNK_SIZE])

            with open(ALPHABET[i] + "." + output_file, 'a+', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for process in result:
                    for row in process:
                        writer.writerow(row)
    except NoPositionException as e:
        print(e)
        print("Error was caught on iteration {}/{}".format(i,25))
