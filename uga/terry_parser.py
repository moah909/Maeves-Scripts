# import libraries
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import html

pages=[]
names=[]
positions = []
emails = []
quote_page = input('URL: ')
# quote_page = "http://www.agriculture.vsu.edu/faculty-and-staff/academic-faculty-staff.php"

# query the website and return the html to the variable 'page'
page = urlopen(quote_page)

# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')

dept = soup.find(class_="organization-unit").text

faculty = soup.find_all(class_="directory-list-item")

for person in faculty:
    if 'faculty' not in person['class']:
        continue # If its supposed to be hidden, skip it

    names.append(person.find("h1").text.strip().replace("\n"," "))
    try:
        emails.append(person.find(class_="email").text.strip())
    except:
        print("\rEmail not found for {}".format(names[-1]))
        emails.append("")
    try:
        positions.append(person.find(class_="title").text.strip())
    except:
        print("\rPosition not found for {}".format(names[-1]))
        positions.append("")

with open('terry_output.csv', 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in range(0,len(names)):
        writer.writerow([names[x],emails[x],positions[x],dept])
