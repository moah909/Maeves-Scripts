# import libraries
import re
import sys
sys.path.insert(0,'../')
from common.common import *
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import csv
import html
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

pages     = []
names     = []
positions = []
emails    = []
depts     = []

def getPositionFromSubpage(link):
    suburl = re.sub("[^/]*$",link['href'],directory_page)
    print(suburl)
    subsoup = BeautifulSoup(urlopen(suburl),"html.parser")
    return subsoup.find(class_="title").text

EMAIL_FROM_HREF = True
FLIP_NAME       = False

container_tag   = None # Can be None to not sort by tag
container_attrs = { "class_" : "view-directory-list"}

faculty_tag     = None # Can be None to not sort by tag
faculty_attrs   = { "class_" : "results"}

name_tag        = None # Can be None to not sort by tag
name_attrs      = { "class_" : "name"}

email_tag       = None # Can be None to not sort by tag
email_attrs     = { "class_" : "staffEmail"}

position_tag    = None # Can be None to not sort by tag
position_attrs  = { "class_" : "staffMember"}

dept_tag        = None # Can be None to not sort by tag
dept_attrs      = { "class_" : "department"}

output_file = "outputfile.csv"


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

    try:
        dept = person.find(dept_tag,**dept_attrs).text
        dept = cleanDepartment(dept)
        depts.append(dept)
    except:
        print("\rDepartment not found for {}".format(name))
        depts.append("")

    if "Clinic" in dept:
        continue

    names.append(name)

    try:
        if(EMAIL_FROM_HREF):
            emails.append(person.find(email_tag,**email_attrs)['href'][7:])
        else:
            emails.append(person.find(email_tag,**email_attrs).text.strip())
    except:
        print("\rEmail not found for {}".format(name))
        emails.append("")
    try:
        position = getPositionFromSubpage(person.find(position_tag,**position_attrs))
        position = cleanPosition(position)
        positions.append(position)
    except KeyError:
        print("\rPosition not found for {}".format(name))
        positions.append("")
    try:
        dept = person.find(dept_tag,**dept_attrs).text
        dept = cleanDepartment(dept)
        depts.append(dept)
    except:
        print("\rDepartment not found for {}".format(name))
        depts.append("")

with open(output_file, 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in range(0,len(names)):
        writer.writerow([names[x],emails[x],positions[x],depts[x]])
