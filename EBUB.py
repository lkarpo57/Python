# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 13:29:56 2023

@author: lkarpo
"""

import pandas as pd
from datetime import date
import os

os.chdir('//p00cifs0369.corp.tmnas.com/DataWarehousing/TMA_DWH/DEV/ACTUARIAL/Processing')
val = os.getcwd()
dir_list = os.listdir(val)
dir_list= [string for string in dir_list if string.endswith("xls")]    
file ="/"+ dir_list[0]
file=str(val)+file
sourceGA=pd.read_excel(file,sheet_name='GrossAdjustments',header=0)
sourceGA['CededIndicator']="N"
sourceGA=sourceGA.rename(columns={'GrossPremiumAdjustment':'PremiumAdjustment'})
sourceCA=pd.read_excel(file,sheet_name='CededAdjustments',header=0)
sourceCA['CededIndicator']="Y"
sourceCA=sourceCA.rename(columns={'CededPremiumAdjustment':'PremiumAdjustment'})
targetdf = pd.concat([sourceGA, sourceCA])
year=str(targetdf['AccountingPeriodDate'].dt.year.max())
month=str(targetdf['AccountingPeriodDate'].dt.month.max())
targetdf['AccountingPeriodDate']=targetdf['AccountingPeriodDate'].dt.strftime("%m/%d/%Y")    
targetdf.set_index('AccountingPeriodDate', inplace=True)
Ofile=str(val)+"\XLS_Exposure_Adjustments_"+month+year+".csv"
targetdf.to_csv(Ofile)