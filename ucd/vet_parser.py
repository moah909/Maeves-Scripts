# import libraries
import re
import sys
sys.path.insert(0,'../')
from common.common import *
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from multiprocessing import Pool
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
container_attrs = { "id" : "main" }

faculty_tag     = "li" # Can be None to not sort by tag
faculty_attrs   = {}

name_tag        = "strong" # Can be None to not sort by tag
name_attrs      = { }

email_tag       = None # Can be None to not sort by tag
email_attrs     = { "text" : re.compile("@")}

position_tag    = None # Can be None to not sort by tag
position_attrs  = { "class_" : "tdtitle"}

dept_tag        = None # Can be None to not sort by tag
dept_attrs      = { "class_" : "value"}

output_file = "outputfile.csv"


# We can use command line input if it exists, otherwise prompt the user for input
directory_page = "file:///home/noah/Documents/Maeves-Scripts/ucd/vet.html"


# query the website and return the html to the variable 'page'
req = Request( directory_page,
   data=None,
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)

page = urlopen(req)

# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')

#dept = soup.find(class_="organization-unit").text

faculty = soup.find(container_tag,**container_attrs).find_all(faculty_tag,**faculty_attrs)[:-3]


def getPerson(link):

    person = BeautifulSoup(urlopen("http://www.vetmed.ucdavis.edu/faculty/" + link['href']), 'html.parser')

    name = person.find(name_tag,**name_attrs).text
    name = cleanName(name, flip=FLIP_NAME)

    try:
        email = person.find(email_tag,**email_attrs).strip()
    except:
        print("\rEmail not found for {}".format(name))
        email = ""
    try:
        position = person.find(class_="tdtitle").contents[1].contents[2]
        position = cleanPosition(position)
    except:
        print("\rPosition not found for {}".format(name))
        position = ""
    try:
        dept = person.find(class_="tdtitle").contents[1].contents[4]
        dept = cleanDepartment(dept)
    except:
        print("\rDepartment not found for {}".format(name))
        dept = ""

    return [name, email, position, dept]

output = []
links = soup(href=re.compile("results"))

for idx, link in enumerate(links):
    output.append(getPerson(link))
    print("\r{}/{}".format(idx,len(links)), flush=True, end="")

with open(output_file, 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in output:
        writer.writerow(x)
