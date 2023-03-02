# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 21:18:44 2022

@author: lkarpo
"""
import pandas as pd
import numpy as np
import pyodbc 

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=P00NORSQL049;'
                      'Database=PHLYWarehouse_Staging;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

#PASTE ADJUSTED HEADERS
source=pd.read_excel('C:/Users/lkarpo/Downloads/template_excl_procede012023.xls')
target=pd.read_sql_query('select * from dbo.src_cededLoss_exclProCede_current',conn) 

target=target.loc[:,["company","claim_number","insured_name","account_number","policy_number"
                     ,"policy_eff_date","policy_exp_date","accident_yr","date_of_loss","report_date",
                     "accident_state","Treaty","Reinsurer","rating","product","exp_product",
                     "ceded_case","ceded_clae","ceded_pdloss","ceded_pdlae","ceded_incurred",
                     "Paid_Loss_Recovered","Paid_LAE_Recovered","Total_Recovered","Paid_DCC",
                     "Paid_ANO","Case_DCC","Case_ANO"]] 
pd.set_option('display.float_format', '{:.2f}'.format)
target['policy_number']=target['policy_number'].replace('Unknown',np.nan) 
source['account_number']=source['account_number'].astype('float')
source['account_number']=source['account_number'].apply(lambda x: '%.0f' % x).values.tolist()
target['account_number']=target['account_number'].apply(lambda x: '%.0f' % x).values.tolist()
source['policy_eff_date']=source['policy_eff_date'].astype('datetime64[ns]')
target['policy_eff_date']=target['policy_eff_date'].replace('1900-01-01 00:00:00',np.nan) 
source['policy_exp_date']=source['policy_exp_date'].astype('datetime64[ns]')
target['policy_exp_date']=target['policy_exp_date'].replace('1900-01-01 00:00:00',np.nan) 
source['date_of_loss']=source['date_of_loss'].astype('datetime64[ns]')
source['report_date']=source['report_date'].astype('datetime64[ns]')
target['rating']=target['rating'].replace('      ',np.nan)

source=source.rename(columns={"company":"company","claim_number":"claim_number","insured_name":"insured_name",
                              "account_number":"account_number","policy_number":"policy_number","policy_eff_date":"policy_eff_date",
                              "policy_exp_date":"policy_exp_date","accident_yr":"accident_yr","date_of_loss":"date_of_loss","report_date":"report_date","accident_state":"accident_state",
                              "Treaty":"Treaty","Reinsurer":"Reinsurer","rating":"rating","product":"product","exp_product":"exp_product","ceded_case":"ceded_case","ceded_clae":"ceded_clae",
                              "ceded_pdloss":"ceded_pdloss","ceded_pdlae":"ceded_pdlae","ceded_incurred":"ceded_incurred",
                              "Paid Loss Recovered":"Paid_Loss_Recovered","Paid LAE Recovered":"Paid_LAE_Recovered","Total Recovered":"Total_Recovered",
                              "Paid DCC":"Paid_DCC","Paid ANO":"Paid_ANO","Case DCC":"Case_DCC","Case ANO":"Case_ANO"})

source['ceded_case']=round(source['ceded_case'],0)
source['ceded_clae']=round(source['ceded_clae'],0)
source['ceded_pdloss']=round(source['ceded_pdloss'],0)
source['ceded_pdlae']=round(source['ceded_pdlae'],0)
source['ceded_incurred']=round(source['ceded_incurred'],0)
source['Paid_Loss_Recovered']=round(source['Paid_Loss_Recovered'],0)
source['Paid_LAE_Recovered']=round(source['Paid_LAE_Recovered'],0)
source['Total_Recovered']=round(source['Total_Recovered'],0)
source['Paid_DCC']=round(source['Paid_DCC'],0)
source['Paid_ANO']=round(source['Paid_ANO'],0)
source['Case_DCC']=round(source['Case_DCC'],0)
source['Case_ANO']=round(source['Case_ANO'],0)
target['ceded_case']=round(target['ceded_case'],0)
target['ceded_clae']=round(target['ceded_clae'],0)
target['ceded_pdloss']=round(target['ceded_pdloss'],0)
target['ceded_pdlae']=round(target['ceded_pdlae'],0)
target['ceded_incurred']=round(target['ceded_incurred'],0)
target['Paid_Loss_Recovered']=round(target['Paid_Loss_Recovered'],0)
target['Paid_LAE_Recovered']=round(target['Paid_LAE_Recovered'],0)
target['Total_Recovered']=round(target['Total_Recovered'],0)
target['Paid_DCC']=round(target['Paid_DCC'],0)
target['Paid_ANO']=round(target['Paid_ANO'],0)
target['Case_DCC']=round(target['Case_DCC'],0)
target['Case_ANO']=round(target['Case_ANO'],0)       
target['account_number']=target['account_number'].replace('-1',np.nan)
target['report_date']=target['report_date'].replace('0',np.nan)
source['report_date']=source['report_date'].replace('NaT',np.nan)
target['accident_state']=target['accident_state'].replace('Un',np.nan)
source['accident_state']=source['accident_state'].replace('',np.nan)
target.rating=target.rating.str.replace(' ','')
target.Reinsurer=target.Reinsurer.str.replace(' ','')
source.Reinsurer=source.Reinsurer.str.replace(' ','')
target.insured_name=target.insured_name.str.replace(' ','')
source.insured_name=source.insured_name.str.replace(' ','')
target.Treaty=target.Treaty.str.replace(' ','')
source.Treaty=source.Treaty.str.replace(' ','')
target.policy_number=target.policy_number.str.replace(' ','')
source.policy_number=source.policy_number.str.replace(' ','')

final_df=pd.merge(source,target,how='left',left_on=['company', 'claim_number',
       'policy_number', 'policy_eff_date', 'policy_exp_date', 'accident_yr',
       'date_of_loss', 'report_date', 'accident_state', 'Treaty', 'Reinsurer',
       'rating', 'product', 'exp_product', 'ceded_case', 'ceded_clae',
       'ceded_pdloss', 'ceded_pdlae', 'ceded_incurred', 'Paid_Loss_Recovered',
       'Paid_LAE_Recovered', 'Total_Recovered', 'Paid_DCC', 'Paid_ANO',
       'Case_DCC', 'Case_ANO'],right_on=['company', 'claim_number',
       'policy_number', 'policy_eff_date', 'policy_exp_date', 'accident_yr',
       'date_of_loss', 'report_date', 'accident_state', 'Treaty', 'Reinsurer',
       'rating', 'product', 'exp_product', 'ceded_case', 'ceded_clae',
       'ceded_pdloss', 'ceded_pdlae', 'ceded_incurred', 'Paid_Loss_Recovered',
       'Paid_LAE_Recovered', 'Total_Recovered', 'Paid_DCC', 'Paid_ANO',
       'Case_DCC', 'Case_ANO'], indicator=True)

is_right_only=final_df['_merge']!='both'
final_df_notmatch = final_df[is_right_only]
                                         
source=source.add_prefix('S_')
target=target.add_prefix('T_')


final_df_OUT=pd.merge(source,target,how='outer',left_on=['S_company', 'S_claim_number',
       'S_policy_number', 'S_policy_eff_date', 'S_policy_exp_date',
       'S_accident_yr', 'S_date_of_loss', 'S_report_date', 'S_accident_state',
       'S_Treaty', 'S_Reinsurer', 'S_rating', 'S_product', 'S_exp_product',
       'S_ceded_case', 'S_ceded_clae', 'S_ceded_pdloss', 'S_ceded_pdlae',
       'S_ceded_incurred', 'S_Paid_Loss_Recovered', 'S_Paid_LAE_Recovered',
       'S_Total_Recovered', 'S_Paid_DCC', 'S_Paid_ANO', 'S_Case_DCC',
       'S_Case_ANO'],right_on=['T_company', 'T_claim_number', 
       'T_policy_number', 'T_policy_eff_date', 'T_policy_exp_date',
       'T_accident_yr', 'T_date_of_loss', 'T_report_date', 'T_accident_state',
       'T_Treaty', 'T_Reinsurer', 'T_rating', 'T_product', 'T_exp_product',
       'T_ceded_case', 'T_ceded_clae', 'T_ceded_pdloss', 'T_ceded_pdlae',
       'T_ceded_incurred', 'T_Paid_Loss_Recovered', 'T_Paid_LAE_Recovered',
       'T_Total_Recovered', 'T_Paid_DCC', 'T_Paid_ANO', 'T_Case_DCC',
       'T_Case_ANO'], indicator=True)
                               
is_right_only=final_df_OUT['_merge']!='both'
final_df_OUT = final_df_OUT[is_right_only]

final_df_OUTS=final_df_OUT.loc[:,['S_company', 'S_claim_number',
       'S_policy_number', 'S_policy_eff_date', 'S_policy_exp_date',
       'S_accident_yr', 'S_date_of_loss', 'S_report_date', 'S_accident_state',
       'S_Treaty', 'S_Reinsurer', 'S_rating', 'S_product', 'S_exp_product',
       'S_ceded_case', 'S_ceded_clae', 'S_ceded_pdloss', 'S_ceded_pdlae',
       'S_ceded_incurred', 'S_Paid_Loss_Recovered', 'S_Paid_LAE_Recovered',
       'S_Total_Recovered', 'S_Paid_DCC', 'S_Paid_ANO', 'S_Case_DCC',
       'S_Case_ANO']]
final_df_OUTT=final_df_OUT.loc[:,['T_company', 'T_claim_number',
       'T_policy_number', 'T_policy_eff_date', 'T_policy_exp_date',
       'T_accident_yr', 'T_date_of_loss', 'T_report_date', 'T_accident_state',
       'T_Treaty', 'T_Reinsurer', 'T_rating', 'T_product', 'T_exp_product',
       'T_ceded_case', 'T_ceded_clae', 'T_ceded_pdloss', 'T_ceded_pdlae',
       'T_ceded_incurred', 'T_Paid_Loss_Recovered', 'T_Paid_LAE_Recovered',
       'T_Total_Recovered', 'T_Paid_DCC', 'T_Paid_ANO', 'T_Case_DCC',
       'T_Case_ANO']]

final_df_OUTS = final_df_OUTS.dropna(how='all')
final_df_OUTT = final_df_OUTT.dropna(how='all')
final_df_OUTT['T_report_date']=final_df_OUTT['T_report_date'].replace('1900-01-01 00:00:00',np.nan)
final_df_OUTT['T_company']=final_df_OUTT['T_company'].replace('NA',np.nan)
final_df_OUTT['T_Treaty']=final_df_OUTT['T_Treaty'].replace('N/A',np.nan)
final_df_OUTS['S_claim_number']=final_df_OUTS['S_claim_number'].str.replace(' ','')
final_df_OUTS=final_df_OUTS.replace(' ','')
final_df_OUTT=final_df_OUTT.replace(' ','')
final_df_OUTT['T_Treaty']=final_df_OUTT['T_Treaty'].str[:42]
final_df_OUTS['S_Treaty']=final_df_OUTS['S_Treaty'].str[:42]
final_df_OUTT['T_exp_product']=final_df_OUTT['T_exp_product'].astype('str')
final_df_OUTS['S_exp_product']=final_df_OUTS['S_exp_product'].astype('str')
final_df_OUTT['T_exp_product']=final_df_OUTT['T_exp_product'].str.replace(' ','')
final_df_OUTS['S_exp_product']=final_df_OUTS['S_exp_product'].str.replace(' ','')
final_df_OUTS['S_product']=final_df_OUTS['S_product'].astype('str')
final_df_OUTS['S_product']=final_df_OUTS['S_product'].str.replace(' ','')

final_df_outsideTol=pd.merge(final_df_OUTS,final_df_OUTT,how='outer',left_on=['S_company', 'S_claim_number',
       'S_policy_number', 'S_policy_eff_date', 'S_policy_exp_date',
       'S_accident_yr', 'S_date_of_loss', 'S_report_date', 'S_accident_state',
       'S_Treaty', 'S_Reinsurer', 'S_rating', 'S_product','S_exp_product'] ,right_on=['T_company', 'T_claim_number',
       'T_policy_number', 'T_policy_eff_date', 'T_policy_exp_date',
       'T_accident_yr', 'T_date_of_loss', 'T_report_date', 'T_accident_state',
       'T_Treaty', 'T_Reinsurer', 'T_rating', 'T_product','T_exp_product'],indicator=True)

final_df_outsideTol['diff']=(abs(final_df_outsideTol['S_ceded_case']+final_df_outsideTol['S_ceded_clae']+final_df_outsideTol['S_ceded_pdloss']+
final_df_outsideTol['S_ceded_pdlae']+final_df_outsideTol['S_ceded_incurred']+final_df_outsideTol['S_Paid_Loss_Recovered']+final_df_outsideTol['S_Paid_LAE_Recovered']+
final_df_outsideTol['S_Total_Recovered']+final_df_outsideTol['S_Paid_DCC']+final_df_outsideTol['S_Paid_ANO']+final_df_outsideTol['S_Case_DCC']+final_df_outsideTol['S_Case_ANO']))-(abs(final_df_outsideTol['T_ceded_case']+final_df_outsideTol['T_ceded_clae']+final_df_outsideTol['T_ceded_pdloss']+
final_df_outsideTol['T_ceded_pdlae']+final_df_outsideTol['T_ceded_incurred']+final_df_outsideTol['T_Paid_Loss_Recovered']+final_df_outsideTol['T_Paid_LAE_Recovered']+
final_df_outsideTol['T_Total_Recovered']+final_df_outsideTol['T_Paid_DCC']+final_df_outsideTol['T_Paid_ANO']+final_df_outsideTol['T_Case_DCC']+final_df_outsideTol['T_Case_ANO']))
                                                                                                                                                                                      
final_df_outsideTol = final_df_outsideTol.drop(final_df_outsideTol[(final_df_outsideTol['_merge'] =='both') & (final_df_outsideTol['diff'] <= 1)].index)
