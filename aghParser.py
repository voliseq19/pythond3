import urllib.request
import urllib.parse
import re
import io, json

class weather(object):
    def __init__(self):
        self.dates = []
        self.temps = []
        self.wind = []

    def find_dates(self, data):
        self.dates = re.findall(r'\d{2}\:\d{2}\s[^,]+,\s\d{2}\.\d{2}\.\d{4}', str(data))

    def find_temps(self,data):
        self.temps = re.findall(r'-?\d\s&deg', str(data))

    def find_wind(self,data):
        self.wind = re.findall(r'\d{1,2}\skm/h', str(data))
        self.wind = self.wind[0::2]
    def print_info(self):
        for i in range(len(self.dates)-1):
            print(" Date: " + self.dates[i] + "  temp: " + self.temps[i] + "  Wind: " + self.wind[i])

def getHTML(url):
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    respdata = resp.read()
    return respdata


respd = getHTML("http://www.twojapogoda.pl/polska/malopolskie/skawina/godzinowa")
w = weather()
w.find_dates(respd)
w.find_temps(respd)
print(w.temps)
w.find_wind(respd)
w.temps = w.temps[3:]
w.dates = [date.replace('<small>', '') for date in w.dates]
w.print_info()

temps = []
winds = []
numberDict = {}
dataJSON = []
def  getNumbers(data):
    newData = []
    for item in data:
        if item[1] == " ":
         item = item[0:1]
        else:
            item = item[0:2]
        newData.append(item)
    return newData


temps = getNumbers(w.temps)
winds = getNumbers(w.wind)

for i in range(len(temps)):
    numberDict[i] = {}
    numberDict[i]["temps"] = temps[i]
    numberDict[i]["wind"] = winds[i]
    dataJSON.append(numberDict[i])

with open('d3Data.json', 'wt') as outfile:
    json.dump(dataJSON, outfile, ensure_ascii=False)



print(temps)
print(winds)
print(w.wind)
print(dataJSON)



