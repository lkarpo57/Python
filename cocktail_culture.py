
from woocommerce import API
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, time
import json
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
import pygwalker as pyg
        
wcapi = API(
    url="https://cocktailculture.co/",
    consumer_key="xxxxxx",
    consumer_secret="xxxxxxxx",
    version="wc/v1",
    timeout=30
)

response=wcapi.get("orders", params={"per_page": 100})
pages_count = int(response.headers['X-WP-TotalPages'])
r=response.json()

current_page = 1
all_page_items_json = []
while current_page <= pages_count:
    page_items=wcapi.get("orders", params={"per_page": 100, "page":current_page})
    page_items_json = page_items.json()
    all_page_items_json.extend(page_items_json)
    current_page = current_page + 1


df = pd.json_normalize(all_page_items_json)
df=pd.DataFrame.from_dict(all_page_items_json, orient='columns')   
paymentdf=df[df['status']=="completed"]
paymentjson=json.loads(json.dumps(list(paymentdf.T.to_dict().values())))                                                                                                     
payment=pd.json_normalize(paymentjson, record_path =['line_items'])
bookingsdf=df[df['status']=="completed"]
bookingjson=json.loads(json.dumps(list(bookingsdf.T.to_dict().values())))
bookings_scr = pd.json_normalize(bookingjson, record_path=['line_items', 'meta'], record_prefix='x_'
,errors='ignore')
bookings_scr['id'] =  np.where(bookings_scr['x_key']=='Booking ID', bookings_scr['x_value'], 
                               np.where(bookings_scr['x_key']!='Booking ID', '', ''))
bookings_scr['id']=bookings_scr['id'].replace('',np.nan)
bookings_scr['id']=bookings_scr['id'].bfill(axis =0, limit=4)
bookings_scr=bookings_scr.dropna(subset=['id'])
bookings_scr = bookings_scr.drop(columns=['x_key'])
bookings_dates=bookings_scr[bookings_scr['x_label'] == "Booking Date"]
bookings_dates=bookings_dates.rename(columns = {"x_value":"Booking Date"})
bookings_dates = bookings_dates.drop(columns=['x_label'])
bookings_time=bookings_scr[bookings_scr['x_label'] == "Booking Time"]
bookings_time=bookings_time.drop('x_label', axis=1, inplace=False) 
bookings_time=bookings_time.rename(columns = {"x_value":"Booking Time"})
bookings_count=bookings_scr[bookings_scr['x_label'] == "Persons"]
bookings_count=bookings_count.rename(columns = {"x_value":"Persons"})
bookings_count = bookings_count.drop(columns=['x_label'])
bookings_count = bookings_count[['id','Persons']].drop_duplicates() 
bookings_type=bookings_scr[bookings_scr['x_label'] == "Booking Type"]
bookings_type=bookings_type.rename(columns = {"x_value":"Classes"})
bookings_type = bookings_type.drop(columns=['x_label'])
bookings_type = bookings_type[['id','Classes']].drop_duplicates()
booking_id = bookings_scr[['id']].drop_duplicates()
bookingsdf = pd.merge(booking_id, bookings_dates, how='inner', on='id')
bookingsdf = pd.merge(bookingsdf, bookings_time, how='inner', on='id')
bookingsdf = pd.merge(bookingsdf, bookings_type, how='inner', on='id')
bookingsdf = pd.merge(bookingsdf, bookings_count, how='inner', on='id') 
bookingsdf['Booking Date']=bookingsdf['Booking Date'].astype('datetime64[ns]')
bookingsdf = bookingsdf[bookingsdf['Booking Date']>(datetime.now()-timedelta(days=1))]
Booking_Cal=bookingsdf
Booking_Cal['Duration'] ="2 hours"
Booking_Cal['Booking Date']=Booking_Cal['Booking Date'].astype('datetime64[ns]')
Booking_Cal=Booking_Cal[Booking_Cal['Booking Date']>=(datetime.now()-timedelta(days=1))]
Booking_Cal = Booking_Cal.drop(columns=['id'])
Booking_Cal['Booking Date']=Booking_Cal['Booking Date'].dt.strftime("%m/%d/%Y")
Booking_Cal['Persons']=Booking_Cal['Persons'].astype('int')
Booking_Cal=Booking_Cal.groupby(['Booking Date', 'Booking Time','Classes', 'Duration'])['Persons'].sum()
Booking_Cal=Booking_Cal.reset_index()
Booking_Cal=Booking_Cal.rename(columns={'Booking Date':'Start Date', 'Booking Time':'Start Time', 'Classes':'Subject'})
Booking_Cal['End Date']=Booking_Cal['Start Date']
Booking_Cal['Duration']=Booking_Cal['Duration'].astype(str)
Booking_Cal['Duration'] = (Booking_Cal['Duration'].str.replace(",",""))
Booking_Cal['Duration'] = (Booking_Cal['Duration'].replace(['hours?', 'hour', 'minutes'], ['*60+','*60+', ''], regex=True)
                           .str.strip('+')
                           .apply(pd.eval))
Booking_Cal['End Time']=Booking_Cal['Start Time']
Booking_Cal['End Time']=Booking_Cal['End Time'].astype(str)
Booking_Cal['End Time'] = (Booking_Cal['End Time'].str.replace("pm",""))
Booking_Cal['End Time']=Booking_Cal['End Time'].astype('datetime64[ns]')
Booking_Cal['End Time']=Booking_Cal['End Time'] + pd.TimedeltaIndex( Booking_Cal['Duration'], unit='m')
Booking_Cal['End Time']=Booking_Cal['End Time'].astype(str)
Booking_Cal['End Time'] = (Booking_Cal['End Time'].str[11:])
Booking_Cal['End Time'] = (Booking_Cal['End Time'].str[:-3])
Booking_Cal['End Time'] = Booking_Cal['End Time'].astype(str)+' pm'
Booking_Cal['All Day Event']="False"
Booking_Cal['Description']=Booking_Cal['Persons']
Booking_Cal['Location']=""
Booking_Cal=Booking_Cal.loc[:,['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 'All Day Event', 'Description', 'Location']]
Booking_Cal=Booking_Cal.set_index('Subject')
Booking_Cal.to_csv('C:/Users/leest/Downloads/cccal.csv')
Booking_Cal['Start Date']=Booking_Cal['Start Date'].astype('datetime64[ns]')
weekahead=Booking_Cal[Booking_Cal['Start Date']<=(datetime.now()+timedelta(days=7))]
weekahead['Start Date']=weekahead['Start Date'].dt.strftime("%m/%d/%Y")
weekahead=weekahead.drop(['End Date', 'All Day Event', 'Start Time', 'Location'],axis=1, inplace=False)
print(tabulate(weekahead, headers = 'keys', tablefmt = 'psql'))

dfpayplot=df[df['status']=="completed"]
dfpayplot=dfpayplot.loc[:,['status', 'date_paid', 'total']]
dfpayplot=dfpayplot[dfpayplot['date_paid']!=""]
dfpayplot['date_paid']=dfpayplot['date_paid'].astype('datetime64[ns]')
dfpayplot=dfpayplot[dfpayplot['status']=="completed"]
dfpayplot=dfpayplot.loc[:,['date_paid', 'total']]
dfpayplot=dfpayplot.sort_values(by='date_paid')
dfpayplot['year'] = pd.DatetimeIndex(dfpayplot['date_paid']).year
dfpayplot['month'] = pd.DatetimeIndex(dfpayplot['date_paid']).month
dfpayplot['total']=dfpayplot['total'].astype(float)
dfpayplot=dfpayplot[dfpayplot['date_paid']>="2020-01-01"]
revplotdf= pd.pivot_table(dfpayplot, index=dfpayplot.month, columns=dfpayplot.year,
                    values='total', aggfunc=sum)
revplotdf=revplotdf.reset_index()
revplotdf[2023]=revplotdf[2023].ffill(limit=1)
plt.figure(figsize=(14,6))
sns.lineplot(data=revplotdf[2020], label="2020")
sns.lineplot(data=revplotdf[2021], label="2021")
sns.lineplot(data=revplotdf[2022], label="2022")
sns.lineplot(data=revplotdf[2023], label="2023")
plt.show()

classmix=bookingsdf.loc[:,['Booking Date', 'Classes','Persons']]
classmix['Persons']=classmix['Persons'].astype(float)
classmix['year'] = pd.DatetimeIndex(classmix['Booking Date']).year
classmix = classmix.drop(columns=['Booking Date'])
labels=['Bachelorette Party Themed Cocktails','Intro to Bourbon & Rye: Public Class','Intro to Scotch: Public Class','Your Phone Drinks First: Public Class',
        'Chocolate & Espresso Cocktails: Public Class','Prohibition Era Cocktails: Public Class','Fresh Fruit Cocktails: Public Class','Herbs & Spices in Mixology: Public Class']
color={"Pink","Black","Grey","Blue","Brown","Yellow","Green","Orange"}



classmix2023=classmix[classmix['year']==2023]
classmix2022=classmix[classmix['year']==2022]
classmix2023g=classmix2023.groupby(['Classes'])['Persons'].sum()
classmix2022g=classmix2022.groupby(['Classes'])['Persons'].sum()
fig, axs = plt.subplots(nrows=1, ncols=2)
classmix2023g.groupby(['Classes']).sum().plot(kind='pie', y='Persons',  label="", labels=labels, colors=color, ax=axs[0])
plt.legend(["Chocolate & Espresso Cocktails: Public Class", "Fresh Fruit Cocktails: Public Class", "Herbs & Spices in Mixology: Public Class",
           "Prohibition Era Cocktails: Public Class", "Your Phone Drinks First: Public Class"], loc="upper center", fontsize="5")
classmix2022g.groupby(['Classes']).sum().plot(kind='pie', y='Persons', label="",colors=color, ax=axs[1])
plt.xlabel("2022")
plt.legend(["Chocolate & Espresso Cocktails: Public Class", "Fresh Fruit Cocktails: Public Class", "Herbs & Spices in Mixology: Public Class",
           "Prohibition Era Cocktails: Public Class", "Your Phone Drinks First: Public Class"], loc='lower center', bbox_to_anchor=(-.5, -0.25)
, fontsize="7")
plt.show()
