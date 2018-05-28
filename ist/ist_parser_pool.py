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

def processEmail(email):
    parts = re.findall("\'([\w\.]*)\'",email)
    email = "@".join(parts[0:2])
    return email

def readDept(department,dept_idx):
    current_page = 0
    last_page = -1
    retval = []
    directory_page = ("https://www.info.iastate.edu/individuals/advanced?last_name=&first_name=&email=&individual_type=faculty_staff&{}"
                            .format(urlencode({"department":department,"page":""})))

    while True:

        page = urlopen(directory_page+"&page={}".format(current_page))

        # parse the html using beautiful soup and store in variable 'soup'
        soup = BeautifulSoup(page, 'html.parser')

        if last_page == -1:
            nav_bar = soup.find(class_="wd-Pagination").find_all("a")
            if nav_bar[-1].text == "Last":
                last_page = int(nav_bar[-1]['href'].split("=")[-1])
            else:
                last_page = int(nav_bar[-2]['href'].split("=")[-1])

        #dept = soup.find(class_="organization-unit").text
        faculty = soup.find(container_tag,**container_attrs).find_all(faculty_tag,**faculty_attrs)

        print("\rPage {}/{}".format(current_page,last_page),end="",flush=True)

        for person in faculty:

            suburl = re.sub("/individuals/.*$",person['href'],directory_page)
            subsoup = BeautifulSoup(urlopen(suburl),"html.parser")

            try:
                classification = subsoup.find(text="Classification:").next
                if classification == " Graduate":
                    continue
            except AttributeError:
                pass

            name = subsoup.find(name_tag,**name_attrs).text
            name = cleanName(name, flip=True)
            try:
                position = subsoup.find(position_tag,**position_attrs).next
                position = cleanPosition(position,delim=",")
                if("Graduate Assistant" in position):
                    continue
            except:
                print("\rPosition not found for {}".format(name))
                position = ""
            try:
                email = processEmail(subsoup.find(email_tag,**email_attrs))
            except:
                print("\rEmail not found for {}".format(name))
                email = ""
            try:
                dept = subsoup.find(dept_tag,**dept_attrs).next
                dept = cleanDepartment(dept)
            except:
                print("\rDepartment not found for {}".format(name))
                dept = ""

            retval.append([name,email,position,dept])

        if current_page == last_page:
            break

        current_page += 1
    print(" Departments: {}/{}".format(dept_idx+1,len(DEPARTMENTS)))
    return retval

pages          = []
directory_page = []
processes      = []


DEPARTMENTS = ["Accounting",
"Advertising",
"Aerospace Eng",
"Ag & Life Sci Administration",
"Agricultural & Biosystems Engineering",
"Agricultural & Biosystems Engr - AGLS",
"Agricultural & Biosystems Engr - Engr",
"Agricultural and Biosystems Engineering",
"Agricultural and Biosystems Engineering (AGLS)",
"Agricultural and Life Sciences Education",
"Agricultural Biochemistry",
"Agricultural Business",
"Agricultural Education & Studies",
"Agricultural Education and Studies",
"Agricultural Engineering",
"Agricultural Studies",
"Agricultural Systems Technology",
"Agriculture and Life Sciences Exploration",
"Agriculture and Society",
"Agriculture Certificate (Non-Degree)",
"Agriculture Communications",
"Agriculture Experiment Station",
"Agriculture Specials",
"Agronomy",
"Air Force Aerospace Studies",
"Alumni Association",
"Ames Laboratory of US DOE",
"Animal Ecology",
"Animal Science",
"Anthropology",
"Apparel, Educational Studies, and Hospitality Mgmt",
"Apparel, Events, and Hospitality Management",
"Apparel, Merchandising, and Design",
"Architecture",
"Architecture-Professional Degree",
"Art & Design",
"Art and Design",
"Art and Design (Bachelor of Arts)",
"Art and Visual Culture",
"Assoc VP Enrollment Mgmt",
"Athletic Department",
"Athletic Training",
"Attending Veterinarian",
"Baker Center Bioinformatics/Biol Stat",
"Biochemistry",
"Biochemistry, Biophysics & Molec Biology",
"Biochemistry, Biophysics and Molecular Biol (AGLS)",
"Biochemistry, Biophysics and Molecular Biol (LAS) ",
"Biochemistry/Biophysics & Molc Biol-AGLS",
"Biochemistry/Biophysics & Molc Biol-LAS",
"Bioeconomy Institute",
"Bioinformatics & Computational Biology",
"Bioinformatics and Computational Biology",
"Biological Systems Engineering",
"Biological/Pre-Medical Illustration",
"Biology",
"Biology (AGLS)",
"Biomedical Engineering",
"Biomedical Sciences",
"Biophysics",
"Biosafety Inst Genetically Modfd At Prod",
"Biotechnology",
"Board of Regents",
"Bookstore",
"Brenton Center for Ag Instr Tech Transf",
"Business",
"Business Administration",
"Business Career Services",
"Business Economics",
"Business Graduate Program",
"Business Services",
"Business Specials (Non-Degree)",
"Business Undeclared",
"Business Undergraduate Program",
"Campus Dining Services",
"Campus Organizations",
"Carrie Chapman Catt Center",
"Center for Agricultural & Rural Develop",
"Center for Agricultural Law & Taxation",
"Center for Biorenewable Chemicals",
"Center for Crops Utilization Research",
"Center for Excellence in Learn & Teach",
"Center for Food Security/Public Health",
"Center for Industrial Research & Service",
"Center for Sustainable Rural Livelihoods",
"Chemical & Biological Engineering",
"Chemical and Biological Engineering",
"Chemical Engineering",
"Chemistry",
"Chemistry Stores",
"Child Care Services",
"Child, Adult, and Family Services",
"Civil Engineering",
"Civil, Construction & Environmental Eng",
"Civil, Construction and Environmental Engineering ",
"Communication Studies",
"Communities - Extension",
"Community & Regional Planning",
"Community and Regional Planning",
"Computer Engineering",
"Computer Science",
"Conference Planning & Management",
"Construction Engineering",
"Controller's Department",
"Coop Ext Fld Ce",
"Cooperative Extension Field Program",
"County Paid Extension Staff",
"Criminal Justice Studies",
"Ctr for Industrial Research & Service",
"Ctr for Nondestructive Evaluation",
"Ctr for Survey Stat/Methodology",
"Ctr Stat & Applctn in Forensic Evidence",
"Culinary Food Science - Agriculture",
"Culinary Food Science - Human Sciences",
"Curriculum and Instruction",
"Dairy Science",
"Dean of Students Office",
"Design",
"Design Administration",
"Design Specials (Non-Degree)",
"Design Undeclared",
"Destination Iowa State-New Student Prgms",
"Diet and Exercise (H SCI)",
"Dietetics (AGLS)",
"Dietetics (H SCI)",
"Division of Finance",
"Early Childcare Education and Programming",
"Early Childhood Education",
"Earth Science",
"Ecology and Evolutionary Biology",
"Ecology, Evolution & Organismal Biol-LAS",
"Ecology, Evolution and Organismal Biology",
"Ecology, Evolution and Organismal Biology (AGLS)",
"Ecology, Evolution and Organismal Biology (LAS)",
"Ecology/Evolution & Organismal Biol-AGLS",
"Economic Dvlpmnt & Industry Relations",
"Economics",
"Economics (AGLS)",
"Economics (LAS)",
"Economics - LAS",
"Economics-AGLS",
"Education",
"Educational Leadership and Policy Studies",
"Educational Talent Search",
"Elec Eng/Cp Eng",
"Electrical and Computer Engineering",
"Electrical Engineering",
"Elementary Education",
"Engineering",
"Engineering Administration",
"Engineering Career Services",
"Engineering College Relations",
"Engineering Management",
"Engineering Outreach Programs",
"Engineering Research Institute",
"Engineering Specials (Non-Degree)",
"Engineering Student Services",
"Engineering Technology Support",
"Engineering-Las Online Learning",
"English",
"Entomology",
"Entrepreneurship",
"Environmental Health & Safety",
"Environmental Science",
"Environmental Science (AGLS)",
"Environmental Science (LAS)",
"Equal Opportunity Office",
"Event Management",
"Extension Distribution",
"Extension IT",
"Extension Organizational Advancement",
"Extension Organizational Development",
"Extension Professional Development",
"Extension To Agriculture-Extension",
"Facilities Planning and Management",
"Faculty Senate",
"Family and Consumer Science Education and Studies ",
"Family and Consumer Sciences",
"Family Finance, Housing and Policy",
"Finance",
"Finance Extension",
"Financial Counseling and Planning",
"Fire Srvc Training Bureau",
"Flight Services",
"Food Science & Human Nutrition - AGLS",
"Food Science & Human Nutrition-H Sci",
"Food Science (AGLS)",
"Food Science (H SCI)",
"Food Science and Human Nutrition (AGLS)",
"Food Science and Human Nutrition (H SCI)",
"Forestry",
"General Preveterinary Medicine",
"Genetics (AGLS)",
"Genetics (LAS)",
"Genetics and Genomics",
"Genetics Development and Cell Biology (AGLS)",
"Genetics Development and Cell Biology (LAS)",
"Genetics, Development & Cell Biology-LAS",
"Genetics/Development & Cell Biology-AGLS",
"Geological and Atmospheric Sciences",
"Geology",
"Gerontology",
"Global Agriculture Programs",
"Global Resource Systems",
"Government Relations",
"Graduate College",
"Grants Hub",
"Graphic Design",
"Greenlee School Journalism/Communication",
"History",
"Honors Program-Prv",
"Horticulture",
"Hospitality Management",
"Hotel Restaurant & Institution Mgmt",
"Human Computer Interaction",
"Human Development & Family Studies",
"Human Development and Family Studies",
"Human Resources Extension",
"Human Sciences",
"Human Sciences Administration",
"Human Sciences Extension and Outreach",
"Human Sciences International Programs",
"Human Sciences Special (Non-Degree)",
"Human Sciences Student Services",
"Immunobiology",
"Industrial & Manufacturing Systems Engr",
"Industrial and Manufacturing Systems",
"Industrial and Manufacturing Systems Engineering",
"Industrial Design",
"Industrial Engineering",
"Industrial Technology",
"Information Assurance",
"Institute for Design Research & Outreach",
"Institute for Social/Behavioral Research",
"Institute for Transportation",
"Institutional Research",
"Integrated Studio Arts",
"Intensive English & Orientation Program",
"Intensive English and Orientation Program LAS",
"Interdepartmental Graduate Programs",
"Interdisciplinary Design",
"Interdisciplinary Graduate Studies",
"Interdisciplinary Studies",
"Interior Design",
"Internal Audit",
"International Students & Scholars",
"Iowa Braille & Sight Saving School",
"Iowa Nutrient Research Center",
"Iowa Public Radio",
"Iowa School for the Deaf",
"Iowa Soybean Research Center",
"Iowa State Center",
"Iowa State Daily",
"Iowa State Research Farms",
"Iowa State Research Foundation",
"Iowa State Univ Research Park",
"ISU Foundation",
"ISU Pappajohn Ctr for Entrepreneurship",
"IT Services Academic Technologies",
"IT Services Administrative Services",
"IT Services Customer Services",
"IT Services Networks & Communications",
"IT Services Office of CIO",
"IT Services Security and Policies",
"IT Services Systems & Operations",
"IT Services University Info Systems",
"Journalism & Mass Communication",
"Journalism and Mass Communication",
"Kinesiology",
"Kinesiology and Health",
"Laboratory Animal Resources",
"Landscape Architecture",
"Lectures Program",
"Leopold Center",
"Liberal Arts & Sci Student Academic Srv",
"Liberal Arts & Sciences Administration",
"Liberal Arts & Sciences Cross Discpl St",
"Liberal Arts and Sciences Certificate (Non-Degree)",
"Liberal Arts and Sciences Specials (Non-Degree)",
"Liberal Studies",
"Library",
"Linguistics",
"Logistics & Support Services",
"LSCM",
"Management",
"Management Information Systems",
"Marketing",
"Materials Engineering",
"Materials Science & Engineering",
"Materials Science and Engineering",
"Mathematics",
"Mechanical Engineering",
"Memorial Union",
"Meteorology",
"Microbiology",
"Microelectronics Research Ctr",
"Midwest Plan Service",
"Military Science & Tactics",
"Molecular Cellular & Developmental Biol",
"Multicultural Student Affairs",
"Music",
"Music and Theatre",
"Nanovaccine Institute",
"National Lab for Ag and the Environment",
"Natural Resource Ecology and Management",
"Naval Science",
"Neurosciences",
"Nutrition & Wellness Research Center",
"Nutritional Science (AGLS)",
"Nutritional Science (H SCI)",
"Nutritional Sciences",
"Ofc Intellectual Property & Tech Transfr",
"Office for Responsible Research",
"Office of Research Integrity",
"Ombuds Office",
"Open Option (LAS)",
"Orientation - New Student Programs",
"Parking",
"Performing Arts",
"Philosophy",
"Philosophy & Religious Studies",
"Physics",
"Physics & Astronomy",
"Physics and Astronomy",
"PL P",
"Plant Biology",
"Plant Pathology",
"Plant Pathology and Microbiology",
"Plant Sciences Institute",
"Political Science",
"PR ST",
"Pre-Advertising",
"Pre-Architecture",
"Pre-Athletic Training",
"Pre-Biological/Pre-Medical Illustration",
"Pre-Business",
"Pre-Community and Regional Planning",
"Pre-Diet and Exercise (AGLS)",
"Pre-Diet and Exercise (H SCI)",
"Pre-Dietetics (AGLS)",
"Pre-Dietetics (H SCI)",
"Pre-Graphic Design",
"Pre-Industrial Design",
"Pre-Integrated Studio Arts",
"Pre-Interior Design",
"Pre-Landscape Architecture",
"Pre-Liberal Studies",
"Preparation For Human Medicine",
"Preparation For Law",
"Preprofessional Health Programs",
"President",
"Printing and Copy Services",
"Procurement Services",
"Professional Agriculture",
"Prog for Women in Science & Engr",
"Psychology",
"Public Relations",
"Public Safety",
"Public Service and Administration in Agriculture",
"Receivables Office",
"Records & Registration",
"Recreation Services",
"Reiman Gardens",
"Religious Studies",
"Residence Halls",
"Risk Management",
"School of Education",
"Seed Science Center - Experiment Station",
"Seed Technology and Business",
"Senior Vice President & Provost",
"Small Business Development Center",
"Sociology",
"Sociology (AGLS)",
"Sociology (LAS)",
"Sociology - AGLS",
"Sociology - LAS",
"Software Engineering",
"Spanish",
"Speech Communication",
"Sponsored Programs Administration",
"Sr Vice Pres for University Services",
"Statistics",
"Supply Chain & Information Systems",
"Supply Chain and Information Systems",
"Supply Chain Management",
"Sustainable Agriculture",
"Systems Engineering",
"Technical Communication",
"Toxicology",
"Undeclared Distance Education",
"Upward Bound",
"Urban Design",
"USDA - Space",
"Value Added Agriculture-Extension",
"Veenker Memorial Golf Course",
"Vet Diagnostic & Production Animal Med",
"Vet Microbiology & Preventive Medicine",
"Veterinary Clinical Science",
"Veterinary Clinical Sciences",
"Veterinary Diag & Prod Animal Med",
"Veterinary Diagnostic Laboratory",
"Veterinary Medicine",
"Veterinary Medicine Nebraska Alliance",
"Veterinary Medicine Specials (Non-Degree)",
"Veterinary Microbiology & Prev Med",
"Veterinary Pathology",
"Water Resources Research Institute",
"Wind Energy Science, Engineering and Policy",
"Women's Center - Student Affairs",
"Women's Studies",
"World Languages and Cultures",
"Zoology & Genetics - Ag"]

EMAIL_FROM_HREF = True

container_tag   = None # Can be None to not sort by tag
container_attrs = { "class_" : "dir-Listing"}

faculty_tag     = None # Can be None to not sort by tag
faculty_attrs   = { "class_" : "dir-Listing-item"}

name_tag        = "h1" # Can be None to not sort by tag
name_attrs      = { }

email_tag       = None # Can be None to not sort by tag
email_attrs     = { "text" : mailto_pat}

position_tag    = None # Can be None to not sort by tag
position_attrs  = { "text" : "Title:"}

dept_tag        = None # Can be None to not sort by tag
dept_attrs      = { "text" : "Dept:"}

output_file = "ist.csv"

for index,department in enumerate(DEPARTMENTS):
        directory_page.append((department,index,))

with Pool() as pool:
    result = pool.starmap(readDept, directory_page)

    with open(output_file, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for process in result:
            for row in process:
                writer.writerow(row)
