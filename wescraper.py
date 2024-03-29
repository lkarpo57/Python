import requests
import re
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
import os
import warnings
warnings.filterwarnings('ignore')

val = os.getcwd()
val= val.replace("\.spyder-py3","")
city = 'Philqdlephia-pa/' #*****change this city to what you want!!!!*****

#just grabbing the first 20 pages
#feel free to make this prettier
url1 = 'https://www.zillow.com/homes/for_sale/'+city
url2 = 'https://www.zillow.com/homes/for_sale/'+city+'/2_p/'
url3 = 'https://www.zillow.com/homes/for_sale/'+city+'/3_p/'
url4 = 'https://www.zillow.com/homes/for_sale/'+city+'/4_p/'
url5 = 'https://www.zillow.com/homes/for_sale/'+city+'/5_p/'
url6 = 'https://www.zillow.com/homes/for_sale/'+city+'/6_p/'
url7 = 'https://www.zillow.com/homes/for_sale/'+city+'/7_p/'
url8 = 'https://www.zillow.com/homes/for_sale/'+city+'/8_p/'
url9 = 'https://www.zillow.com/homes/for_sale/'+city+'/9_p/'
url10 = 'https://www.zillow.com/homes/for_sale/'+city+'/10_p/'
url11 = 'https://www.zillow.com/homes/for_sale/'+city+'/11_p/'
url12 = 'https://www.zillow.com/homes/for_sale/'+city+'/12_p/'
url13 = 'https://www.zillow.com/homes/for_sale/'+city+'/13_p/'
url14 = 'https://www.zillow.com/homes/for_sale/'+city+'/14_p/'
url15 = 'https://www.zillow.com/homes/for_sale/'+city+'/15_p/'
url16 = 'https://www.zillow.com/homes/for_sale/'+city+'/16_p/'
url17 = 'https://www.zillow.com/homes/for_sale/'+city+'/17_p/'
url18 = 'https://www.zillow.com/homes/for_sale/'+city+'/18_p/'
url19 = 'https://www.zillow.com/homes/for_sale/'+city+'/19_p/'
url20 = 'https://www.zillow.com/homes/for_sale/'+city+'/20_p/'

#add headers in case you use chromedriver (captchas are no fun); namely used for chromedriver
req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

with requests.Session() as s:
    r1 = s.get(url1, headers=req_headers)
    r2 = s.get(url2, headers=req_headers)
    r3 = s.get(url3, headers=req_headers)
    r4 = s.get(url4, headers=req_headers)
    r5 = s.get(url5, headers=req_headers)
    r6 = s.get(url6, headers=req_headers)
    r7 = s.get(url7, headers=req_headers)
    r8 = s.get(url8, headers=req_headers)
    r9 = s.get(url9, headers=req_headers)
    r10 = s.get(url10, headers=req_headers)
    r11 = s.get(url11, headers=req_headers)
    r12 = s.get(url12, headers=req_headers)
    r13 = s.get(url13, headers=req_headers)
    r14 = s.get(url14, headers=req_headers)
    r15 = s.get(url15, headers=req_headers)
    r16 = s.get(url16, headers=req_headers)
    r17 = s.get(url17, headers=req_headers)
    r18 = s.get(url18, headers=req_headers)
    r19 = s.get(url19, headers=req_headers)
    r20 = s.get(url20, headers=req_headers)
    
    data1 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r1.text).group(1))
    data2 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r2.text).group(1))
    data3 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r3.text).group(1))
    data4 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r4.text).group(1))
    data5 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r5.text).group(1))
    data6 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r6.text).group(1))
    data7 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r7.text).group(1))
    data8 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r8.text).group(1))
    data9 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r9.text).group(1))
    data10 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r10.text).group(1))
    data11 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r11.text).group(1))
    data12 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r12.text).group(1))
    data13 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r13.text).group(1))
    data14 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r14.text).group(1))
    data15 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r15.text).group(1))
    data16 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r16.text).group(1))
    data17 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r17.text).group(1))
    data18 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r18.text).group(1))
    data19 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r19.text).group(1))
    data20 = json.loads(re.search(r'!--(\{"queryState".*?)-->', r20.text).group(1))
    
data_list = [data1,data2,data3,data4,data5,data6,data7,data8,data9,data10
             ,data11,data12,data13,data14,data15,data16,data17,data18,data19,data20]

df = pd.DataFrame()

def make_frame(frame):
    for i in data_list:
        for item in i['cat1']['searchResults']['listResults']:
            frame = frame.append(item, ignore_index=True)
    return frame

df = make_frame(df)
df['beds']=df['beds'].astype('float')
df['baths']=df['baths'].astype('float')
df=df.replace(np.nan,0)
#drop cols
df = df.drop('hdpData', 1) #remove this line to see a whole bunch of other random cols, in dict format

#drop dupes
df = df.drop_duplicates(subset='zpid', keep="last")

df=df.loc[:,['id', 'detailUrl','statusType', 'statusText','unformattedPrice', 'addressStreet', 'addressCity',
'addressState', 'addressZipcode','beds','baths', 'area']]

#status pie_status 
plt1=df.loc[:,['id','statusText']]
plt1=plt1.groupby(['statusText']).count()
plt1=plt1.reset_index()
fig=plt.figure(figsize=(10,7))
plt.pie(plt1['id'], labels=plt1['statusText'])
plt.show()

#table
tble=df.loc[:, ['statusText','beds','baths','unformattedPrice']]
tble=tble.rename(columns={'statusText':'Status', 'unformattedPrice':'Price'})
tble=tble.groupby(['Status']).mean()
tble['Price']=tble['Price'].astype('int')
tble['beds']=tble['beds'].astype('int')
tble['baths']=tble['baths'].astype('int')
tble=tble.round(0)
print(tble)
#heatmap
plt2=df.loc[:, ['statusText', 'beds','baths','unformattedPrice']]
plt2['unformattedPrice']=plt2['unformattedPrice'].astype('int')
x = df['beds']
z = df['baths']
y = df['unformattedPrice']
fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')
ax.scatter(x, z, y)

## Save
##path=val+"//Downloads"
df.to_csv('C:/Users/leest/Downloads/phl.csv')

