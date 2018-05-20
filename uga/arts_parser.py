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
directory_page = input('URL: ')

# query the website and return the html to the variable 'page'
page = urlopen(directory_page)

# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser').find(class_="views-responsive-grid")

dept = "Art"

# Get all entries in the table
faculty = soup.find_all(class_="views-column")

i = 1;

for person in faculty:
    name = person.find(class_="views-field-field-last-name").text
    name = re.sub(" +"," ",name).strip()
    names.append(name)
    try:
        emails.append(html.unescape(re.search(">(.+)</a>",person.find(class_="views-field-field-email").text).group(1)))
    except:
        print("\rEmail not found for {}".format(names[-1]))
        emails.append("")
    try:
        position = person.find(class_="views-field-field-job-title").text.strip()
        if not position:
            position = person.find(class_="views-field-field-job-title-1").text.strip()
        positions.append(position)
    except:
        print("\rPosition not found for {}".format(names[-1]))
        positions.append("")

    print("\r{}/{}".format(i,len(faculty)), end = "", flush=True)
    i += 1

print()

with open('arts_output.csv', 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in range(0,len(names)):
        try:
            writer.writerow([names[x],emails[x],positions[x],dept])
        except:
            print("There was an issue writing data for {}".format(names[x]))
