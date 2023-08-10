# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 15:37:57 2022

@author: lkarpo
"""

import pandas as pd
import numpy as np
import sharepy
import requests
import pyodbc 

conn = pyodbc.connect('*****')
cursor = conn.cursor()

source=pd.read_excel('C:/Users/lkarpo/Downloads//TMM_Canada_Assumed_Loss_Template_2_2023.xls', sheet_name='LOSSES')
target=pd.read_sql_query('select * from dbo.src_TM_Canada_current',conn)
header=source.iloc[4]
source=source[1:]
source.columns = header

m = source['PROD'].where(source['PROD'] == 'CHG IN MONTH').ffill()
source=source[m.notnull()]

source = source.drop(source.index[source['Account Name'].isnull()])
source=source[1:]

source=source.loc[:,['PROD','Account Name','U/W YEAR','CUR','Policy #','Eff\nDate','Exp Date',
                     'Claim No.','Loss Date','loss yr','Acc State','Paid Loss','Paid LAE - A&O',
                     'Paid LAE - DCC','O/S Loss','O/S LAE- A&O','O/S LAE- DCC', 'Direct Incurred']]
target=target.loc[:,['ProductCode', 'ExperienceProduct',
       'AccountName', 'PolicyNumber', 'EffectiveDate', 'ExpirationDate',
       'ClaimNumber', 'LossDate', 'LossYear', 'AccidentState',
       'Currency', 'PaidLoss', 'ANOPaidAmount', 'DCCPaidAmount',
       'CaseLossAmount', 'CaseANOAmount', 'CaseDCCAmount', 'DirectIncurred']]
source=source.rename(columns={'PROD':'ProductCode','Account Name':'AccountName','CUR':'Currency',
                              'Policy #':'PolicyNumber','Eff\nDate':'EffectiveDate','Exp Date':'ExpirationDate',
                              'Claim No.':'ClaimNumber','Loss Date':'LossDate','loss yr':'LossYear','Acc State':'AccidentState',
                              'Paid Loss':'PaidLoss','Paid LAE - A&O':'ANOPaidAmount','Paid LAE - DCC':'DCCPaidAmount',
                              'O/S Loss':'CaseLossAmount','O/S LAE- A&O':'CaseANOAmount','O/S LAE- DCC':'CaseDCCAmount', 
                              'Direct Incurred':'DirectIncurred'})
source=source.loc[:,['ProductCode', 'AccountName',
       'EffectiveDate', 'ExpirationDate', 'ClaimNumber', 'LossDate',
       'LossYear', 'AccidentState', 'PaidLoss', 'ANOPaidAmount',
       'DCCPaidAmount', 'CaseLossAmount', 'CaseANOAmount', 'CaseDCCAmount',
       'DirectIncurred']]
target=target.loc[:,['ProductCode', 'AccountName',
       'EffectiveDate', 'ExpirationDate', 'ClaimNumber', 'LossDate',
       'LossYear', 'AccidentState', 'PaidLoss', 'ANOPaidAmount',
       'DCCPaidAmount', 'CaseLossAmount', 'CaseANOAmount', 'CaseDCCAmount',
       'DirectIncurred']]
source['EffectiveDate']=source['EffectiveDate'].values.astype('datetime64[ns]')
source['ExpirationDate']=source['ExpirationDate'].values.astype('datetime64[ns]')



source['LossYear']=source['LossYear'].values.astype('int')
target['LossYear']=target['LossYear'].values.astype('int')
source['PaidLoss']=source['PaidLoss'].values.astype('int')
target['PaidLoss']=target['PaidLoss'].values.astype('int')
source['ANOPaidAmount']=source['ANOPaidAmount'].values.astype('int')
target['ANOPaidAmount']=target['ANOPaidAmount'].values.astype('int')
source['DCCPaidAmount']=source['DCCPaidAmount'].values.astype('int')
target['DCCPaidAmount']=target['DCCPaidAmount'].values.astype('int')
source['CaseLossAmount']=source['CaseLossAmount'].values.astype('int')
target['CaseLossAmount']=target['CaseLossAmount'].values.astype('int')
source['CaseANOAmount']=source['CaseANOAmount'].values.astype('int')
target['CaseANOAmount']=target['CaseANOAmount'].values.astype('int')
source['CaseDCCAmount']=source['CaseDCCAmount'].values.astype('int')
target['CaseDCCAmount']=target['CaseDCCAmount'].values.astype('int')
source['DirectIncurred']=source['DirectIncurred'].values.astype('int')
target['DirectIncurred']=target['DirectIncurred'].values.astype('int')
source['AccountName'] = source['AccountName'].str.replace(' ', '')
target['AccountName'] = target['AccountName'].str.replace(' ', '')
source['AccountName'] = source['AccountName'].str.replace(',', '')
target['AccountName'] = target['AccountName'].str.replace(',', '')
source['AccountName'] = source['AccountName'].str.replace('.', '')
target['AccountName'] = target['AccountName'].str.replace('.', '')


df_final=pd.merge(source,target,how='left',left_on=['ProductCode', 'AccountName',
        'ClaimNumber',
       'LossYear', 'AccidentState', 'PaidLoss', 'ANOPaidAmount',
       'DCCPaidAmount', 'CaseLossAmount', 'CaseANOAmount', 'CaseDCCAmount',
       'DirectIncurred'],right_on=['ProductCode', 'AccountName',
       'ClaimNumber',
       'LossYear', 'AccidentState', 'PaidLoss', 'ANOPaidAmount',
       'DCCPaidAmount', 'CaseLossAmount', 'CaseANOAmount', 'CaseDCCAmount',
       'DirectIncurred'],indicator=True)
source=source.add_prefix('S_')   
target=target.add_prefix('T_')
df_finalouter=pd.merge(source,target,how='outer',left_on=['S_ProductCode', 'S_AccountName','S_ClaimNumber', 'S_LossDate', 'S_LossYear',
       'S_AccidentState', 'S_PaidLoss', 'S_ANOPaidAmount', 'S_DCCPaidAmount',
       'S_CaseLossAmount', 'S_CaseANOAmount', 'S_CaseDCCAmount',
       'S_DirectIncurred'],right_on=['T_ProductCode', 'T_AccountName', 'T_ClaimNumber', 'T_LossDate', 'T_LossYear',
       'T_AccidentState', 'T_PaidLoss', 'T_ANOPaidAmount', 'T_DCCPaidAmount',
       'T_CaseLossAmount', 'T_CaseANOAmount', 'T_CaseDCCAmount',
       'T_DirectIncurred'],indicator=True)
is_right_only=df_finalouter['_merge']!='both'
df_finalouter = df_finalouter[is_right_only]
final_df_outsideS=df_finalouter.loc[:,['S_ProductCode', 'S_AccountName', 'S_ClaimNumber', 'S_LossYear',
       'S_AccidentState', 'S_PaidLoss', 'S_ANOPaidAmount', 'S_DCCPaidAmount',
       'S_CaseLossAmount', 'S_CaseANOAmount', 'S_CaseDCCAmount',
       'S_DirectIncurred']]
final_df_outsideT=df_finalouter.loc[:,['T_ProductCode', 'T_AccountName', 'T_ClaimNumber', 'T_LossYear',
       'T_AccidentState', 'T_PaidLoss', 'T_ANOPaidAmount', 'T_DCCPaidAmount',
       'T_CaseLossAmount', 'T_CaseANOAmount', 'T_CaseDCCAmount',
       'T_DirectIncurred']]
final_df_outsideS = final_df_outsideS.dropna(how='all')
final_df_outsideT = final_df_outsideT.dropna(how='all')
final_df_outsideTol=pd.merge(source,target,how='outer',left_on=('S_ProductCode', 'S_AccountName', 'S_ClaimNumber', 'S_LossYear',
       'S_AccidentState'),right_on=('T_ProductCode', 'T_AccountName', 'T_ClaimNumber', 'T_LossYear',
       'T_AccidentState'), indicator=True)
is_right_only=final_df_outsideTol['_merge']!='both'
final_df_outsideTol = final_df_outsideTol[is_right_only]
                                     
