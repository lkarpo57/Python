# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 19:47:51 2022
 
@author: lkarpo
"""
 
import pandas as pd
import numpy as np
from datetime import date
import os
import re 

os.chdir('//p00cifs0369.corp.tmnas.com/DataWarehousing/TMA_DWH/TMA_OriginalSourceFiles/Processing')
val = os.getcwd()
dir_list = os.listdir(val)
dir_list= [string for string in dir_list if string.endswith("xlsx")]    
file ="/"+ dir_list[0]
file=str(val)+file
source=pd.read_excel(file,sheet_name=None,header=None)
dictKeys = list(source.keys())
result = [word for word in dictKeys if len(word) <=4]
source=pd.read_excel(file,sheet_name=result,header=None)
df = pd.concat(source, ignore_index=True)
As_of=df.loc[3][0]
As_of=As_of.replace('As of ','')
As_of=As_of.replace('2008 Policy Year as of ','')
df['PolicyYear']=df[1]    
cols = list(df.columns)
cols = [cols[-1]] + cols[:-1]
df = df[cols]

df['PolicyYear']=df['PolicyYear'].astype('str')    
m = df["PolicyYear"].str.contains("|".join(result))
df.loc[~m, "PolicyYear"] = np.nan
df['PolicyYear']=df['PolicyYear'].astype('str')    
df['PolicyYear']=df['PolicyYear'].replace(to_replace=r'TD', value=np.nan, regex=True)
df['PolicyYear']=df['PolicyYear'].replace('nan', value=np.nan)
df['PolicyYear']=np.where(df[0]=='POLICY YEAR',df[1],np.nan)


df['DatePeriod']=df[1]    
cols = list(df.columns)
cols = [cols[-1]] + cols[:-1]
df = df[cols]
m = df["DatePeriod"].str.contains("|".join(result))
df['DatePeriod']=df['DatePeriod'].astype('str')    
df['DatePeriod'] = df['DatePeriod'].replace(to_replace=r"^(.(?<!TD))*?$", value=' ',regex=True)
df['PreiodDate']=df['DatePeriod']
df['DatePeriod']=np.nan 
cols = list(df.columns)
cols = [cols[-1]] + cols[:-1]
df = df[cols]
df[['PreiodDate', 'DatePeriod']] = df['PreiodDate'].str.rsplit(' ', 1, expand=True)
df['index'] = np.nan
df.loc[df[1] == "Written Premium", 'index'] = 1
df.loc[df[1] == "Paid Loss", 'index'] = 2
cols = list(df.columns)
cols = [cols[-1]] + cols[:-1]
df = df[cols]
df['PreiodDate']=df['PreiodDate'].replace('', value=np.nan)
df['DatePeriod']=df['DatePeriod'].replace('', value=np.nan)
df = df.dropna(how='all')
df['index'] = df['index'].ffill(axis=0)
df['PolicyYear'] = df['PolicyYear'].ffill(axis=0)
df['PreiodDate']=df['PreiodDate'].fillna(method='ffill')
df['DatePeriod']=df['DatePeriod'].fillna(method='ffill')
df.drop(df[df[0] == "   Total"].index, inplace=True)
df.drop(df[df[0] == "POLICY YEAR"].index, inplace=True)
df.drop(df[df[0] == "Tokio Marine Quarterly Cession Statement"].index, inplace=True)
df.drop(df[df[0] == "As of March 2022"].index, inplace=True)
df.drop(df[df[0] == "Ceded Activity"].index, inplace=True)
df=df[df[0].notna()]
df=df.dropna(axis=1,how='all')
df=df.drop([13],axis=1)
df[11]=df[11].replace(to_replace='Net Written Premium', value=np.nan, regex=True)
df[11]=df[11].replace(to_replace='Ceded Paid Loss and Expense', value=np.nan, regex=True)
df[11]=df[11].replace(to_replace='Less Commission on WP', value=np.nan, regex=True)
df['AccidentYear'] = df[0]
cols = list(df.columns)
cols = [cols[-1]] + cols[:-1]
df = df[cols]
df['AccidentYear']=df['AccidentYear'].replace(to_replace='Auto - 50%', value=np.nan, regex=True)
df['AccidentYear']=df['AccidentYear'].replace(to_replace='Property - 50%', value=np.nan, regex=True)
df['AccidentYear']=df['AccidentYear'].replace(to_replace='Property - 50% - FL', value=np.nan, regex=True)
df['AccidentYear']=df['AccidentYear'].replace(to_replace='Property - 50% - Other', value=np.nan, regex=True)
df['AccidentYear']=df['AccidentYear'].replace(to_replace='AY ', value='', regex=True)
m=df[0].str.startswith('AY')
df.loc[m,0]=np.nan
df[0]=df[0].fillna(method='ffill')
df = df.dropna(axis=0, subset=[1])
df['AccidentYear'] =df.apply(lambda row: row['PolicyYear'] if pd.isnull(row['AccidentYear']) else row['AccidentYear'], axis=1)
df[12]=np.nan
df[13]=np.nan
df[14]=np.nan
df[15]=np.nan
df['index']=df['index'].replace(to_replace=2, value=np.nan, regex=True)
mask = df[['index']].isna().all(axis=1)
df.loc[mask, 1:15] = df.loc[mask, 1:15].shift(4, axis=1)
df=df.fillna(0)
df[1] =[(lambda x: np.format_float_positional(x))(x) for x in df[1]]
df[3] =[(lambda x: np.format_float_positional(x))(x) for x in df[3]]
df[5] =[(lambda x: np.format_float_positional(x))(x) for x in df[5]]
df[7] =[(lambda x: np.format_float_positional(x))(x) for x in df[7]]
df[9] =[(lambda x: np.format_float_positional(x))(x) for x in df[9]]
df[11] =df[11].replace(to_replace=' ',value=0)

df[11] =[(lambda x: np.format_float_positional(x))(x) for x in df[11]]
df[12] =[(lambda x: np.format_float_positional(x))(x) for x in df[12]]
df[13] =[(lambda x: np.format_float_positional(x))(x) for x in df[13]]
df[14] =[(lambda x: np.format_float_positional(x))(x) for x in df[14]]
df[15] =[(lambda x: np.format_float_positional(x))(x) for x in df[15]]
df_template=pd.DataFrame(columns=['PolicyYear','AccidentYear',	'AsOfDate','PeriodDate','DataPeriod','InsuranceType','WrittenPremiumAmount',
'EarnedPremiumAmount','CommissionAmount','UnearnedPremiumAmount','PaidLossAmount','PaidExpenseAmount',
'AdjustedIncLoss','AdjustedIncExpense','CaseReserveLossAmount','CaseReserveExpenseAmount','TransactionDate',
'FileName','ProcessDate'])
df_template['PolicyYear']=df['PolicyYear'].round(0)
df_template['PolicyYear']=df_template['PolicyYear'].astype('int')
df_template['AccidentYear']=df['AccidentYear'].astype('int')
df_template['AsOfDate']=(pd.to_datetime(As_of)+ pd.offsets.MonthEnd(0)).strftime("%m/%d/%Y")
df_template['PeriodDate']=(pd.to_datetime(df['PreiodDate'])+ pd.offsets.MonthEnd(0)).dt.strftime("%m/%d/%Y")
df_template['DataPeriod']=df['DatePeriod']
df_template['InsuranceType']=df[0]
df_template['WrittenPremiumAmount']=df[1]
df_template['EarnedPremiumAmount']=df[3]
df_template['CommissionAmount']=df[5]
df_template['UnearnedPremiumAmount']=df[7]
df_template['PaidLossAmount']=df[9]
df_template['PaidExpenseAmount']=df[11]
df_template['AdjustedIncLoss']=df[12]
df_template['AdjustedIncExpense']=df[13]
df_template['CaseReserveLossAmount']=df[14]
df_template['CaseReserveExpenseAmount']=df[15]
df_template['TransactionDate']=(pd.to_datetime(As_of)+ pd.offsets.MonthEnd(0)).strftime("%m/%d/%Y")
df_template['FileName']=file
df_template['ProcessDate']=date.today()
df_template.set_index('PolicyYear', inplace=True)
file=re.sub('xlsx$', 'csv', file)
df_template.to_csv(file)