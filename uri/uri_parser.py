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

BAD_POSITIONS = {"Admin","admin","Worker","Researcher","RA","Spec","Temporary","Doctoral","Suppmental","Cook","Practical","Attendant","Intern","Developer"}

def processEmail(email):
    parts = re.findall("\'([\w\.]*)\'",email)
    email = "@".join(parts[0:2])
    return email

def readPage(query):
    current_page = 0
    last_page = -1
    retval = []
    soup = None
    directory_page = "https://directory.uri.edu/index.php?SearchType=people#left"
    data = {
    "my_base_dn":"dc=URI,dc=EDU",
    "op":"searchresult",
    "Search":"Search",
    "searchfor":"yes",
    "searchfor_cn":"",
    "searchfor_dept":"",
    "searchfor_sn":query,
    "searchfor_title":"",
    "URIEduStatus":"staff"
    }

    for attempt in range(0,5):
        try:
            response = requests.post(directory_page,data=data)
            response.raise_for_status()
            soup = BeautifulSoup(response.content,"html.parser")
        except:
            print("{} failed to open {}/5, retrying...".format(query,attempt,))
            time.sleep(attempt)
            pass
        else:
            break
    else:
        raise Exception("Failed 5 times")

    faculty = soup.find_all(faculty_tag,**faculty_attrs)

    for idx, person in enumerate(faculty):

        bolded = person("b")

        left_tds = person("td",align="left")

        if(bolded[-1].text != "Faculty" ) and (bolded[-1].text != "Emeriti" ):
            continue

        name = cleanName(bolded[0].text, flip=FLIP_NAME)

        try:
            email = person.find(email_tag,**email_attrs).strip()
        except:
            print("\rEmail not found for {}".format(name))
            continue
        try:
            position = left_tds[1].text.strip()
            position = cleanPosition(position)
        except:
            print("\rPosition not found for {}".format(name))
            position = ""
        try:
            dept = left_tds[2].text.strip()
            dept = cleanDepartment(dept)
        except:
            print("\rDepartment not found for {}".format(name))
            dept = ""

        print("\r{}/{}".format(idx,len(faculty)), flush=True, end="")

        retval.append([name,email,position,dept])


    print("\r{}/{} {}".format(len(faculty),len(faculty),query), flush=True)

    return retval

pages          = []
directory_page = []
processes      = []


EMAIL_FROM_HREF = True
FLIP_NAME = True

container_tag   = None # Can be None to not sort by tag
container_attrs = { }

faculty_tag     = "table" # Can be None to not sort by tag
faculty_attrs   = { "align" : "center"}

name_tag        = "h2" # Can be None to not sort by tag
name_attrs      = { }

email_tag       = None # Can be None to not sort by tag
email_attrs     = { "text" : re.compile("@")}

position_tag    = None # Can be None to not sort by tag
position_attrs  = { "text" : "Title:"}

dept_tag        = None # Can be None to not sort by tag
dept_attrs      = { "text" : "Dept:"}

output_file = "uri.csv"

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

CHUNK_SIZE  = 26
START_INDEX = 0

queries = [ "".join(tup) for tup in itertools.product(ALPHABET,repeat=2) ]

for i in range(0,26):
    try:
        with Pool() as pool:
            result = pool.map(readPage, queries[i*CHUNK_SIZE:(i+1)*CHUNK_SIZE])

            with open(ALPHABET[i] + "." + output_file, 'a+', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for process in result:
                    for row in process:
                        writer.writerow(row)
    except Exception as e:
        print(e)
        print("Error was caught on iteration {}/{}".format(i,25))
