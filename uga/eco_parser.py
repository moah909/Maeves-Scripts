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
dept       = "Odum School of Ecology"
directory_page = input("URL: ")

# query the website and return the html to the variable 'page'
page = urlopen(directory_page)

# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')

# Get the smallest common group to make finding things easier
links = soup.find_all(href=re.compile("facultyMember"))
# For every link we get that starts with people, we want to go to that page
i = 1;
for link in links:
    # Make a proper url
    suburl = re.sub("[^/]*$",link['href'],directory_page)
    # Make a new soup for it
    subsoup = BeautifulSoup(urlopen(suburl),"html.parser").find(id="page")

    names.append(subsoup.find("h2").string)

    try:
        position = subsoup.find("p",class_="").text
        position = position.split("\r")[0].strip()
        positions.append(position)
    except:
        print("\rPosition not found for {}".format(names[-1]))
        positions.append("")
    try:
        emails.append(subsoup.find(href=re.compile("mailto")).string)
    except:
        print("\rEmail not found for {}".format(names[-1]))
        emails.append("")

    print("\r{}/{}".format(i,len(links)), end = "")
    i += 1

with open('odum_output.csv', 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in range(0,len(names)):
        writer.writerow([names[x],emails[x],positions[x],dept])
