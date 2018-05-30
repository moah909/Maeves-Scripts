# import libraries
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

BAD_POSITIONS = {"Admin","admin","Worker","Researcher","RA","Spec","Temporary","Doctoral","Suppmental","Cook","Practical","Attendant"}

def processEmail(email):
    parts = re.findall("\'([\w\.]*)\'",email)
    email = "@".join(parts[0:2])
    return email

def readPage(query):
    current_page = 0
    last_page = -1
    retval = []
    directory_page = ("https://myaccount.umn.edu/lookup?SET_INSTITUTION=&campus=t&role=sta&type=name&CN={}".format(query))

    supersoup  = BeautifulSoup(urlopen(directory_page),"html.parser")

    links = supersoup(href=re.compile("/lookup"))

    for idx, link in enumerate(links):

        page = urlopen("https://myaccount.umn.edu"+link['href'])

        # parse the html using beautiful soup and store in variable 'soup'
        soup = BeautifulSoup(page, 'html.parser')

        #dept = soup.find(class_="organization-unit").text
        name = soup.find("h2").text

        blurb = soup.find("th").next.next.contents

        try:
            position = blurb[0]
            position = cleanPosition(position)
            if any([bad in position for bad in BAD_POSITIONS]):
                continue
        except:
            print("\rPosition not found for {}".format(name))
            position = ""
        try:
            dept = blurb[2]
            dept = cleanDepartment(dept)
        except:
            print("\rDepartment not found for {}".format(name))
            dept = ""
        try:
            email = soup.find(href=mailto_pat).text
        except:
            print("\rEmail not found for {}".format(name))
            email = ""

        print("\r{}/{}".format(idx,len(links)), flush=True, end="")

        retval.append([name,email,position,dept])


    print("\r{}/{} {}".format(len(links),len(links),query), flush=True)

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
        with Pool() as pool:
            result = pool.map(readPage, queries[START_INDEX*i::CHUNK_SIZE])

            with open(output_file+str(i), 'a+', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for process in result:
                    for row in process:
                        writer.writerow(row)
    except Exception as e:
        print(e)
        print("Error was caught on iteration {}/{}".format(i,25))
