# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 15:39:31 2022

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
source=pd.read_excel('C:/Users/lkarpo/Downloads/LibertyMutual_Assumed_Accrual_2_2023.xls',sheet_name=['Liberty Policies'])
target=pd.read_sql_query('select * from src_LibertyMutual_Premium_Current',conn)
source=source.get('Liberty Policies')
source = source.drop(source.index[source['Assumed Reinsurance Policies to Book'].isnull()])
source=source.iloc[5:]
header=source.iloc[0]
source=source[1:]
source.columns = header
source = source.drop(source.index[source['EFF DATE'].isnull()])
source['ASLOB']=source['ASLOB'].values.astype('int')
source['MONO']=source['MONO'].values.astype('int')
source['EFF DATE']=source['EFF DATE'].values.astype('datetime64[ns]')
source['EXP DATE']=source['EXP DATE'].values.astype('datetime64[ns]')
source['PREM. AFTER TAX & FEES']=source['PREM. AFTER TAX & FEES'].values.astype('float')
source['PREM. AFTER TAX & FEES']=round(source['PREM. AFTER TAX & FEES'],0)
source['PLUS: LIBERTY TAX & FEES']=source['PLUS: LIBERTY TAX & FEES'].values.astype('float')
source['PLUS: LIBERTY TAX & FEES']=round(source['PLUS: LIBERTY TAX & FEES'],0)
source['TOTAL PREMIUM']=source['TOTAL PREMIUM'].values.astype('float')
source['TOTAL PREMIUM']=round(source['TOTAL PREMIUM'],0)
source['LESS: BROKER FEE']=source['LESS: BROKER FEE'].values.astype('float')
source['LESS: BROKER FEE']=round(source['LESS: BROKER FEE'],0)
source['LESS: LIBERTY COMM.']=source['LESS: LIBERTY COMM.'].values.astype('float')
source['LESS: LIBERTY COMM.']=round(source['LESS: LIBERTY COMM.'],0)
source['BALANCE DUE']=source['BALANCE DUE'].values.astype('float')
source['BALANCE DUE']=round(source['BALANCE DUE'],0)
source['Days']=source['Days'].values.astype('int')
target['PremiumAfterTaxesAndFees']=round(target['PremiumAfterTaxesAndFees'],0)
target['PlusLibertyTaxAndFees']=round(target['PlusLibertyTaxAndFees'],0)
target['TotalPremium']=round(target['TotalPremium'],0)
target['LessBrokerFee']=round(target['LessBrokerFee'],0)
target['LessLibertyCommission']=round(target['LessLibertyCommission'],0)
target['BalanceDue']=round(target['BalanceDue'],0)
target['UnearnedPremium']=round(target['UnearnedPremium'],0)
source=source.loc[:,['Insured Name','POLICY','ASLOB','MONO','PROD','EXP',
                       'EFF DATE','EXP DATE','PREM. AFTER TAX & FEES',
                       'PLUS: LIBERTY TAX & FEES','TOTAL PREMIUM','LESS: BROKER FEE','LESS: LIBERTY COMM.',
                       'BALANCE DUE','UPR CURR']]
target=target.loc[:,['InsuredName','PolicyNumber','ASLOBCode','MonolineASLOB','ProductCode',
                       'ExperienceProduct','EffectiveDate','ExpirationDate',
                       'PremiumAfterTaxesAndFees','PlusLibertyTaxAndFees','TotalPremium',
                       'LessBrokerFee','LessLibertyCommission','BalanceDue','UnearnedPremium']]
source=source.rename(columns={'Insured Name':'InsuredName','POLICY':'PolicyNumber','ASLOB':'ASLOBCode',
                              'MONO':'MonolineASLOB','PROD':'ProductCode','EXP':'ExperienceProduct',
                              'EFF DATE':'EffectiveDate','EXP DATE':'ExpirationDate','PREM. AFTER TAX & FEES':'PremiumAfterTaxesAndFees',
                              'PLUS: LIBERTY TAX & FEES':'PlusLibertyTaxAndFees','TOTAL PREMIUM':'TotalPremium',
                              'LESS: BROKER FEE':'LessBrokerFee','LESS: LIBERTY COMM.':'LessLibertyCommission','BALANCE DUE':'BalanceDue',
                              'UPR CURR':'UnearnedPremium'})

finaldf=pd.merge(source,target,how='left',left_on=('InsuredName','PolicyNumber','ASLOBCode','MonolineASLOB','ProductCode',
                       'ExperienceProduct','EffectiveDate','ExpirationDate',
                       'PremiumAfterTaxesAndFees','PlusLibertyTaxAndFees','TotalPremium',
                       'LessBrokerFee','LessLibertyCommission','BalanceDue','UnearnedPremium'),right_on=('InsuredName','PolicyNumber','ASLOBCode','MonolineASLOB','ProductCode',
                       'ExperienceProduct','EffectiveDate','ExpirationDate',
                       'PremiumAfterTaxesAndFees','PlusLibertyTaxAndFees','TotalPremium',
                       'LessBrokerFee','LessLibertyCommission','BalanceDue','UnearnedPremium'), indicator=True)

source=source.add_prefix('S_')   
target=target.add_prefix('T_')  

final_df_outside=pd.merge(source,target,how='outer',left_on=('S_InsuredName', 'S_PolicyNumber', 'S_ASLOBCode', 'S_MonolineASLOB',
       'S_ProductCode', 'S_ExperienceProduct', 'S_EffectiveDate',
       'S_ExpirationDate', 'S_PremiumAfterTaxesAndFees',
       'S_PlusLibertyTaxAndFees', 'S_TotalPremium', 'S_LessBrokerFee',
       'S_LessLibertyCommission', 'S_BalanceDue', 'S_UnearnedPremium'),right_on=('T_InsuredName', 'T_PolicyNumber', 'T_ASLOBCode', 'T_MonolineASLOB',
       'T_ProductCode', 'T_ExperienceProduct', 'T_EffectiveDate',
       'T_ExpirationDate', 'T_PremiumAfterTaxesAndFees',
       'T_PlusLibertyTaxAndFees', 'T_TotalPremium', 'T_LessBrokerFee',
       'T_LessLibertyCommission', 'T_BalanceDue', 'T_UnearnedPremium'), indicator=True)


is_right_only=final_df_outside['_merge']!='both'
final_df_outside = final_df_outside[is_right_only] 

final_df_outsideS=final_df_outside.loc[:,['S_InsuredName', 'S_PolicyNumber', 'S_ASLOBCode', 'S_MonolineASLOB',
       'S_ProductCode', 'S_ExperienceProduct', 'S_EffectiveDate',
       'S_ExpirationDate', 'S_PremiumAfterTaxesAndFees',
       'S_PlusLibertyTaxAndFees', 'S_TotalPremium', 'S_LessBrokerFee',
       'S_LessLibertyCommission', 'S_BalanceDue', 'S_UnearnedPremium']]
final_df_outsideT=final_df_outside.loc[:,['T_InsuredName', 'T_PolicyNumber', 'T_ASLOBCode', 'T_MonolineASLOB',
       'T_ProductCode', 'T_ExperienceProduct', 'T_EffectiveDate',
       'T_ExpirationDate', 'T_PremiumAfterTaxesAndFees',
       'T_PlusLibertyTaxAndFees', 'T_TotalPremium', 'T_LessBrokerFee',
       'T_LessLibertyCommission', 'T_BalanceDue', 'T_UnearnedPremium']]
final_df_outsideS = final_df_outsideS.dropna(how='all')
final_df_outsideT = final_df_outsideT.dropna(how='all')
final_df_outsideTol=pd.merge(final_df_outsideS,final_df_outsideT,how='outer',left_on=('S_InsuredName', 'S_PolicyNumber', 'S_ASLOBCode', 'S_MonolineASLOB',
       'S_ProductCode', 'S_ExperienceProduct', 'S_EffectiveDate',
       'S_ExpirationDate'),right_on=('T_InsuredName', 'T_PolicyNumber', 'T_ASLOBCode', 'T_MonolineASLOB',
       'T_ProductCode', 'T_ExperienceProduct', 'T_EffectiveDate',
       'T_ExpirationDate'), indicator=True)
final_df_outsideTol['Delta']=abs(abs(final_df_outsideTol['S_PremiumAfterTaxesAndFees']+
                                 final_df_outsideTol['S_PlusLibertyTaxAndFees']+ 
                                 final_df_outsideTol['S_TotalPremium']+
                                 final_df_outsideTol['S_LessBrokerFee']+ 
                                 final_df_outsideTol['S_LessLibertyCommission']+ 
                                 final_df_outsideTol['S_BalanceDue']+ 
                                 final_df_outsideTol['S_UnearnedPremium'])-abs(final_df_outsideTol['T_PremiumAfterTaxesAndFees']+
                                                                               final_df_outsideTol['T_PlusLibertyTaxAndFees']+ final_df_outsideTol['T_TotalPremium']+ final_df_outsideTol['T_LessBrokerFee']+
                                                                               final_df_outsideTol['T_LessLibertyCommission']+ final_df_outsideTol['T_BalanceDue']+ final_df_outsideTol['T_UnearnedPremium']))
final_df_outsideTol=final_df_outsideTol.drop(final_df_outsideTol[(final_df_outsideTol['_merge'] =='both') & (final_df_outsideTol['Delta'] <= 1)].index)
