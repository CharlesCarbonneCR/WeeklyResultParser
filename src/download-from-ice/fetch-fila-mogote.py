import json, os, math, statistics
from datetime import date, datetime, timedelta
from operator import attrgetter

from dotenv import load_dotenv

load_dotenv()

PRICE_SESONA_ALTA_FDM = os.getenv('PRICE_SESONA_ALTA_FDM')
PRICE_SESONA_BAJA_FDM = os.getenv('PRICE_SESONA_BAJA_FDM')

###Def calculate price of mwh:
def calculateTotalUsd(date, mwh):
    if(date.month >= 1 and date.month <=5):
        priceKW = PRICE_SESONA_ALTA_FDM
    if(date.month >= 6 and date.month <=12):
        priceKW = PRICE_SESONA_BAJA_FDM
    total_usd = mwh * (float(priceKW)*1000)
    return total_usd
    

class Plant():
    def __init__(self, fecha, dato, fuente, planta, grupo):
        self.fechaStr = fecha
        if type(fecha) is str:
            self.fecha = datetime.strptime(fecha[:-2], '%Y-%m-%d %H:%M:%S')
        if type(fecha) is datetime:
            self.fecha = fecha
        self.dato = dato
        self.fuente = fuente
        self.planta = planta
        self.grupo = grupo
        self.fechaStr = fecha

plantList = []

jsonFolderPath = '../json'
jsonFolderPath = jsonPath = os.path.join(os.path.dirname(__file__), jsonFolderPath)

#### Get files from json folder:
for x in os.listdir(jsonFolderPath):
    if x.endswith(".json"):
        # Prints only text file present in My Folder
        print(x)
        jsonPath = '../json/'+x
        jsonPath = os.path.join(os.path.dirname(__file__), jsonPath)
        print(jsonPath)
        with open(jsonPath) as f:
            d = json.load(f)
            data = d['data']
            for i in data:
                if "Mogote" in i['planta']:
                    plant = Plant(**i)
                    plantList.append(plant)


###Sort the list by date:
sorted_list_by_date = sorted(plantList, key=attrgetter('fecha'))

for data in sorted_list_by_date:
    dataObject = Plant(data.fecha, data.dato, data.fuente, data.planta, data.grupo)
    # print('fecha=',dataObject.fecha)
    # print('dato en MWh=',dataObject.dato)
    # print('fuente=',dataObject.fuente)
    # print('planta=',dataObject.planta)
    # print('grupo=',dataObject.grupo)

###Buildup total per day:
#Get todays date:
today = date.today()
#Get start of month date
startMonth = today.replace(day=1)
print("start month = ", startMonth)
print("Today's date:", today)
#set processingDate
processingDate = startMonth
datoTotal = float()
total_usd = float()
average_usd = float()
daysTotal = 0
while (processingDate <= today and processingDate.month == today.month and processingDate.day < (today.day -1) and processingDate.year == today.year):
    print("###############")
    print("processingDate =", processingDate)
    dayString = str(processingDate.day)
    dayStringWithLeadingZero = str(processingDate.strftime("%d"))
    monthString = str(processingDate.month)
    monthStringWithLeadingZero = str(processingDate.strftime("%m"))
    yearString = str(processingDate.year)
    dataByDate = []
    datoTotalByDate = []
    for data in sorted_list_by_date:
        if (data.fecha.day == processingDate.day 
            and data.fecha.month == processingDate.month 
            and data.fecha.year == processingDate.year):
            dataByDate.append(data)
            datoTotalByDate.append(data.dato)
    # get number of elements in datoTotalByDateFloat should be 24:
    print("total elements (should be 24) :", len(datoTotalByDate))
    datoTotalByDateFloat = math.fsum(datoTotalByDate)
    print("dato total for date "+dayString+"/"+monthString+"/"+yearString+": "+str(datoTotalByDateFloat))
    total_usd_by_date = calculateTotalUsd(processingDate, datoTotalByDateFloat)
    print("Total USD = for date "+dayString+"/"+monthString+"/"+yearString+": "+str(total_usd_by_date))
    tmpList = []
    tmpList.append(datoTotalByDateFloat)
    tmpList.append(datoTotal)
    datoTotal = math.fsum(tmpList)
    tmpListUSD = []
    tmpListUSD.append(total_usd_by_date)
    tmpListUSD.append(total_usd)
    total_usd = math.fsum(tmpListUSD)
    print("total MW produced on month "+monthString+" :", datoTotal)
    print("total usd produced on month "+monthString+" :", total_usd)
    # add a day then loop
    daysTotal = daysTotal+1
    processingDate = processingDate + timedelta(days=1)

 ###DIsplay totals
average_usd = total_usd / float(daysTotal)
print("#### TOTALS :")
print("TOTAL MWh produced :", datoTotal)
print("TOTAL USD : ",total_usd)
print("AVERAGE USD :", average_usd)
print("NUMBER OF DAYS IN THE CALCULATION :", daysTotal)
proj = float(average_usd) * float(processingDate.max.day)
print("Projection for the month based on the average and "+str(processingDate.max.day)+" days", proj)