# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 13:10:21 2022

@author: lkarpo
"""

import pandas as pd
import numpy as np
import pyodbc 

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=PHLYDWHPROD;'
                      'Database=PHLYWarehouse_Staging;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

source=pd.read_excel('C:/Users/lkarpo/Downloads/HCC_London_Surety_assumed_2_2023.xls',sheet_name=['Policies'])
target=pd.read_sql_query("""select * from dbo.src_HCC_London_Premium_Archive where TransactionDate='2023-1-31 00:00:00.000'""",conn)
source=source.get('Policies')
source = source[source['Unnamed: 11'].notna()]
header=source.iloc[0]
source=source[1:]
source.columns = header
source['ASLOB']=source['ASLOB'].astype('int')
target['ASLOBCode']=target['ASLOBCode'].astype('int')
source['MONO']=source['MONO'].astype('int')
target['MonolineASLOB']=target['MonolineASLOB'].astype('int')
source['EFF DATE']=source['EFF DATE'].astype('datetime64[ns]')
source['EXP DATE']=source['EXP DATE'].astype('datetime64[ns]')
source['WRIT PREM']=source['WRIT PREM'].astype('int')
target['WrittenPremium']=target['WrittenPremium'].astype('int')
source['COMM. & BROK. %']=source['COMM. & BROK. %'].astype('int')
target['CommissionAndBrokerPct']=target['CommissionAndBrokerPct'].astype('int')
source['COMM. & BROK. $']=source['COMM. & BROK. $'].astype('int')
target['CommissionAndBrokerAmount']=target['CommissionAndBrokerAmount'].astype('int')
source['BALANCE DUE']=source['BALANCE DUE'].astype('int')
target['BalanceDue']=target['BalanceDue'].astype('int')
source['UPR']=source['UPR'].astype('int')





source=source.loc[:,["Insured Name","POLICY","ASLOB","MONO","PROD","EXP PROD",
                     "EFF DATE","EXP DATE","WRIT PREM","COMM. & BROK. %",
                     "COMM. & BROK. $","BALANCE DUE","UPR"]]
target=target.loc[:,["InsuredName","PolicyNumber","ASLOBCode","MonolineASLOB",
                     "ProductCode","ExperienceProduct","EffectiveDate","ExpirationDate",
                     "WrittenPremium","CommissionAndBrokerPct","CommissionAndBrokerAmount",
                     "BalanceDue","CurrentUnearnedPremium"]]
source=source.rename(columns={"Insured Name":"InsuredName","POLICY":"PolicyNumber",
                              "ASLOB":"ASLOBCode","MONO":"MonolineASLOB","PROD":"ProductCode",
                              "EXP PROD":"ExperienceProduct","EFF DATE":"EffectiveDate",
                              "EXP DATE":"ExpirationDate","WRIT PREM":"WrittenPremium",
                              "COMM. & BROK. %":"CommissionAndBrokerPct","COMM. & BROK. $":"CommissionAndBrokerAmount",
                              "BALANCE DUE":"BalanceDue","UPR":"CurrentUnearnedPremium"})

target['CurrentUnearnedPremium']=target['CurrentUnearnedPremium'].astype('int')
source["WrittenPremium"]=round(source["WrittenPremium"],0)
source["CommissionAndBrokerPct"]=round(source["CommissionAndBrokerPct"],0)
source["CommissionAndBrokerAmount"]=round(source["CommissionAndBrokerAmount"],0)
source["BalanceDue"]=round(source["BalanceDue"],0)
source["CurrentUnearnedPremium"]=round(source["CurrentUnearnedPremium"],0)
target["WrittenPremium"]=round(target["WrittenPremium"],0)
target["CommissionAndBrokerPct"]=round(target["CommissionAndBrokerPct"],0)
target["CommissionAndBrokerAmount"]=round(target["CommissionAndBrokerAmount"],0)
target["BalanceDue"]=round(target["BalanceDue"],0)
target["CurrentUnearnedPremium"]=round(target["CurrentUnearnedPremium"],0)

final_df=pd.merge(source,target, how='left', left_on=['InsuredName', 'PolicyNumber', 'ASLOBCode', 'MonolineASLOB',
       'ProductCode', 'ExperienceProduct', 'EffectiveDate', 'ExpirationDate',
       'WrittenPremium', 'CommissionAndBrokerPct', 'CommissionAndBrokerAmount',
       'BalanceDue', 'CurrentUnearnedPremium'], right_on=['InsuredName', 'PolicyNumber', 'ASLOBCode', 'MonolineASLOB',
       'ProductCode', 'ExperienceProduct', 'EffectiveDate', 'ExpirationDate',
       'WrittenPremium', 'CommissionAndBrokerPct', 'CommissionAndBrokerAmount',
       'BalanceDue', 'CurrentUnearnedPremium'], indicator=True)

source=source.add_prefix('S_')
target=target.add_prefix('T_')

final_df_outside=pd.merge(source,target, how='outer', left_on=['S_InsuredName', 'S_PolicyNumber', 'S_ASLOBCode', 'S_MonolineASLOB',
       'S_ProductCode', 'S_ExperienceProduct', 'S_EffectiveDate',
       'S_ExpirationDate', 'S_WrittenPremium', 'S_CommissionAndBrokerPct',
       'S_CommissionAndBrokerAmount', 'S_BalanceDue',
       'S_CurrentUnearnedPremium'], right_on=['T_InsuredName', 'T_PolicyNumber', 'T_ASLOBCode', 'T_MonolineASLOB',
       'T_ProductCode', 'T_ExperienceProduct', 'T_EffectiveDate',
       'T_ExpirationDate', 'T_WrittenPremium', 'T_CommissionAndBrokerPct',
       'T_CommissionAndBrokerAmount', 'T_BalanceDue',
       'T_CurrentUnearnedPremium'], indicator=True)
is_right_only=final_df_outside['_merge']!='both'
final_df_outside = final_df_outside[is_right_only]

final_df_outsideTOL=pd.merge(source,target, how='outer', left_on=['S_InsuredName', 'S_PolicyNumber', 'S_ASLOBCode', 'S_MonolineASLOB',
       'S_ProductCode', 'S_ExperienceProduct', 'S_EffectiveDate',
       'S_ExpirationDate'], right_on=['T_InsuredName', 'T_PolicyNumber', 'T_ASLOBCode', 'T_MonolineASLOB',
       'T_ProductCode', 'T_ExperienceProduct', 'T_EffectiveDate',
       'T_ExpirationDate'], indicator=True)

final_df_outsideTOL['difference'] = (abs(final_df_outsideTOL['S_WrittenPremium']+final_df_outsideTOL['S_CommissionAndBrokerPct']+final_df_outsideTOL['S_CommissionAndBrokerAmount']+final_df_outsideTOL['S_BalanceDue']+final_df_outsideTOL['S_CurrentUnearnedPremium'])
- (abs(final_df_outsideTOL['T_WrittenPremium']+final_df_outsideTOL['T_CommissionAndBrokerPct']+final_df_outsideTOL['T_CommissionAndBrokerAmount']+final_df_outsideTOL['T_BalanceDue']+final_df_outsideTOL['T_CurrentUnearnedPremium'])))

final_df_outsideTOL=final_df_outsideTOL.drop(final_df_outsideTOL[(final_df_outsideTOL['_merge'] =='both') & (final_df_outsideTOL['difference'] <= 1)].index)
