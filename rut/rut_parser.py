# import libraries
import time
import re
import sys
from multiprocessing import Pool, Queue
sys.path.insert(0,'../')
from common.common import *
import requests
from bs4 import BeautifulSoup
import csv
import itertools

def getInfoFromSubpage(link):
    for attempt in range(0,5):
        time.sleep(5)
        try:
            soup     = BeautifulSoup(requests.get(link).text,"html.parser")
        except:
            print("{} failed to open {}/5, retrying...".format(query,attempt,))
            time.sleep(attempt)
            pass
        else:
            break
    else:
        raise Exception("Failed 5 times")
    email    = soup.find(href=re.compile("mailto")).text.strip()
    position = soup.find("dd").text.strip()
    return (email,position)

def readPage(query):
    current_page = 0
    last_page = -1
    retval = []
    directory_page = ("http://www.acs.rutgers.edu/pls/pdb_p/Pdb_Display.search_results")
    data = { "p_name_first":"",
             "p_name_last":query }

    for attempt in range(0,5):
        time.sleep(5)
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

    faculty = soup.find("tbody")("tr")

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

        retval.append([name,email,position,dept])


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

output_file = "umn.csv"

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

CHUNK_SIZE  = 26
START_INDEX = 0

queries = [ "".join(tup) for tup in itertools.product(ALPHABET,repeat=2) ]

for i in range(0,26):
    try:
        result = []
        # with Pool() as pool:
        for j in range(0,26):
            result.append(readPage(queries[i*26+j]))

        with open(ALPHABET[i] + "." + output_file, 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for process in result:
                for row in process:
                    writer.writerow(row)
    except Exception as e:
        print(e)
        print("Error was caught on iteration {}/{}".format(i,25))
