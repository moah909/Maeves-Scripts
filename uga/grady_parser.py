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
directory_page = input('URL: ')

def getEmailFromSubpage(link):
    subsoup = BeautifulSoup(urlopen(link),"html.parser")
    return subsoup.find(href=re.compile("mailto")).text

# query the website and return the html to the variable 'page'
page = urlopen(directory_page)

# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')

# Get all entries in the table
faculty = soup.find_all(class_="faculty-block")

i = 1;

for person in faculty:
    name = person.find(class_="faculty-block_name").text
    names.append(name)
    try:
        emails.append(getEmailFromSubpage(person.find("a")['href']))
    except:
        print("\rEmail not found for {}".format(names[-1]))
        emails.append("")
    try:
        position = person.find(class_="faculty-block_title").text
        positions.append(position)
    except:
        print("\rPosition not found for {}".format(names[-1]))
        positions.append("")
    try:
        dept = person.find(class_="faculty-block_department").text
        depts.append(dept)
    except:
        print("\rDepartment not found for {}".format(names[-1]))
        depts.append("")

    print("\r{}/{}".format(i,len(faculty)), end = "")
    i += 1

print()

with open('grady_output.csv', 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in range(0,len(names)):
        try:
            writer.writerow([names[x],emails[x],positions[x],dept])
        except:
            print("There was an issue writing data for {}".format(names[x]))

print("Type exit to exit")
while input() is not 'exit':
    pass
