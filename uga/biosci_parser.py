# import libraries
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

names     = []
positions = []
emails    = []
dept     = "Biological Sciences"
quote_page = input("URL: ")

# query the website and return the html to the variable 'page'
page = urlopen(quote_page)

# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')

# Get the smallest common group to make finding things easier
links = soup.find_all(href=re.compile("people"))
# For every link we get that starts with people, we want to go to that page

for link in links:
    # Make a proper url
    suburl = re.sub("/directory/[^/]*$",link['href'],quote_page)

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
        emails.append(subsoup.find("a",href=re.compile("mailto")).string)
    except:
        print("Email not found for {}".format(names[-1]))
        emails.append("")


with open('biosci_output.csv', 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in range(0,len(names)):
        writer.writerow([names[x],emails[x],positions[x],dept])
