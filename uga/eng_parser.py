# import libraries
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import html

names     = []
positions = []
emails    = []
depts     = []
directory_page = input("URL: ")

# query the website and return the html to the variable 'page'
page = urlopen(directory_page)

# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser').find(class_="content-inner")

# Get the smallest common group to make finding things easier
links = soup.find_all(href=re.compile("people"),class_="content")
# For every link we get that starts with people, we want to go to that page

i = 1;
for link in links:
    # Make a proper url
    suburl = re.sub("/people/[^/]*$",link['href'],directory_page)
    # Make a new soup for it
    subsoup = BeautifulSoup(urlopen(suburl),"html.parser")

    name = subsoup.find(class_="name").text
    name = name.split(",")[0]

    names.append(name)

    try:
        positions.append(subsoup.find("h2",class_="title").text.strip())
    except:
        print("\rPosition not found for {}".format(names[-1]))
        positions.append("")
    try:
        emails.append(subsoup.find(href=re.compile("mailto")).string.strip())
    except:
        print("\rEmail not found for {}".format(names[-1]))
        emails.append("")
    try:
        depts.append(subsoup.find("h3",class_="school").string)
        if depts[-1] == "":
            depts[-1] = subsoup.find(href=re.compile("/people/sch")).text
    except:
        print("\rDepartment not found for {}".format(names[-1]))
        depts.append("")

    print("\r{}/{}".format(i,len(links)), end = "")
    i += 1

with open('eng_output.csv', 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in range(0,len(names)):
        writer.writerow([names[x],emails[x],positions[x],depts[x]])
