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

def getInfoFromSubpage(link):
    for attempt in range(0,5):
        try:
            soup = BeautifulSoup(requests.get(link, proxies = {"http":proxies[randrange(100)]}, timeout=30).text,"html.parser")
            email    = soup.find(href=re.compile("mailto")).text.strip()
            position = soup.find("dd").text.strip()
            return (email,position)
        except:
            print("{} failed to open {}/5, retrying...".format(query,attempt,))
            time.sleep(attempt)
            pass
        else:
            break
    else:
        raise Exception("Failed 5 times")
def readPage(query):
    print("Query: {}".format(query))
    current_page = 0
    last_page = -1
    retval = []
    directory_page = ("http://www.acs.rutgers.edu/pls/pdb_p/Pdb_Display.search_results")
    data = { "p_name_first":"",
             "p_name_last":query }

    for attempt in range(0,5):
        try:
            response = requests.post(directory_page,data=data)
            response.raise_for_status()
            soup  = BeautifulSoup(response.text,"html.parser")
        except:
            print("{} failed to open {}/5, retrying...".format(query,attempt,))
            time.sleep(attempt)
            pass
        else:
            break
    else:
        raise Exception("Failed 5 times")

    body = soup.find("tbody")
    if body == None:
        return [["","","",""]]

    faculty = body("tr")

    for idx, person in enumerate(faculty):
        info = person("td")

        if(info[1].text.strip() != "Faculty" or info[0].text.strip()  == ""):
            continue

        #dept = soup.find(class_="organization-unit").text
        name = info[0].text.strip()

        try:
            email, position = getInfoFromSubpage("http" + info[0].find("a")["href"][5:])
        except:
            print("\rPosition or email not found for {}".format(name))
            continue
            position = ""
            email    = ""
        try:
            dept = info[2].text.strip()
            dept = cleanDepartment(dept)
        except:
            print("\rDepartment not found for {}".format(name))
            continue
            dept = ""

        print("\r{}/{}".format(idx,len(faculty)), flush=True, end="")
        past_queries.append(query)
        retval.append([name,email,position,dept])


    if soup.find(text=re.compile("50 matches")) != None:
        print()
        last_name = faculty[-1].td.text.strip().split(" ")[-1]
        if last_name not in past_last_names and query.lower() in last_name.lower():
            past_last_names.append(last_name)
            if len(query) + 1 < len(last_name):
                new_query = last_name[0:len(query)+1]
            else:
                new_query = last_name
            while True:

                if new_query not in past_queries:
                    readPage(new_query)

                if new_query[-1] == "z":
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

output_file = "rut.csv"

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

CHUNK_SIZE  = 26
START_INDEX = 0

queries = [ "".join(tup) for tup in itertools.product(ALPHABET,repeat=2) ]
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

for i in range(0,26):
    # try:
    result = []
    # with Pool() as pool:
    for j in range(0,26):
        result.append(readPage(queries[i*26+j]))

    with open(ALPHABET[i] + "." + output_file, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for process in result:
            for row in process:
                writer.writerow(row)
    # except Exception as e:
    #     print(e)
    #     print("Error was caught on iteration {}/{}".format(i,25))
