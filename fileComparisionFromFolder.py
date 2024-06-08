#Compare two or more files line by line in python.
import os
import glob
import pandas as pd
import configparser
import datetime
from datetime import datetime, date
import csv
import shutil
import gzip
from ordinal import ordinal
import smtplib, socket
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.message import EmailMessage
from email.utils import make_msgid

# Read config file
print("reading config parser")
config = configparser.ConfigParser()
config.read('configUniteFile.properties')

# Get current directory
dirPath = os.path.dirname(__file__)
today = date.today()
fileDate = today.strftime("%d%m%Y")  # 22012024
conversionDate: str = fileDate  # date format is 22012024
fileOutputDate = today.strftime("%Y%m%d")  # 20240122

# Read a source path
print("load the config file")
inputexcelFile = config.get("files", "inputexcelFile")
firstValidationFile = config.get("files", "firstValidationFile")
secondValidationFile = config.get("files", "secondValidationFile")
thirdValidationFile = config.get("files", "thirdValidationFile")
outputCombinedFile = config.get("files", "outputCombinedFile")
combinedFile = config.get("files", "combinedFile")

# read the filepath
# get current file from path
inputFirstSecondFilePath = inputexcelFile  # get folder ./unite/
firstFileSearchPattern = inputFirstSecondFilePath + 'FIRST_Status' + conversionDate + '.csv'
secondFileSearchPattern = inputFirstSecondFilePath + 'SECOND_Status' + conversionDate + '.csv'
thirdFileSearchPattern = inputFirstSecondFilePath + 'THIRD_Status' + conversionDate + '.csv'
outputCombinedFileWithDate = outputCombinedFile + 'FIRSTSECONDTHIRD_Status' + fileOutputDate + '.csv'
combinedFileWithDate = combinedFile + 'FIRSTSECONDTHIRD_Status' + fileOutputDate + '.csv'
getcombinedGZFileWithDate = combinedFileWithDate + '.gz'

# Read server file path
firstsecondCurrentFilePath = today.strftime("%d-%m-Y")  # get startTime i.e 22-Jan-2024

# Create an empty array for appended data
secondServerFileContentArray = []
thirdServerFileContentArray = []
finalContentArray = []

# creating a named list
secondIdList = {}
thirdIdList = {}

# list all the files from the billing directory
secondcsvReader = csv.reader(open(secondFileSearchPattern, 'r'))
next(secondcsvReader, None)
# Iterate each row data from file
for secondserverItem in secondcsvReader:
    # print(secondserverItem)     #['750\t', '\t1234585758585485\t', ]
    firstServerFileContentArray.append(firstserverItem)
    firstData = firstserverItem[0]
    secondId = secondData.strip()
    secondList[secondId] = secondItem
# print("named List", secondList)  # {'1234585758585485': ['750\t', '\t1234585758585485\t', ]}

# list all the files from the bss directory
thirdcsvReader = csv.reader(open(thirdFileSearchPattern, 'r'))
next(thirdcsvReader, None)
# Iterate each row data from file
for thirdserverItem in thirdcsvReader:
    # print(thirdserverItem)     #['750\t', '\t1234585758585485\t', ]
    thirdServerFileContentArray.append(thirdserverItem)
    thirdData = thirdserverItem[0]
    thirdId = thirdData.strip()
    thirdIdList[thirdId] = thirdserverItem
# print("named List", thirdIdList)  # {'1234585758585485': ['750\t', '\t1234585758585485\t', ]}

# list all the files from the aircontrol directory
firstcsvReader = csv.reader(open(firstFileSearchPattern, 'r'))
next(firstcsvReader, None)
i = 0
# Iterate each row data from file
for firstItem in firstcsvReader:
    # print(firstItem)     #['750\t', '\t1234585758585485\t', ]
    firstIdData = firstItem[0]
    firstIdValue = firstIdData.strip()
    secondSearchedItem = []
    thirdSearchedItem = []
    uniqueIDMatch = ',,,,,,,,,,No'
    firstsdnMatch = 'No'
    firstIdMatch = 'No'
    secondFileDate = 'No'
    firstStatusMatch = 'No'
    uniqueStatusMatch = 'No'

    thirduniqueIDMatch = ',,,,,,,,,,No'
    thirdfirstsdnMatch = 'No'
    thirdfirstIdMatch = 'No'
    thirdsecondFileDateMatch = 'No'

    try:
        # check unique id exist from a second file server list
        secondSearchedItem = secondIdList[firstIdValue]
        # print("Matched Unique NO", firstIdValue)
        uniqueIDMatch = 'Yes'

        # check unique id exist from a third file server list
        thirdSearchedItem = thirdIdList[firstIdValue]
        # print("Matched Unique No", airControlIdValue)
        thirduniqueIDMatch = 'Yes'

        firstsdnValue = firstItem[1]
        secondsdnValue = secondSearchedItem[1]
        # print(firstsdnValue, secondsdnValue)
        if firstsdnValue == secondsdnValue:
            firstsdnMatch = 'Yes'

        firstsdnValue = firstItem[1]
        thirdsdnValue = thirdSearchedItem[1]
        # print(firstsdnValue, thirdsdnValue)
        if firstsdnValue == thirdsdnValue:
            thirdfirstsdnMatch = 'Yes'

        firstIdValue = firstItem[2]
        secondIdValue = secondSearchedItem[2]
        # print("firstIdValue", "secondIdValue")
        if firstIdValue == secondIdValue:
            firstIdMatch = 'Yes'

        firstIdValue = firstItem[2]
        thirdIdValue = thirdSearchedItem[2]
        # print("firstIdValue", "thirdIdValue")
        if firstIdValue == thirdIdValue:
            thirdIdMatch = 'Yes'

        firstFileDateValue = firstItem[3]
        secondFileDateValue = secondSearchedItem[3]
        # print(firstFileDateValue, secondFileDateValue)
        if firstFileDateValue == secondFileDateValue:
            secondFileDate = 'Yes'

        firstFileDateValue = firstItem[3]
        thirdFileDateValue = thirdSearchedItem[3]
        # print(firstFileDateValue, thirdFileDateValue)
        if firstFileDateValue == thirdFileDateValue:
            thirdFileDateMatch = 'Yes'

        firtStatusValue = firstItem[6]
        firstStatusValue = firstStatusValue.strip()
        secondStatusValue = secondSearchedItem[6]
        secondStatusValue = secondStatusValue.strip()
        # print(firtStatusValue, secondStatusValue)
        if firstStatusValue == 'Active' and secondStatusValue == 'Active':
            firstStatusMatch = 'Yes'
        else:
            firstStatusMatch = 'No'

        firstStateValue = firstItem[11]
        firstStateValue = firstStateValue.strip()
        secondStateValue = secondSearchedItem[10]
        secondStateValue = secondStateValue.strip()
        # print(firstStateValue, secondStateValue)
        if firstStatusValue == 'ACTIVATED' and secondStatusValue == 'Activated':
            uniqueStatusMatch = 'Yes'
        else:
            uniqueStatusMatch = 'No'

    except KeyError:
        print("Second file uniqueID not found in first file uniqueID list for", firstIdValue)

    # Check value exists in a first array
    firstFileItemString = ""
    secondFileItemString = ""
    thirdFileItemString = ""
    firstFileItemList = firstItem
    # print("firstFileItemString", firstFileItemString)  # ['12\t', '\tMy Sample data\t',] i.e firstfile data
    counterFirstFile = 0
    for columnData in firstFileItemList:
        if counterFirstFile == 0:
            firstFileItemString = columnData.strip()
        else:
            firstFileItemString = firstFileItemString + "," + columnData.strip()
        counterFirstFile = counterFirstFile + 1
    # print(firstFileItemString)

    # check not empty for secondSearchedItem
    if secondSearchedItem:
        counterSecondFile = 0
        for secondcolumnData in secondSearchedItem:
            if counterSecondFile == 0:
                secondFileItemString = secondcolumnData.strip()
            else:
                secondFileItemString = secondFileItemString + "," + secondcolumnData.strip()
            counterSecondFile = counterSecondFile + 1
        # print(secondFileItemString)

    # check not empty for thirdSearchedItem
    if thirdSearchedItem:
        counterThirdFile = 0
        for thirdcolumnData in secondSearchedItem:
            if counterThirdFile == 0:
                thirdFileItemString = thirdcolumnData.strip()
            else:
                thirdFileItemString = thirdFileItemString + "," + thirdcolumnData.strip()
            counterThirdFile = counterThirdFile + 1
        # print(thirdFileItemString)

    mergeitemString = firstFileItemString + "," + secondFileItemString + "," + uniqueIDMatch + "," + firstsdnMatch + "," + firstIdMatch + "," + secondFileDate + "," + firstStatusMatch + "," + uniqueStatusMatch + "," + thirdFileItemString + "," + thirduniqueIDMatch + "," + thirdfirstsdnMatch + "," + thirdfirstIdMatch + "," + thirdsecondFileDateMatch
    # print("merged >>>>>>>>")
    # print("mergeitemString", mergeitemString)
    finalContentArray.append([mergeitemString.strip()])
    i = i + 1

print("final>>>>>>>>>>")
# print(finalContentArray)
# endloop
print(finalContentArray)
# field names
headerCols = "FIRST_UNIQUE, FIRST_SDN, FIRST_AccountID, First_FILEDATE, FIRST_Status, UniqueStatusMatch, THIRD_UNIQUE_ID, THIRD_FIRST_SDN, THIRD_AC_ID, THIRD_FILEDATE, ThirduniqueIDMatch, ThirdfirstsdnMatch, ThirdFirstIdMatch, ThirdsecondFileDateMatch,"
fields = [headerCols]
with open(combinedFileWithDate, 'w', newline="") as csvfile:
    # create a csv writer object
    writer = csv.writer(csvfile, delimiter="\t")
    writer.writerow(fields)
    for row in finalContentArray:  # generator
        # print(row)
        writer.writerow(row)
# Close the file
csvfile.close()

# ---------- Create gz file ----------
# open the csv file read mode
with open(combinedFileWithDate, 'rb') as f:
    # Read the contents of the file
    data = f.read()

# compress the data
compressed_data = gzip.compress(data)

# Open the gzipped file in writing mode
fileSearchPattern = combinedFileWithDate
allFirstSecondThirdStatusFiles = glob.glob(fileSearchPattern)  # ['./unite/FIRSTSECONDTHIRD_Unique_Status_20240402.csv']
# print("Fetched all FIRSTSECONDTHIRD_Unique_Status matching files from downloaded folder")
for eachFirstSecondThirdStatusFile in allFirstSecondThirdStatusFiles:
    with open(eachFirstSecondThirdStatusFile + '.gz', 'wb') as f:
        f.write(compressed_data)
# ---------- end gz file compress code -----------

# ----------------------------
#   Configure mail
# ----------------------------
# Read config file
print("reading config parser of smtp mail server")
smtpServer = config.get("email", "smtpServer")
emailFROM = config.get("email", "emailFROM")
emailTo = config.get("email", "emailTo")
emailLogo = config.get("email", "emailLogo")

# setup port number and server name
smtp_server = smtpServer
emailFrom = emailFROM
emailTo = emailTo.split(",")
subject = 'FIRSTSECONDTHIRD Unique Status'

# Textual month, day and year
print("The date used as per format for mail")
currentFolder = firstsecondCurrentFilePath
fileName = 'FIRSTSECONDTHIRD_Unique_Status' + fileOutputDate + '.csv'
mdate = today.strftime("%d")
tdate = int(mdate)
fromdateOrdinal = ordinal(int(mdate))
dateFormatForMail = datetime.strptime(str(today), '%Y-%m-%d')  # Get today - 1 day i.e, 2023-12-21 00:00:00
print(dateFormatForMail)
fromdateFormat = datetime.strptime(str(dateFormatForMail), '%Y-%m-%d %H:%M:%S').strftime(f"{fromdateOrdinal} %B %Y")


def send_emails(emailTo):
    # make a MIME Object to define parts of the email
    msg = EmailMessage()
    msg['from'] = emailFrom
    msg['to'] = ", ".join(emailTo)
    msg['subject'] = subject

    # update code for email signature--------
    img_path = emailLogo  # Path to img you are appending to the end of the email
    image_id = make_msgid()

    msg.add_alternative("""\
    <html>
        <head></head>
        <body>
            <p>Dear All, </p>
            <p>Please find the file at path mentioned below: </p>
            <p>Path: C:/PythonScript/allFile""" + """/""" + str(currentFolder) + """/""" + str(fileName) + """</p>
            <p>FileName: """ + str(fileName) + """</p>
            <table border="0" cellspacing="3" cellpadding="0" width="0">
                <tbody>
                    <tr>
                        <td width="112" style="width:84.0pt; padding: .75pt .75pt .75pt .75pt;">
                            <u></u>
                                <img width="102" height="71" src="cid:{image_id}">
                            <u></u>
                        </td>
                        <td>
                            <span></span>
                            <span></span>
                        </td>
                        <td width="272" style="width:204.0pt;border:none;border-left:solid #1486ed 1.5 pt;padding:.75pt .75pt .75pt .75pt">
                            <span style="font-size:9.5pt;font-family:&quot;sans-serif;color:#404040;margin-left:5px;"></span>
                            <span style="font-size:9.5pt;font-family:&quot;sans-serif;color:#404040;margin-left:5px;"></span>
                            <span style="font-size:9.5pt;font-family:&quot;sans-serif;color:#404040;margin-left:5px;"></span>
                            <span style="font-size:9.5pt;font-family:&quot;sans-serif;color:#404040;margin-left:5px;"></span>
                        </td>
                    </tr>
                </tbody>
            </table><br>
            <div style="background-color: yellow; display: inline-block;">Note: This is an automatically generated email by automationScript</div>
            </body>
    </html>
    """.format(image_id=image_id[1:-1]), subtype='html')
    # Note that we needed to peel <> off the msg-id for use in the html
    # Now add the related image to the html part.
    with open(img_path, 'rb') as img:
        msg.get_payload()[0].add_related(img.read(), 'image', 'png', cid=image_id)
    # end email signature template----------

    # Cast as string
    try:
        text = msg.as_string()
        print("connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server)
        print("Successfully connected to server :-) ")
        print()
        # send emails to "allEmail" as a list is iterated
        print(f"Sending email To - {emailTo}")
        print(f"Sending email Cc - {emailCc}")
        TIE_server.sendmail(emailFrom, (emailTo + emailCc), text)
        print(f"Email sent To - {emailTo}")
        print(f"Email sent To - {emailCc}")
        print()
        TIE_server.quit()
    except socket.error as errmsg:
        print(errmsg, "Could not connect to server")


send_emails(emailTo)
# end mail function >>>>>
