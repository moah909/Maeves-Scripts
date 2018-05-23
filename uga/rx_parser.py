# import libraries
import re
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import csv
import html

pages     = []
names     = []
positions = []
emails    = []
depts     = []

DEPARTMENT_CLASSES = [
'intl-biomedical-regulatory-sciences-and-clinical-trials-programs',
'pharmaceutical-and-biomedical-sciences',
'pharmaceutical-and-biomedical-sciences']
quote_page = input('URL: ')
# quote_page = "http://www.agriculture.vsu.edu/faculty-and-staff/academic-faculty-staff.php"

# query the website and return the html to the variable 'page'
req = Request( quote_page,
   data=None,
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)

page = urlopen(req)

# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')

#dept = soup.find(class_="organization-unit").text

faculty = soup.find_all(class_="bio-box")

for person in faculty:
    if set(person.parent['class']).isdisjoint(set(DEPARTMENT_CLASSES)):
        continue # If its supposed to be hidden, skip it

    names.append(person.find("h5").text.strip().split(",")[0])
    try:
        emails.append(person.find(class_="email-address").text.strip())
    except:
        print("\rEmail not found for {}".format(names[-1]))
        emails.append("")
    try:
        positions.append(person.find(class_="title").text.strip())
    except:
        print("\rPosition not found for {}".format(names[-1]))
        positions.append("")
    try:
        depts.append(person.find(class_="dept").text.strip())
    except:
        print("\rDepartment not found for {}".format(names[-1]))
        depts.append("")

with open('rx_output.csv', 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in range(0,len(names)):
        writer.writerow([names[x],emails[x],positions[x],depts[x]])
