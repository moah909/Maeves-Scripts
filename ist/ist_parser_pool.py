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
import html

def readDept(directory_page):
    current_page = 0
    last_page = -1
    retval = []

    while True:

        page = urlopen(directory_page+"&page={}".format(current_page))

        # parse the html using beautiful soup and store in variable 'soup'
        soup = BeautifulSoup(page, 'html.parser')

        if last_page == -1:
            nav_bar = soup.find(class_="wd-Pagination").find_all("a")
            if nav_bar[-1].text == "Last":
                last_page = int(nav_bar[-1]['href'].split("=")[-1])
            else:
                last_page = int(nav_bar[-2]['href'].split("=")[-1])

        #dept = soup.find(class_="organization-unit").text
        print(nav_bar)
        faculty = soup.find(container_tag,**container_attrs).find_all(faculty_tag,**faculty_attrs)

        print("\rPage {}/{}".format(current_page,last_page),end="",flush=True)

        for person in faculty:

            if person.find(class_="type").text != "appointed personnel":
                continue

            name = person.find(name_tag,**name_attrs).text
            name = cleanName(name, flip=True)
            try:
                if(EMAIL_FROM_HREF):
                    email = (person.find(email_tag,**email_attrs)['href'][7:-1])
                else:
                    email = (person.find(email_tag,**email_attrs).text.strip())
            except:
                print("\rEmail not found for {}".format(names[-1]))
                email = ("")
            try:
                position = person.find(position_tag,**position_attrs).text
                position = cleanPosition(position,delim=",")
            except:
                print("\rPosition not found for {}".format(names[-1]))
                positions = ("")
            try:
                dept = person.find(dept_tag,**dept_attrs).text
                dept = cleanDepartment(dept)
            except:
                print("\rDepartment not found for {}".format(names[-1]))
                dept = ""

            retval.append([name,email,position,dept])

        if current_page == last_page:
            break

        current_page += 1
    print(" Departments: /{}".format(len(DEPARTMENTS)))
    return retval

pages     = []
directory_page = []
processes = []


DEPARTMENTS = ["Accounting"]

EMAIL_FROM_HREF = False

container_tag   = None # Can be None to not sort by tag
container_attrs = { "role" : "main"}

faculty_tag     = None # Can be None to not sort by tag
faculty_attrs   = { "class_" : "views-row"}

name_tag        = "h3" # Can be None to not sort by tag
name_attrs      = {}

email_tag       = "a" # Can be None to not sort by tag
email_attrs     = { "class_" : "mailto"}

position_tag    = None # Can be None to not sort by tag
position_attrs  = { "class_" : "department"}

dept_tag        = None # Can be None to not sort by tag
dept_attrs      = { "class_" : "degree"}

output_file = "uoa.csv"

for department in DEPARTMENTS:
        directory_page.append("https://www.info.iastate.edu/individuals/advanced?last_name=&first_name=&email=&individual_type=faculty_staff&{}"
                                .format(urlencode({"department":department,"page":""})))
readDept(directory_page[0])

with Pool() as pool:
    result = pool.map(readDept, directory_page)

    with open(output_file, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for process in result:
            for row in process:
                writer.writerow(row)
