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
import html

def readDept(directory_page):
    current_page = 0
    last_page = -1
    retval = []

    while True:

        page = urlopen(directory_page+"&page={}".format(current_page))

        # parse the html using beautiful soup and store in variable 'soup'
        soup = BeautifulSoup(page, 'html.parser')

        if last_page == -1:
            last_page = int(soup.find(class_="pager-last").find("a")['href'].split("=")[-1])

        #dept = soup.find(class_="organization-unit").text

        faculty = soup.find(container_tag,**container_attrs).find_all(faculty_tag,**faculty_attrs)

        print("\rPage {}/{}".format(current_page,last_page),end="",flush=True)

        for person in faculty:

            if person.find(class_="type").text != "appointed personnel":
                continue

            name = person.find(name_tag,**name_attrs).text
            name = cleanName(name, flip=True)
            try:
                if(EMAIL_FROM_HREF):
                    email = (person.find(email_tag,**email_attrs)['href'][7:-1])
                else:
                    email = (person.find(email_tag,**email_attrs).text.strip())
            except:
                print("\rEmail not found for {}".format(names[-1]))
                email = ("")
            try:
                position = person.find(position_tag,**position_attrs).text
                position = cleanPosition(position,delim=",")
            except:
                print("\rPosition not found for {}".format(names[-1]))
                positions = ("")
            try:
                dept = person.find(dept_tag,**dept_attrs).text
                dept = cleanDepartment(dept)
            except:
                print("\rDepartment not found for {}".format(names[-1]))
                dept = ""

            retval.append([name,email,position,dept])

        if current_page == last_page:
            break

        current_page += 1
    print(" Departments: {}/{}".format(start_index*10,len(DEPARTMENTS)))
    return retval

pages     = []
directory_page = []
processes = []


DEPARTMENTS = ["Accounting",
"Aerospace & Mechanical Engr",
"Africana Studies",
"Agric & Biosystems Engr-Ext",
"Agric Biosystems Engr-Ins",
"Agric & Biosystems Engr-Res",
"Agricultural Education-Ext",
"Agricultural Education-Ins",
"Agricultural Resource Econ-Ext",
"Agricultural Resource Econ-Res",
"American Indian Studies Prog",
"Anesthesiology",
"Animal&Biomedical Sciences-Ext",
"Animal&Biomedical Sciences-Ins",
"Animal&Biomedical Sciences-Res",
"Animal Sciences-Res",
"Apache County Office",
"Applied Mathematics GIDP",
"Arizona Telemedicine Program",
"Astronomy",
"Atmospheric Sciences",
"Biomedical Engineering",
"Cellular & Molecular Medicine",
"Chemical & Environmental Engr",
"Chemistry & Biochemistry - Med",
"Chemistry & Biochemistry - Sci",
"Civil Engr and Engr Mechanics",
"Classics",
"Clinical Teaching",
"Cognitive Science",
"College of Nursing",
"College of Optical Sciences",
"Colleges Letters Arts Sci Adm",
"Communication",
"Community Environment & Policy",
"Computer Science",
"Continuing&Professional Educ",
"Dept of Emergency Medicine",
"Disability Psychoeduc Studies",
"East Asian Studies",
"Ecology & Evolutionary Biology",
"Economics",
"Educational Psychology",
"Electrical and Computer Engr",
"Eller Undergraduate Programs",
"English",
"English as a Second Language",
"Entomology-Res",
"Epidemiology and Biostatistics",
"Family and Community Medicine",
"Finance",
"Fine Arts Administration",
"French and Italian",
"Gender and Womens Studies",
"Geosciences",
"German Studies",
"GIDP Neuroscience",
"Health Promotion Sciences",
"History",
"Human Resources",
"Hydrology and Water Resources",
"Immunobiology",
"Journalism",
"Karl Eller Grad School of Mgmt",
"Law Instruction",
"Legislative&CommunityRelations",
"Linguistics",
"Management and Organizations",
"Management Information Systems",
"Maricopa Ag Center-Ext",
"Maricopa Agriculture Ctr-Res",
"Marketing",
"Materials Science & Engr",
"Mathematics",
"Medical Imaging",
"Medical Student Education",
"Medicine",
"Medieval Reformation Studies",
"Mexican American Studies",
"Military Aerospace Studies",
"Military Science Tactics",
"Mining & Geological Engr",
"Molecular and Cellular Biology",
"Museum of Art",
"Naval Science",
"Neurology",
"Neuroscience",
"Nutritional Sciences-Ext",
"Nutritional Sciences-Ins",
"Nutritional Sciences-Res",
"Obstetrics and Gynecology",
"Ophthalmology & Vision Science",
"Orthopedic Surgery",
"Otolaryngology",
"Pathology",
"Pediatrics",
"Pharmaceutical Sciences",
"Pharmacology",
"Pharmacology and Toxicology",
"Pharmacy Administration",
"Pharmacy Practice and Science",
"Philosophy",
"Physics",
"Physiology",
"Planetary Sciences",
"Psychiatry",
"Psychology",
"Radiation Chem & Bio Safety",
"Radiation Oncology",
"Religious Studies Program",
"Risk Management and Safety",
"Russian and Slavic Studies",
"Sch Middle E/N African Studies",
"Sch of Family Consumer Sci-Res",
"Sch of Family & Consum Sci-Ext",
"Sch of Family & Consum Sci-Ins",
"Sch of Geography & Development",
"Sch of Info Res & Library Sci",
"Sch of Info: Sci Tech & Arts",
"Sch of Intl Lang Lit & Culture",
"Sch of Landscape Architecture",
"Sch of Mind Brain & Behavior",
"Sch of Nat Resource&Enviro-Ext",
"Sch of Nat Resource&Enviro-Res",
"Sch of Natural Resources-Ins",
"School of Anthropology",
"School of Architecture",
"School of Art",
"School of Dance",
"School of Govt & Public Policy",
"School of Music",
"School of Plant Sciences-Ext",
"School of Plant Sciences-Ins",
"School of Plant Sciences-Res",
"Sch Theatre Film & Television",
"Soc & Behavioral Sci Rsch Inst",
"Social & Behavioral Sci Admin",
"Sociology",
"Soil Water and Enviro Sci-Ext",
"Soil Water and Enviro Sci-Ins",
"Soil Water Enviro Sci-Res",
"Spanish and Portuguese",
"Speech Language & Hearing Sci",
"Surgery",
"Surgery-Clinical Residents",
"Systems and Industrial Engr",
"Systems Control",
"Teachg Learning Sociocult Stds",
"Water Resources Resrch Ctr-Ext",
"Water Resources Rsch Ctr-Res"]

EMAIL_FROM_HREF = False

container_tag   = None # Can be None to not sort by tag
container_attrs = { "role" : "main"}

faculty_tag     = None # Can be None to not sort by tag
faculty_attrs   = { "class_" : "views-row"}

name_tag        = "h3" # Can be None to not sort by tag
name_attrs      = {}

email_tag       = "a" # Can be None to not sort by tag
email_attrs     = { "class_" : "mailto"}

position_tag    = None # Can be None to not sort by tag
position_attrs  = { "class_" : "department"}

dept_tag        = None # Can be None to not sort by tag
dept_attrs      = { "class_" : "degree"}

output_file = "uoa.csv"

for start_index in range(0,5):
        directory_page.append("https://www.info.iastate.edu/individuals/advanced?last_name=&first_name=&email=&individual_type=faculty_staff&"+urlencode(dict(("department[{}]".format(i),DEPARTMENTS[start_index*10+i]) for i in range(0,10))))

with Pool() as pool:
    result = pool.map(readDept, directory_page)

    with open(output_file, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for process in result:
            for row in process:
                writer.writerow(row)
