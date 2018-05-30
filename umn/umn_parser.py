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
import itertools

BAD_POSITIONS = {"Admin","admin","Worker","Researcher","RA","Spec","Temporary","Doctoral","Suppmental","Cook","Practical","Attendant","Intern","Developer","Info Tech Mgmt 3",
"Assistant Child Care Teacher",
"Painter",
"System Engineer",
"Animal Care Manager 2",
"Camp Ops/Protect Prof 3 Sup",
"Data Analyst",
"Student Affairs Manager",
"Senior Energy Engineer",
"Pharmacy Associate",
"Academic Advisor",
"Finance Professional 3 Supv",
"External Service Provider",
"Business/Systems Analyst 3",
"Alumni Rel/Adv Op Ofc No Entry",
"Research Coordinator",
"Monarch Joint Venture Science",
"Education and Operations Mgr",
"Student Services Manager 2",
"Assistant Scientist",
"Printing Scheduler",
"Materials Mgmt Assistant",
"Assistant Vice President",
"Sch Building",
"Pipefitter",
"Senior Laboratory Technician",
"Psychotherapist",
"Dental Assistant",
"Summer Term TA (w/o Tuit Ben)",
"CETI Program Manager",
"Assessment Tech: N Carolina",
"Facilities Team Manager",
"Psych Clinic Rsrch Trainer",
"Non-Univ Temp/Casual Employee",
"Security Program Manager",
"Gift Officer 5b",
"Asst AD, Communications",
"Museum Preparator",
"COSP Graduate Assistant",
"Off-Cmps Study Prog Coordinatr",
"Developer",
"Mechanic 2",
"Grants/Cntrcts Prof 3",
"Finance Professional 2 Supv",
"Fullbright Scholar (affiliated)",
"Dtr, Editorial and Design Svcs",
"Junior Cashier/Food Aide",
"Visiting Scholar (affiliated)",
"Assoc AD, Health",
"Visiting PhD Student (affiliated)",
"Digital Content Strategist",
"Research Professional 2",
"Non Exempt Cas/ Cmty Prog",
"Allied Health Care Prof2 Supv",
"Pharmacy Technician",
"Purchasing Professional 3",
"Sr Veterinary Technician - ER",
"Human Resources Generalist 1",
"End User Support",
"Admissions Associate",
"Development Assistant",
"Workforce Planning",
"Allied Health Care Prof 2",
"Finance Analyst 3",
"Allied Health Care Prof3 Supv",
"AgroInform Resrcher/Data Sci",
"Asst Dir Leases",
"Comm Rel/Otrch Assoc 3 No Ent",
"Grants/Cntrcts Prof 3 No Entry",
"Access Consultant",
"Interpreter - Somali",
"Intern",
"Procurement",
"Grant Writing",
"Research Quality Analyst",
"Massage Therapist",
"Research Nurse 4 No New Entry",
"Associate Development Officer",
"CETI Process Manager",
"Professional Program Assistant",
"IMED Medical Resident",
"Career Counselor",
"Endow Prof Targeted Delivery",
"Senior Veterinary Technician",
"Nursing Assistant",
"Assistant Vice Provost",
"Donor Rel and Stewardship",
"Business/Systems Analyst 2",
"Construction Laborer",
"Education Program Manager 2",
"Student Services Prof 2",
"Dental Incentive Plan",
"Admissions Counselor",
"Non-University Employee (affiliated)",
"Mental Health Care Provider 2",
"BioNet Research Technician",
"Research Professional 4 No NE",
"Associate Academic Advisor",
"Tutor Coordinator",
"Infrastructure Analyst",
"Radiographic Tech- Temp",
"Education Program Associate 2",
"Lab Services Coordinator",
"Student Academic Support",
"Clinical Trials Assistant",
"Scientist",
"Human Resources Consultant 1",
"Info Tech Mgmt 1 No Entry",
"Mechanic 3",
"Sr Compensation Analyst",
"Coordinator",
"BHH Program Manager",
"Graduate Program Coordinator",
"Graduate Assistant Coach",
"Graphic/Multimedia Designer",
"Veterinary Technician",
"Finance Manager 2",
"Research Assoc No New Entry (affiliated)",
"Finance Professional 2",
"University Regent",
"Animal Care Provider 3",
"Manager",
"Casual Assistant",
"Medical Resident",
"IRB Analyst",
"Musician - Dance",
"End User Support 1",
"Assistant To",
"Developer 2 (affiliated)",
"Office Support Assistant",
"Plumber",
"Research Professional 4",
"Marketing Assistant",
"Research Support Manager 1",
"Non-Exempt Casual Facilitator",
"Research Professional 3",
"Senior Auditor",
"Steam/Chld Water Utilities Sup",
"Senior Academic Advisor",
"Business/Systems Analyst",
"0001 GH Res Asst",
"Data Architect",
"Camp Ops/Protect Prof 2",
"Finance Manager 1 No Entry",
"Natl Media Relations Consultan",
"Teaching Assistant",
"Sign Language Interpreter",
"Prin Graphic/Multimedia Des (affiliated)",
"Animal Diagnostic Prof 2",
"Developer 2",
"Library/Museum Manager 1",
"Pub/Int Rel Comm Sr Consultant",
"One Stop Counselor 4",
"Finance Analyst 2",
"Triage Nurse",
"Seasonal Custodial Assistants",
"Allied Health Care Provider 2",
"Finance Professional 3",
"Info Tech Mgmt 2",
"Instructional Services Librari",
"Prin Envrn Health/Safety Tech",
"Golf Course Grounds Crew",
"Dentist (affiliated)",
"Video Production Assistant",
"Community Program Assistant",
"PhD Candidate Research Asst",
"Intercollegiate Athl Equp Wrkr",
"Academic Technologist 2",
"Postgraduate Pharmacy Resident (affiliated)",
"Alumni Rel/Adv Ops Officer",
"Finance Professional 1",
"Curator",
"Financial Analyst",
"Service Learning Coordinator",
"OAP Operations/Processes Mgr",
"Human Resources Generalist 2",
"Pub/Int Rel Comm Consultant",
"Senior Cashier/Food Aide",
"Research Professional 3 Supv",
"Library Associate 2",
"Junior Scientist",
"Executive in Residence (affiliated)",
"Project Coordinator",
"Graduate School Trainee",
"Research Support Mgr 2",
"Chi Summer Intern",
"Copy Center Equipment Operator",
"Student Services Manager 3",
"Admissions Associate/Reader",
"Mechanical Engineer 1",
"Assessment Tech: Kentucky",
"Student Services Prof 3",
"Extension Program Associate 2",
"Developer 3 No Entry",
"Human Resources Generalist 3",
"Visiting Research Asst Prof (affiliated)",
"Animal Diagnostic Prof 3",
"Developer 1",
"One Stop Counselor 3",
"CORE Intern (affiliated)",
"Animal Diagnostic Prof 1",
"Finance Professional 4 Supv",
"Veterinary Medical Resident",
"Communications Associate",
"Executive Assistant",
"Summer Sess TA (w/o Tuit Ben)",
"Medical Assistant",
"Research Professional 1",
"OTC Royalty Accountant",
"Camp Ops/Protect Mgr 2",
"Graphic/Multimedia Comm Assoc",
"Mental Health Care Provider 1",
"Research Professional 4 No Ent",
"Student Services Prof 1",
"Laborer",
"Lead Accountant",
"Police Officer",
"Clinical Services Coordinator",
"Student Services Manager 1",
"Developer 3",
"PhD Candidate Teaching Asst",
"Database Technician",
"QA and Committee Assistant",
"Student Personnel Coordinator",
"Asst Prof - Will be hired 7/27 (affiliated)",
"Ext Prog Assoc 3 - No Entry",
"IATSE stage hands",
"Coordinator, AI Recruitment",
"Data Modeler / Architect",
"Technology Support Analyst",
"Ugrad Rsrch Asst(Non-Univ Stu)",
"Nursing Professional",
"Junior Laboratory Technician",
"Research Manager 2 No Entry",
"Principal Auditor",
"Research Manager 3",
"Grants/Cntrcts Prof 2",
"Camp Ops/Protect Prof 2 Sup",
"Student Finance Counselor 2",
"Principal Editor/Writer",
"Captioner",
"Summer Term AF (w/o Tuit Ben)",
"Camp Ops/Prot Mgr 2 No Entry",
"DBA Program Manager",
"Animal Care Professional 2",
"Senior Career Counselor",
"Library Assistant 2",
"Principal Engineer",
"Prin Ofc",
"Medical Student Tutor",
"Assistant Librarian",
"Animal Care Manager 3",
"IMED Chief Resident",
"Pennycress Research Manager",
"Patient Cr Provider1 No Entry",
"Librarian",
"Severance",
"End User Support 2",
"Manager, Enterprise Systems",
"Business/Systems Analyst 1",
"Concrete Finisher",
"Mental Health Care Prof 2",
"Affiliate",
"Athletics Operations Manager 3",
"Research Assistant",
"Assistant Coach",
"CURE Intern",
"Research Associate (affiliated)",
"Patient Care Professional 2",
"Legal Proj Asst (w/o Tuit Ben)",
"Athletic Trainer",
"Environmental Hlth",
"Art Museum Preparator",
"Clinical Research Coordinator",
"Student Tech Support Services",
"Grad School Committee Member (affiliated)",
"Business Development Mgr 1",
"BioStats Graduate (affiliated)",
"Admissions Interviewer",
"Library Assistant 3",
"Admissions Operations Coord",
"International Counselor (affiliated)",
"Pre K-12 Manager 2 - No Entry",
"Ops/Prot Prof Supv 4 No Entry",
"Finance Professional 4",
"Audio/Visual Media Producer",
"LPA-McGeveran",
"Sr Associate General Counsel",
"Camp Ops/Protect Prof 1",
"Communications Supv No Entry",
"Research Support Manager 3",
"Graduate Subject Tutor",
"Research Intern",
"Systems Analyst",
"Finance Supervisor 3",
"Mechanic 1",
"Senior Attorney-Sanderson"}

def processEmail(email):
    parts = re.findall("\'([\w\.]*)\'",email)
    email = "@".join(parts[0:2])
    return email

def readPage(query):
    current_page = 0
    last_page = -1
    retval = []
    directory_page = ("https://myaccount.umn.edu/lookup?SET_INSTITUTION=&campus=t&role=sta&type=name&CN={}".format(query))

    for attempt in range(0,5):
        try:
            supersoup  = BeautifulSoup(urlopen(directory_page),"html.parser")
        except:
            print("{} failed to open {}/5, retrying...".format(query,attempt,))
            pass
        else:
            break
    else:
        raise Exception("Failed 5 times")

    links = supersoup(href=re.compile("/lookup"))

    for idx, link in enumerate(links):

        for attempt in range(0,5):
            try:
                page = urlopen("https://myaccount.umn.edu"+link['href'])

                # parse the html using beautiful soup and store in variable 'soup'
                soup = BeautifulSoup(page, 'html.parser')
            except:
                print("{} failed to open {}/5, retrying...".format(query,attempt,))
                pass
            else:
                break
        else:
            raise Exception("Failed 5 times")

        #dept = soup.find(class_="organization-unit").text
        name = soup.find("h2").text

        blurb = soup.find("th").next.next.contents

        try:
            position = blurb[0]
            position = cleanPosition(position)
            if any([bad in position for bad in BAD_POSITIONS]):
                continue
        except:
            print("\rPosition not found for {}".format(name))
            continue
            position = ""
        try:
            dept = blurb[2]
            dept = cleanDepartment(dept)
        except:
            print("\rDepartment not found for {}".format(name))
            continue
            dept = ""
        try:
            email = soup.find(href=mailto_pat).text
        except:
            print("\rEmail not found for {}".format(name))
            continue
            email = ""

        print("\r{}/{}".format(idx,len(links)), flush=True, end="")

        retval.append([name,email,position,dept])


    print("\r{}/{} {}".format(len(links),len(links),query), flush=True)

    return retval

pages          = []
directory_page = []
processes      = []


EMAIL_FROM_HREF = True

container_tag   = None # Can be None to not sort by tag
container_attrs = { "class_" : "dir-Listing"}

faculty_tag     = None # Can be None to not sort by tag
faculty_attrs   = { "class_" : "dir-Listing-item"}

name_tag        = "h2" # Can be None to not sort by tag
name_attrs      = { }

email_tag       = None # Can be None to not sort by tag
email_attrs     = { "text" : mailto_pat}

position_tag    = None # Can be None to not sort by tag
position_attrs  = { "text" : "Title:"}

dept_tag        = None # Can be None to not sort by tag
dept_attrs      = { "text" : "Dept:"}

output_file = "umn.csv"

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

CHUNK_SIZE  = 26
START_INDEX = 0

queries = [ "".join(tup) for tup in itertools.product(ALPHABET,repeat=2) ]

for i in range(0,26):
    try:
        with Pool() as pool:
            result = pool.map(readPage, queries[i*CHUNK_SIZE:(i+1)*CHUNK_SIZE])

            with open(ALPHABET[i] + "." + output_file, 'a+', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for process in result:
                    for row in process:
                        writer.writerow(row)
    except Exception as e:
        print(e)
        print("Error was caught on iteration {}/{}".format(i,25))
