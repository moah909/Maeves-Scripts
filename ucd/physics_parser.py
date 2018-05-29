# import libraries
import re
import sys
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
dept      = "Physics"

EMAIL_FROM_HREF = False
FLIP_NAME       = True

container_tag   = None # Can be None to not sort by tag
container_attrs = { "class_" : "repeating_content_block"}

faculty_tag     = None # Can be None to not sort by tag
faculty_attrs   = { "class_" : "faculty-column"}

name_tag        = "a" # Can be None to not sort by tag
name_attrs      = { }

email_tag       = None # Can be None to not sort by tag
email_attrs     = { "class_" : "value"}

position_tag    = None # Can be None to not sort by tag
position_attrs  = { "class_" : "value"}\

dept_tag        = None # Can be None to not sort by tag
dept_attrs      = { "class_" : "value"}

output_file = "physics.csv"


# We can use command line input if it exists, otherwise prompt the user for input
if len(sys.argv) < 2:
    directory_page = input('URL: ')
else:
    directory_page = sys.argv[1]

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

faculty = soup.find(container_tag,**container_attrs).find_all(faculty_tag,**faculty_attrs)

for person in faculty:

    name = person.find(name_tag,**name_attrs).text
    name = cleanName(name, flip=FLIP_NAME)
    names.append(name)

    blurb = person.find("br").contents
    try:
        emails.append(blurb[3].contents[0])
    except:
        try:
            emails.append(person.contents[5].contents[0])
        except:
            print("\rEmail not found for {}".format(names[-1]))
            emails.append("")
    try:
        position = blurb[0]
        position = cleanPosition(position)
        positions.append(position)
    except:
        try:
            position = person.contents[2]
            position = cleanPosition(position)
            positions.append(position)
        except:
            print("\rPosition not found for {}".format(names[-1]))
            positions.append("")



with open(output_file, 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in range(0,len(names)):
        writer.writerow([names[x],emails[x],positions[x],dept])
