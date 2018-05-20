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
directory_page = input('URL: ')

# query the website and return the html to the variable 'page'
page = urlopen(directory_page)

# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')

dept = soup.find(class_="active").text

faculty = soup.find_all(class_="vcard")

for person in faculty:

    names.append(person.find("p",class_="fn").text.strip().replace("\n"," "))
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

with open('fcs_output.csv', 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in range(0,len(names)):
        writer.writerow([names[x],emails[x],positions[x],dept])
