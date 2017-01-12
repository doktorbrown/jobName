'''
Created on Jan 12, 2017

@author: tbrown
'''
import os
import re
import time
from datetime import date
import csv
from bs4 import BeautifulSoup #installation at http://www.crummy.com/software/BeautifulSoup/     $ pip install beautifulsoup4


#update with full list, abbreviations, and lower case expanded campus list
campusList = ['ABINGTON', 'ALTOONA','BEAVER', 'BEHREND', 'BERKS','BRANDYWINE', 'CARLISLE', 'DICKINSON','DUBOIS', 'ERIE', 'FAYETTE', 'GREAT', 'GREAT VALLEY', 'GREATER', 'GREATER ALLEGHENY', 'HARRISBURG', 'HAZELTON', 'HERSHEY', 'LEHIGH', 'LEHIGH VALLEY', 'MONT', 'MONT ALTO', 'NEW', 'NEW KENSINGTON', 'SCHUYLKILL', 'SHENANGO', 'SCRANTON', 'WILKES-BARRE', 'WILLIAMSPORT','WORTHINGTON', 'WORTHINGTON SCRANTON', 'YORK']
campus = str()

fname = "MakerBot Innovation Center.html"
soup = BeautifulSoup(open(fname), 'html.parser') 
out = "clipboard.txt"
log = "log.txt"
csvLogOutput = "3D_label_Logs.csv"

#print soup.prettify()

nameGetter = soup.find_all(text = re.compile("^Requestor"))[0].next
emailGetter = soup.find_all(text = re.compile("^Requestor Email"))[0].next.next.next_element
campusGetter = soup.find_all(text = re.compile("^Requestor Notes"))[0].next
fileNameGetter = soup.find_all(text = re.compile("^File Name"))[0].next
requestGetter = soup.find_all(text = re.compile("^Request:"))[0].next
printerGetter = soup.find_all(text = re.compile("^Printer:"))[0].next.next.next_element

#exception handling for uncompleted prints or variations in html
try:
    filamentGetter = soup.find_all(text = re.compile("Filament Usage Actual"))[0].next
except:
    filamentGetterEstimate = soup.find_all(text = re.compile("Filament Usage Estimate"))[0].next
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
print "printerGetter: ",printerGetter
# print "requestGetter: ", requestGetter
# print "fileNameGetter: ", fileNameGetter

#keep additional options out for now in case html is from rest page instead of jobs. once location parsing or printer name is added 
try:
    print filamentGetter
except:
    print filamentGetterEstimate
    filamentGetter = filamentGetterEstimate

#print notesGetter
#print " "#space the final frontier

campusGetterUpper = campusGetter.upper()
#fix that unicode crap
cc = campusGetterUpper.encode('utf-8')
# print "cc = ", cc

campusGetterSplitter = cc.upper()
campusGetterSplitter = cc.split()

# print "CampusGetterSplitter = ", campusGetterSplitter

campusListSize=len(campusList)
# print "campus list size",campusListSize
campusGetterSplitterSize=len(campusGetterSplitter)
#print campusGetterSplitterSize

for num in range(campusListSize):
    a= campusList[num]
    for num2 in range(campusGetterSplitterSize):
        b = campusGetterSplitter[num2]
        if a in b:
            campus = b.upper()
#             print campus    
            
        else:
#             print "no match"
            
            continue
        
#campus exception checking 
# print "campus", campus
      
if campus == "ERIE":
    campus ="BEHREND"
if campus == "GREAT":
    campus ="GREAT VALLEY"
if campus == "GREATER":
    campus = "GREATER ALLEGHENY"
if campus == "GREATER":
    campus = "GREATER ALLEGHENY"
if campus == "LEHIGH":
    campus = "LEHIGH VALLEY"
if campus == "MONT":
    campus = "MONT ALTO"
if campus == "NEW":
    campus = "NEW KENSINGTON"
if campus == "SCRANTON":
    campus = "WORTHINGTON SCRANTON"
if campus == "WORTHINGTON":
    campus = "WORTHINGTON SCRANTON"
if campus == "SCHUYKILL":
    campus ="SCHUYLKILL"    
    
        

print campus
print lastName,",", firstName
print today
print emailGetter, filamentGetter,fileNameGetter,

#open output file for writing results
f = open(out, 'w')
    
#format extracted text for label
#lineOne = (nameGetter,'\n', emailGetter, '\n', "\n Failing to add a Raft or \n Supports when preparing the \n .makerbot file is the most \n common reason for a failed print. \n Please check: \n makercommons.psu.edu/fail \n for more info.  Consultations \n can be scheduled by emailing  \n makercommons@psu.edu.")
#for landscape print
# lineOne = (campus, '\n',lastName,",", firstName,'\n', today, " ", emailGetter, " ", filamentGetter, " ",fileNameGetter," ", requestGetter,'\n', '\n', "Not adding a Raft or Supports when   prepping the .makerbot file is the   most common reason for failed prints. \n Info: makercommons.psu.edu/fail \n Consultation Scheduling: \n makercommons@psu.edu")
#shorter msg re: rafts to adjust formatting and fit on one label
lineOne = (campus, '\n',lastName,",", firstName,'\n', today, " ", emailGetter, " ", filamentGetter, " ",fileNameGetter," ", requestGetter,'\n',  "Consultation Scheduling: \n makercommons@psu.edu")

#strip extra mc label info so it doesn't clutter log
lineTwo = (today,",",campus,",",lastName,"," ,firstName,",",emailGetter,",",printerGetter,",",filamentGetter," ",fileNameGetter, " ", requestGetter,'\n','\n')


f.writelines(lineOne)
print lineOne

f.close()

os.system("lpr -o landscape -P DYMO_LabelWriter_450_Turbo clipboard.txt")

#open log file for appending results
logs = open(log, 'a')
logs.writelines(lineTwo)
# print "log appended"
# print lineTwo
logs.close()

#logsCommaSeparated.
row_to_enter = (today, campus, lastName, firstName, emailGetter, printerGetter,filamentGetter, requestGetter, fileNameGetter, '\n')
csvLogs = csv.writer(open(csvLogOutput, 'a'))
csvLogs.writerow(row_to_enter)
print "log appended"
print lineTwo
