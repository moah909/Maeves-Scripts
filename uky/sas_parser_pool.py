# import libraries
import re
import sys
from multiprocessing import Pool, Queue
sys.path.insert(0,'../')
from common.common import *
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import csv

def getDept(link,base_url):
    suburl = re.sub("[^/]*$",link['href'],base_url)
    subsoup = BeautifulSoup(urlopen(suburl),"html.parser")
    return subsoup.find("h1").text

def readPage(page_num):
    directory_page = ("https://www.as.uky.edu/faculty?page={}".format(page_num))

    retval = []

    page = urlopen(directory_page+"&page={}".format(page_num))
    soup = BeautifulSoup(page, 'html.parser')

    #dept = soup.find(class_="organization-unit").text
    faculty = soup.find(container_tag,**container_attrs).find_all(faculty_tag,**faculty_attrs)

    print("\rPage {}/{}".format(page_num,pages),end="",flush=True)

    for person in faculty:

        name = person.find(name_tag,**name_attrs).text
        name = cleanName(name)
        try:
            position = person.find(position_tag,**position_attrs).text
            position = cleanPosition(position,delim=",")
            if("Graduate Assistant" in position):
                continue
        except:
            print("\rPosition not found for {}".format(name))
            position = ""
        try:
            email = person.find(email_tag,**email_attrs).text
        except:
            print("\rEmail not found for {}".format(name))
            email = ""
            continue
        try:
            dept = getDept(person.find(name_tag,**name_attrs).a,directory_page)
            dept = cleanDepartment(dept)
        except:
            print("\rDepartment not found for {}".format(name))
            dept = ""

        retval.append([name,email,position,dept])

    print("Pages: {}/{}".format(page_num,pages))
    return retval

pages          = 14
directory_page = []
processes      = []


EMAIL_FROM_HREF = True

container_tag   = "tbody" # Can be None to not sort by tag
container_attrs = { }

faculty_tag     = "tr" # Can be None to not sort by tag
faculty_attrs   = { }

name_tag        = None # Can be None to not sort by tag
name_attrs      = { "class_":"name"}

email_tag       = None # Can be None to not sort by tag
email_attrs     = { "class_":"email" }

position_tag    = None # Can be None to not sort by tag
position_attrs  = { "class_" : "position"}

dept_tag        = None # Can be None to not sort by tag
dept_attrs      = { "text" : "Dept:"}

output_file = "sas.csv"

with Pool() as pool:
    result = pool.map(readPage, range(0,15))

    with open(output_file, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for process in result:
            for row in process:
                writer.writerow(row)
