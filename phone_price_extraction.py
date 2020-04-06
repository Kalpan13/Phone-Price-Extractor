# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm
import json
df = pd.read_csv('DeviceNames.csv')
smartprixUrl = "https://www.smartprix.com/products/?q="    #Url to for Findig the Phone Price
df['price'] = ""

phones = {}
phone_list = list(df['device_name'])

for i,phone in enumerate(phone_list):
    phone_name = str(phone)
    
    if not phone_name.isdecimal():
        if phone_name not in list(phones.keys()):
            phone = phone_name.replace(' ','+')
            phone = phone.replace('(','%28')
            phone = phone.replace(')','%29')
            phone = phone.replace('/','%2F')
            phone = phone.replace('\'','%27')
            req_url = smartprixUrl+phone
            r= requests.get(req_url)
            data=r.text
            soup=BeautifulSoup(data,features ='html.parser')
            listings = soup.find_all('span', attrs={'class': 'price'})
            price=str(listings[0].find(text=True, recursive=False))
            price = price.replace('₹','')
            price = price.replace(',','')
            
            if price.isdigit():
              df['price'][i] = int(price)
              phones[phone_name] = int(price)    #For Stroing in Json Format
            else :
              df['price'][i] = -1
    else:
      df['price'][i] = -1   # Device Name is Wrong 
            

df.to_csv('DeviceNames.csv')
'''
In Case you want to store the prices in Json
Json Format : 
{
    'Device_Name' : Price
}
'''
with open('PhonePrices.json', 'w') as f:
    json.dump(phones, f)
with open('PhonePrices.json') as f:
  data = json.load(f)


