# import libraries AND COLSA
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import html

pages     = []
names     = []
positions = []
emails    = []
directory_page = "https://law.unh.edu/faculty/all?page="

def getEmailFromSubpage(link):
    suburl = re.sub("/people/[^/]*$",link['href'],directory_page)
    subsoup = BeautifulSoup(urlopen(suburl),"html.parser")
    return subsoup.find(href=re.compile("mailto")).text

department = input("Department Number: ")

# query the website and return the html to the variable 'page'
page = urlopen(directory_page + department)

# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')

#dept = soup.find(selected="selected").text.strip()

dept = "Law"

# Get all entries in the table
faculty = soup.find_all("li",class_="media")

i = 1;

for person in faculty:
    name = person.find(class_="media-heading").text.strip()
    name = re.sub(" +"," ",name).strip()
    names.append(name)
    try:
        emails.append(person.find(href=re.compile('mailto')).text.strip())
    except:
        print("\rEmail not found for {}".format(names[-1]))
        emails.append("")
    try:
        blurb = person.find(class_="field-field-title").text.strip()
        position = blurb.split(" of ")[0]
        position = blurb.split(", ")[0]
    except:
        print("\rPosition not found for {}".format(names[-1]))
        position = ""

    positions.append(position)

    print("\r{}/{}".format(i,len(faculty)), end = "")
    i += 1

print()

with open('law_output.csv', 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in range(0,len(names)):
        try:
            writer.writerow([names[x],emails[x],positions[x],dept])
        except:
            print("There was an issue writing data for {}".format(names[x]))
