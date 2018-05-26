# import libraries CAN BE USED FOR COLA
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import html

pages     = []
names     = []
positions = []
emails    = []
directory_page = input("URL: ")

def getEmailFromSubpage(link):
    suburl = re.sub("/people/[^/]*$",link['href'],directory_page)
    subsoup = BeautifulSoup(urlopen(suburl),"html.parser")
    return subsoup.find(href=re.compile("mailto")).text

# query the website and return the html to the variable 'page'
page = urlopen(directory_page)

# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')

dept = soup.find(class_="department-branding").text.strip()

# Get all entries in the table
faculty = soup.find_all(class_="thecontent")

i = 1;

for person in faculty:
    data = person.text.strip().split("\n")
    name = data[0]
    names.append(name)
    try:
        emails.append(data[3])
    except:
        print("\rEmail not found for {}".format(names[-1]))
        emails.append("")
    try:
        position = data[1]
        position = position.split(" of ")[0]
        position = position.split(" in ")[0]
    except:
        print("\rPosition not found for {}".format(names[-1]))
        position = ""

    positions.append(position)

    print("\r{}/{}".format(i,len(faculty)), end = "")
    i += 1

print()

with open('cola_output.csv', 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in range(0,len(names)):
        try:
            writer.writerow([names[x],emails[x],positions[x],dept])
        except:
            print("There was an issue writing data for {}".format(names[x]))
