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
name_boxes = []
position_boxes = []
email_boxes = []
quote_page = input('URL: ')
# quote_page = "http://www.agriculture.vsu.edu/faculty-and-staff/academic-faculty-staff.php"

# query the website and return the html to the variable 'page'
page = urlopen(quote_page)

# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')

dept = "Lamar Dodd School of Art"


name_boxes.extend(soup.find_all(class_="views-field-field-last-name"))
try:
     position_boxes.extend(soup.find_all(class_= re.compile("views-field-field-job-title")))
except Exception:
     print("Manually check positions, there's a mismatch")
     positions.append("")

email_boxes.extend(soup.find_all(class_="views-field-field-email"))
#email_boxes.extend(soup.find_all(href=re.compile("mailto"))) # look for attributes with href = "mailto..."
#sections.append(sections[x].find("a").attrs['name'])

for x in range(0,len(name_boxes)):
    names.append(name_boxes[x].text.strip())
    try:
     positions.append(position_boxes[x].findChild().string)
    except Exception:
     print("Manually check positions, there's a mismatch")
     positions.append("")

    try:
     emails.append(html.unescape(re.search(">(.+)</a>",email_boxes[x].findChild().text).group(1)))
    except Exception:
     print("Manually check emails, there's a mismatch")
     emails.append("")

    #semails.append(email_boxes[x].string)
    # emails.append(email_boxes[x].attrs["href"][7:]) # [7:] cuts off first 7 chacters "mailto:"

with open('arts_output.csv', 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in range(0,len(names)):
        writer.writerow([names[x],emails[x],positions[x],dept])
