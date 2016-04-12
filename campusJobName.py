'''
Created on Apr 11, 2016

@author: tbrown
'''
import os
import re
import time
from datetime import date
from bs4 import BeautifulSoup #installation at http://www.crummy.com/software/BeautifulSoup/     $ pip install beautifulsoup4


#update with full list, abbreviations, and lower case
campusList = ['ABINGTON', 'ALTOONA','BEAVER', 'BEHREND', 'BERKS','BRANDYWINE', 'CARLISLE', 'DUBOIS', 'FAYETTE', 'GREAT VALLEY', 'GREATER ALLEGHENY', 'HARRISBURG', 'HAZELTON', 'HERSHEY', 'LEHIGH VALLEY', 'MONT ALTO', 'NEW KENSINGTON', 'SCHUYKILL', 'SHENANGO', 'UNIVERSITY PARK', 'WILKES-BARRE', 'WILLIAMSPORT','WORTHINGTON SCRANTON', 'YORK']
campus = str()

fname = "MakerBot Innovation Center.html"
soup = BeautifulSoup(open(fname), 'html.parser') 
out = "clipboard.txt"

#print soup.prettify()

nameGetter = soup.find_all(text = re.compile("^Requestor"))[0].next
emailGetter = soup.find_all(text = re.compile("^Requestor Email"))[0].next.next.next_element
campusGetter = soup.find_all(text = re.compile("^Requestor Notes"))[0].next
#printerGetter = soup.find_all(text = re.compile("^Printer"))[0].next
#filamentGetter = soup.find_all(text = re.compile("Filament Usage Actual"))[0].next
#notesGetter = soup.find_all(text = re.compile("^Campus"))#not yet implemented in form
today =str(date.today())
#split the name string and then figure out size to determine last position since 1 is not always last name...
nameSplitter = nameGetter.split()
#print nameSplitter[0]
lastNamePlace= len(nameSplitter)
lastName = nameSplitter[lastNamePlace-1]
firstName = nameSplitter[0]

#print lastName,",", firstName


#print emailGetter
#print printerGetter
#keep additional options out for now in case html is from rest page instead of jobs. once location parsing or printer name is added 
#print filamentGetter
#print notesGetter
#print " "#space the final frontier

campusGetterUpper = campusGetter.upper()
#fix that unicode crap
cc = campusGetterUpper.encode('utf-8')
#print cc

campusGetterSplitter = cc.upper()
campusGetterSplitter = cc.split()

campusListSize=len(campusList)
#print campusListSize
campusGetterSplitterSize=len(campusGetterSplitter)
#print campusGetterSplitterSize

for num in range(campusListSize):
    a= campusList[num]
    for num2 in range(campusGetterSplitterSize):
        b = campusGetterSplitter[num2]
        if a in b:
            campus = b.upper()
            #print campus
        else:
            #print "no match"
            
            continue
        

print campus
print lastName,",", firstName
print today
print emailGetter

#open output file for writing results
f = open(out, 'w')
    
#format extracted text for label
#lineOne = (nameGetter,'\n', emailGetter, '\n', "\n Failing to add a Raft or \n Supports when preparing the \n .makerbot file is the most \n common reason for a failed print. \n Please check: \n makercommons.psu.edu/fail \n for more info.  Consultations \n can be scheduled by emailing  \n makercommons@psu.edu.")
#for landscape print
lineOne = (campus, '\n',lastName,",", firstName,'\n', today, " ", emailGetter, '\n', '\n', "Not adding a Raft or Supports when   prepping the .makerbot file is the   most common reason for failed prints. \n Info: makercommons.psu.edu/fail \n Consultation Scheduling: \n makercommons@psu.edu")


f.writelines(lineOne)
print lineOne

f.close()

os.system("lpr -o landscape -P DYMO_LabelWriter_450_Turbo clipboard.txt")
