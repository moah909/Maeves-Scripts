# import libraries
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import html

pages     = []
names     = []
positions = []
emails    = []
depts     = []
directory_page = "https://carsey.unh.edu/people/faculty"

def getEmailFromSubpage(link):
    suburl = re.sub("/people/[^/]*$",link['href'],directory_page)
    subsoup = BeautifulSoup(urlopen(suburl),"html.parser")
    return subsoup.find(href=re.compile("mailto")).text

# query the website and return the html to the variable 'page'
page = urlopen(directory_page)

# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')

# Get all entries in the table
faculty = soup.find_all(class_="contextual-links-region")

i = 1;

for person in faculty:
    name = person.find(class_="views-field-title").text.strip()
    names.append(name)
    try:
        emails.append(getEmailFromSubpage(person.find("a")))
    except:
        print("\rEmail not found for {}".format(names[-1]))
        emails.append("")
    try:
        blurb = person.find(class_="views-field-field-title").find("p").text
        position = blurb.split(", ")[0]

        if len(blurb.split(", ")) < 2:
            dept = "School of Public Policy"
        else:
            dept = blurb.split(", ")[1]
    except:
        print("\rPosition or department not found for {}".format(names[-1]))
        position = ""
        dept     = ""

    positions.append(position)
    depts.append(dept)

    print("\r{}/{}".format(i,len(faculty)), end = "")
    i += 1

print()

with open('carsey_output.csv', 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in range(0,len(names)):
        try:
            writer.writerow([names[x],emails[x],positions[x],depts[x]])
        except:
            print("There was an issue writing data for {}".format(names[x]))

print("Type exit to exit")
while input() != 'exit':
    pass
