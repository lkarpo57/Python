# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 13:14:15 2022

@author: lkarpo
"""


import pandas as pd
import numpy as np
import pyodbc 

##Import
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=P00NORSQL049;'
                      'Database=PHLYWarehouse_Staging;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

source=pd.read_excel('C:/Users/lkarpo/Downloads/PHIL Group_Claimspaid data_010123-013123.xls')
target=pd.read_sql_query('select * from dbo.src_AJ_Flood_Current',conn)

source["Benefit Code Desc"]=source["Benefit Code Desc"].str.strip()
source["Net Pay Amt"]=round(source["Net Pay Amt"],0)
source["UDF Policy "]=source["UDF Policy "].replace("PHPA1083991","PHPA108391")
source["UDF Policy "]=source["UDF Policy "].replace("WANE","PHPA110822")
source["UDF Policy "]=source["UDF Policy "].replace("PHPA1102040","PHPA110204")

sourceG=source.groupby(['Mem Name','Case Num','Claim ID','Benefit Code Desc','UDF Policy ','Incident  DT','Line Itm Key','UDF Program']).sum().reset_index()
sourceG=sourceG.loc[:,["Case Num","Incident  DT","Benefit Code Desc","Net Pay Amt","UDF Policy ","UDF Program"]]

target["ClaimNumber"]=target["ClaimNumber"].values.astype('str')
target["BenefitCodeDescription"]=target["BenefitCodeDescription"].str.strip()
target["TransactionAmount"]=round(target["TransactionAmount"],0)
target["UDFProgram_CoverageCode"]=target["UDFProgram_CoverageCode"].replace("Unknown",np.nan)


targetG=target.groupby(['ClaimantName','ClaimNumber','ClaimID','BenefitCodeDescription','UDF_PolicyNumber','LossDate','LineItemKey','UDFProgram_CoverageCode']).sum().reset_index()

targetG=targetG.loc[:,["ClaimNumber","LossDate","BenefitCodeDescription","TransactionAmount","UDF_PolicyNumber","UDFProgram_CoverageCode"]]

sourceG=sourceG.rename(columns={"Case Num":"ClaimNumber"
                              ,"Incident  DT":"LossDate"
                              ,"Benefit Code Desc":"BenefitCodeDescription"
                              ,"Net Pay Amt":"TransactionAmount"
                              ,"UDF Policy ":"UDF_PolicyNumber"
                              ,"UDF Program":"UDFProgram_CoverageCode"})
targetG["ClaimNumber"]=targetG["ClaimNumber"].values.astype('float')

targetGsub=targetG[targetG['ClaimNumber']==(574488)]
sourceGsub=sourceG[sourceG['ClaimNumber']==(574488)]


final_df=pd.merge(sourceG,targetG, how='left', 
                  left_on=['ClaimNumber','LossDate','BenefitCodeDescription','TransactionAmount','UDF_PolicyNumber','UDFProgram_CoverageCode']
                  , right_on=['ClaimNumber','LossDate','BenefitCodeDescription','TransactionAmount','UDF_PolicyNumber','UDFProgram_CoverageCode'], indicator=True)

sourceG=sourceG.add_prefix('S_')
targetG=targetG.add_prefix('T_')

final_df_outside=pd.merge(sourceG,targetG,how='outer',left_on=['S_ClaimNumber','S_LossDate','S_BenefitCodeDescription','S_TransactionAmount','S_UDF_PolicyNumber']
                                                             ,right_on=['T_ClaimNumber','T_LossDate','T_BenefitCodeDescription','T_TransactionAmount','T_UDF_PolicyNumber'],indicator=True)
                                                      
is_right_only=final_df_outside['_merge']!='both'
final_df_outside = final_df_outside[is_right_only]

final_df_outsideS=final_df_outside.loc[:,["S_ClaimNumber","S_LossDate","S_BenefitCodeDescription","S_TransactionAmount","S_UDF_PolicyNumber","S_UDFProgram_CoverageCode"]]
final_df_outsideT=final_df_outside.loc[:,["T_ClaimNumber","T_LossDate","T_BenefitCodeDescription","T_TransactionAmount","T_UDF_PolicyNumber","T_UDFProgram_CoverageCode"]]

final_df_outsideS = final_df_outsideS.dropna(how='all')
final_df_outsideT = final_df_outsideT.dropna(how='all')

final_df_outsideTol=pd.merge(final_df_outsideS,final_df_outsideT,how='outer',left_on=['S_ClaimNumber','S_LossDate','S_BenefitCodeDescription','S_UDF_PolicyNumber']
                                                             ,right_on=['T_ClaimNumber','T_LossDate','T_BenefitCodeDescription','T_UDF_PolicyNumber'],indicator=True)

final_df_outsideTol['difference'] = abs(abs(final_df_outsideTol['S_TransactionAmount']) -abs(final_df_outsideTol['T_TransactionAmount']))

final_df_outsideTol = final_df_outsideTol.drop(final_df_outsideTol[(final_df_outsideTol['_merge'] =='both') & (final_df_outsideTol['difference'] <= 1)].index)

##final_df.to_csv('C:/Users/lkarpo/Downloads/AJFlood_Source_check_LOSS.csv')
##final_df_outsideTol.to_csv('C:/Users/lkarpo/Downloads/AJFlood_Target_check_LOSS.csv')