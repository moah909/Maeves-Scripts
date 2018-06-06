# import libraries
import re
import sys
from multiprocessing import Pool
sys.path.insert(0,'../')
from common.common import *
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import csv
import html

pages     = []
names     = []
positions = []
emails    = []
depts     = []

EMAIL_FROM_HREF = False
FLIP_NAME       = False

container_tag   = None # Can be None to not sort by tag
container_attrs = { "id" : "cn-list-body"}

faculty_tag     = None # Can be None to not sort by tag
faculty_attrs   = { "class_" : "vcard"}

name_tag        = None # Can be None to not sort by tag
name_attrs      = { "class_" : "n"}

email_tag       = None # Can be None to not sort by tag
email_attrs     = { "class_" : "value"}

position_tag    = None # Can be None to not sort by tag
position_attrs  = { "class_" : "title"}

dept_tag        = None # Can be None to not sort by tag
dept_attrs      = { "class_" : "org"}

output_file = "eng.csv"

# We can use command line input if it exists, otherwise prompt the user for input
directory_page = "https://faculty.engineering.ucdavis.edu/pg/"

def getPage(page_num):
    page = urlopen(directory_page+str(page_num))

    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')

    #dept = soup.find(class_="organization-unit").text

    faculty = soup.find(container_tag,**container_attrs).find_all(faculty_tag,**faculty_attrs)

    for idx, person in enumerate(faculty):

        name = person.find(name_tag,**name_attrs).text
        name = cleanName(name, flip=FLIP_NAME)
        names.append(name)

        try:
            link = person.find("a")

            subsoup = BeautifulSoup(urlopen(link['href']),"html.parser")
            email = subsoup.find(text=re.compile("[Ee]mail:"))[7:]
            emails.append(email)
        except:
            print("\rEmail not found for {}".format(name))
            emails.append("")
        try:
            position = person.find(position_tag,**position_attrs).text
            position = cleanPosition(position)
            positions.append(position)
        except:
            print("\rPosition not found for {}".format(name))
            positions.append("")
        try:
            dept = person.find(dept_tag,**dept_attrs).text
            dept = cleanDepartment(dept)
            depts.append(dept)
        except:
            print("\rDepartment not found for {}".format(name))
            depts.append("")

        print("\r{}/{}".format(idx,len(faculty)), end = "", flush=True)
    print("\r{}/{} ({})".format(len(faculty),len(faculty), page_num), flush=True)

for i in range(1,14):
    getPage(i)

with open(output_file, 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in range(0,len(names)):
        writer.writerow([names[x],emails[x],positions[x],depts[x]])
