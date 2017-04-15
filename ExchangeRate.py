import urllib3
from bs4 import BeautifulSoup
from utils import delay
http = urllib3.PoolManager()



id_dollar = "R01235"
id_evro = "R01239"
def updateRates():
    r = http.request('GET', 'http://www.cbr.ru/scripts/XML_daily.asp?date_req')
    soup = BeautifulSoup(r.data, "lxml")
    dollar,euro = '',''
    for link in soup.find_all('valute'):
        try:
            valute_id = link['id']
            if (valute_id == id_dollar):
                dollar = link.find('value').text
            if (valute_id == id_evro):
                euro = link.find('value').text

        except:
            continue
    return dollar,euro
@delay(100)
def f():
    dollar, euro = updateRates()
    f()

dollar,euro = updateRates()
f()