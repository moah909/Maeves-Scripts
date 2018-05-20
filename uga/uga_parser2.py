# import libraries
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import html

# If it follows a link with a bad name, just skip it
BAD_NAMES = ["Students","Staff","Faculty","Instructor","Directory","Assistant","Alumni"]

names     = []
positions = []
emails    = []
dept       = input("Department: ")
quote_page = input("URL: ")

# query the website and return the html to the variable 'page'
page = urlopen(quote_page)

# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')

# Get the smallest common group to make finding things easier
links = soup.find_all(href=re.compile("directory"))
# For every link we get that starts with people, we want to go to that page
i = 1;
for link in links:
    # Make a proper url
    suburl = re.sub("/directory/.*$",link['href'],quote_page)
    # Make a new soup for it
    subsoup = BeautifulSoup(urlopen(suburl),"html.parser")

    name = subsoup.find(class_="main-title-text").string

    # Get rid of Dr.
    name = re.sub("Dr.  ","",name)

    if any(bad_name in name for bad_name in BAD_NAMES ):
        print("\rFound bad name, skipping")
        print("\r{}/{}".format(i,len(links)), end = "")
        i += 1
        continue

    names.append(name)

    alleven = subsoup.find_all(class_="even")

    try:
        positions.append(subsoup.find(class_="field-name-field-job-title").find(class_="even").text)
    except:
        print("\rPosition not found for {}".format(names[-1]))
        positions.append("")
    try:
        emails.append(subsoup(href=re.compile("mailto"))[0].string)
    except:
        try:
            emails.append(html.unescape(re.search(">(.+)</a>",subsoup.find(class_="field-type-email").text).group(1)))
        except:
            print("\rEmail not found for {}".format(names[-1]))
            emails.append("")

    print("\r{}/{}".format(i,len(links)), end = "")
    i += 1

with open('output2.csv', 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in range(0,len(names)):
        writer.writerow([names[x],emails[x],positions[x],dept])
