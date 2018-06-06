# import libraries
import time
import re
import sys
from multiprocessing import Pool, Queue
sys.path.insert(0,'../')
from common.common import *
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import csv
import itertools

def processEmail(email):
    parts = re.findall("\'([\w\.]*)\'",email)
    email = "@".join(parts[0:2])
    return email

def readPage(query):
    current_page = 0
    last_page = -1
    retval = []
    directory_page = ("https://www.uky.edu/chs/directory?page={}".format(query))

    for attempt in range(0,5):
        try:
            supersoup  = BeautifulSoup(urlopen(directory_page),"html.parser")
        except:
            print("{} failed to open {}/5, retrying...".format(query,attempt))
            time.sleep(attempt)
            pass
        else:
            break
    else:
        raise Exception("Failed 5 times")

    links = supersoup.find(class_="view-content")(href=re.compile("^/chs/\w+"))

    for idx, link in enumerate(links):

        for attempt in range(0,5):
            try:
                page = urlopen("https://www.uky.edu"+link['href'])
                # parse the html using beautiful soup and store in variable 'soup'
                soup = BeautifulSoup(page, 'html.parser')
            except:
                print("{} failed to open {}/5, retrying...".format(query,attempt,))
                time.sleep(attempt)
                pass
            else:
                break
        else:
            raise Exception("Failed 5 times")

        subsoup = soup.find(class_="group-profile-sidebar")

        name = subsoup.find(name_tag,**name_attrs).text
        name = cleanName(name,delim=",")
        try:
            position = subsoup.find(position_tag,**position_attrs).text
            position = cleanPosition(position,delim=",")
        except:
            print("\rPosition not found for {}".format(name))
            position = ""
        try:
            email = subsoup.find(email_tag,**email_attrs).text
        except:
            print("\rEmail not found for {}".format(name))
            email = ""
        try:
            dept = subsoup.find(dept_tag,**dept_attrs).text
            dept = cleanDepartment(dept)
        except:
            print("\rDepartment not found for {}".format(name))
            dept = ""

        print("\r{}/{}".format(idx,len(links)), flush=True, end="")

        retval.append([name,email,position,dept])


    print("\r{}/{} {}".format(len(links),len(links),query), flush=True)

    return retval

pages          = []
directory_page = []

name_tag        = None # Can be None to not sort by tag
name_attrs      = { "class_":"field-name-field-name" }

email_tag       = None # Can be None to not sort by tag
email_attrs     = { "class_" : "field-name-field-email-address"}

position_tag    = None # Can be None to not sort by tag
position_attrs  = { "class_" : "field-name-field-position-title"}

dept_tag        = None # Can be None to not sort by tag
dept_attrs      = { "class_" : "field-name-field-department"}

output_file = "health.csv"

with Pool() as pool:
    result = pool.map(readPage, range(0,10))

    with open(output_file, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for process in result:
            for row in process:
                writer.writerow(row)
