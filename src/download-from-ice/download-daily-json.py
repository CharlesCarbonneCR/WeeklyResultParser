#### download from json from website of ICE
#### example url :
#### https://apps.grupoice.com/CenceWeb/data/sen/json/EnergiaHorariaFuentePlanta?anno=2024&mes=1&dia=16

import urllib.request, json 
from datetime import date, datetime, timedelta
import os

#Get todays date:
today = date.today()
#Get start of month date
startMonth = today.replace(day=1)
print("start month = ", startMonth)
print("Today's date:", today)
#set processingDate
processingDate = startMonth

#Loop for each day untill today
while processingDate <= today:
    print("###############")
    print("processingDate =", processingDate)
    dayString = str(processingDate.day)
    dayStringWithLeadingZero = str(processingDate.strftime("%d"))
    monthString = str(processingDate.month)
    monthStringWithLeadingZero = str(processingDate.strftime("%m"))
    yearString = str(processingDate.year)
    #determine url
    urlToProcess = "https://apps.grupoice.com/CenceWeb/data/sen/json/EnergiaHorariaFuentePlanta?anno="+yearString+"&mes="+monthString+"&dia="+dayString
    print("url =", urlToProcess)
    #determine fileName
    fileName = monthStringWithLeadingZero+"-"+dayStringWithLeadingZero+"-"+yearString+".json"
    print("fileName =", fileName)
    #determine filePath
    jsonPath = '../json/'+fileName
    jsonPath = os.path.join(os.path.dirname(__file__), jsonPath)
    print("filePath =",jsonPath)
    print("Downloading json from ",urlToProcess)
    with urllib.request.urlopen(urlToProcess) as url:
        data = json.load(url)
    #Write data to file
    print("Writing json to file ", jsonPath)
    jsonFile = open(jsonPath, "w")
    jsonString = json.dumps(data)
    jsonFile.write(jsonString)
    jsonFile.close()
    # add a day then loop
    processingDate = processingDate + timedelta(days=1)



##TODO if file already exist check date, if date superior to date in filename +1 then don't download
