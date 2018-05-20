# import libraries
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

names     = []
positions = []
emails    = []
dept     = input("Department: ")
quote_page = input("URL: ")

# query the website and return the html to the variable 'page'
page = urlopen(quote_page)

# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')

# Get the smallest common group to make finding things easier
faculty = soup.find_all(class_="views-row")
# For every link we get that starts with people, we want to go to that page
i = 1;
for person in faculty:
    # Make a proper url
    suburl = re.sub("/directory/[^/]*$",person.find("a")['href'],quote_page)

    # Make a new soup for it
    subsoup = BeautifulSoup(urlopen(suburl),"html.parser")

    name = subsoup.find("h1").findChild().string

    # Flip the name for VSU
    name = (" ".join(name.split(", ")[1::-1]))

    # Get rid of Dr.
    name = re.sub("Dr.  ","",name)

    names.append(name)
    try:
        positions.append(subsoup.find(class_="field_job_title").string)
    except:
        print("Position not found for {}".format(names[-1]))
        positions.append("")
    try:
        emails.append(subsoup.find(class_="field_email").string)
    except:
        print("Email not found for {}".format(names[-1]))
        emails.append("")

    print("\r{}/{}".format(i,len(faculty)), end = "", flush=True)
    i += 1

with open('output.csv', 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in range(0,len(names)):
        writer.writerow([names[x],emails[x],positions[x],dept])
