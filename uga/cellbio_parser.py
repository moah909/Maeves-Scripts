# import libraries
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import html

names     = []
positions = []
emails    = []
dept     = "Cellular Biology"
quote_page = input("URL: ")

# query the website and return the html to the variable 'page'
page = urlopen(quote_page)

# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')

# Get the smallest common group to make finding things easier
links = soup.find_all(href=re.compile("directory"))
# For every link we get that starts with people, we want to go to that page

for link in links:
    # Make a proper url
    suburl = re.sub("/directory$",link['href'],quote_page)

    # Make a new soup for it
    subsoup = BeautifulSoup(urlopen(suburl),"html.parser")

    name = subsoup.find(class_="main-title-text").string

    # Get rid of Dr.
    name = re.sub("Dr.  ","",name)

    names.append(name)

    alleven = subsoup.find_all(class_="even")

    try:
        positions.append(alleven[1].string)
    except:
        print("Position not found for {}".format(names[-1]))
        positions.append("")
    try:
        emails.append(html.unescape(re.search(">(.+)</a>",alleven[4].contents[3].text).group(1)))
    except:
        print("Email not found for {}".format(names[-1]))
        emails.append("")


with open('cellbio_output.csv', 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in range(0,len(names)):
        writer.writerow([names[x],emails[x],positions[x],dept])
