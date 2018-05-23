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
soup = BeautifulSoup(page, 'html.parser')

# Get all entries in the table
faculty = soup.find_all(class_="directory-member")

dept = soup.find(class_="section-title").text

i = 1;
for person in faculty:
    name = person.find(class_="as-heading-small").text.strip()
    names.append(name)
    try:
        emails.append(person.find(href=re.compile("mailto")).text)
    except:
        print("\rEmail not found for {}".format(names[-1]))
        emails.append("")
    try:
        position = person.find("p").text.strip()
        positions.append(position)
    except:
        print("\rPosition not found for {}".format(names[-1]))
        positions.append("")

    print("\r{}/{}".format(i,len(faculty)), end = "")
    i += 1

print()

with open('ed_output.csv', 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in range(0,len(names)):
        try:
            writer.writerow([names[x],emails[x],positions[x],dept])
        except:
            print("There was an issue writing data for {}".format(names[x]))

print("Type exit to exit")
while input() != 'exit':
    pass
