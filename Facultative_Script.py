# -*- coding: utf-8 -*-
"""
Created on Tue May 10 14:16:22 2022

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

source=pd.read_excel('C:/Users/lkarpo/Downloads/Facultative Template.xls')
target=pd.read_sql_query("""select * from dbo.src_XLS_Facultative_CededCommission where acctngMonth = 2 and acctngYear=2023""",conn)

source=source.loc[:,['acctngMonth', 'acctngYear', 'companycode', 'contractcode',
       'contractPeriod', 'productcode','experienceProduct', 
       'aslobcode','policynumber','writtenPremium', 'commissionRate',
       'cededCommissionAmt', 'unearnedPremiumPrior', 'unearnedCommissionPrior',
       'unearnedPremiumCurrent', 'unearnedCommissionCurrent']]

target=target.loc[:,['acctngMonth', 'acctngYear', 'companycode', 'contractcode',
       'contractPeriod', 'productcode','experienceProduct', 
       'aslobcode','policynumber','writtenPremium', 'commissionRate',
       'cededCommissionAmt', 'unearnedPremiumPrior', 'unearnedCommissionPrior',
       'unearnedPremiumCurrent', 'unearnedCommissionCurrent']]



source['aslobcode']=source['aslobcode'].astype('int')
target['aslobcode']=target['aslobcode'].astype('int')

target['cededCommissionAmt']=target['cededCommissionAmt'].astype('float64')
target['unearnedPremiumPrior']=target['unearnedPremiumPrior'].astype('float64')
target['unearnedCommissionPrior']=target['unearnedCommissionPrior'].astype('float64')
target['unearnedPremiumCurrent']=target['unearnedPremiumCurrent'].astype('float64')
target['unearnedCommissionCurrent']=target['unearnedCommissionCurrent'].astype('float64')
target["experienceProduct"]=target["experienceProduct"].replace('Unknown',np.nan)
target['unearnedPremiumPrior']=target['unearnedPremiumPrior'].replace(0,np.nan)
target['unearnedCommissionPrior']=target['unearnedCommissionPrior'].replace(0,np.nan)
target['unearnedPremiumCurrent']=target['unearnedPremiumCurrent'].replace(0,np.nan)
target['unearnedCommissionCurrent']=target['unearnedCommissionCurrent'].replace(0,np.nan)
target['writtenPremium']=round(target['writtenPremium'],0)
source['writtenPremium']=round(source['writtenPremium'],0)
target['commissionRate']=round(target['commissionRate'],0)
source['commissionRate']=round(source['commissionRate'],0)
target['cededCommissionAmt']=round(target['cededCommissionAmt'],0)
source['cededCommissionAmt']=round(source['cededCommissionAmt'],0)
target['unearnedPremiumPrior']=round(target['unearnedPremiumPrior'],0)
source['unearnedPremiumPrior']=round(source['unearnedPremiumPrior'],0)
target['unearnedCommissionPrior']=round(target['unearnedCommissionPrior'],0)
source['unearnedCommissionPrior']=round(source['unearnedCommissionPrior'],0)
target['unearnedPremiumCurrent']=round(target['unearnedPremiumCurrent'],0)
source['unearnedPremiumCurrent']=round(source['unearnedPremiumCurrent'],0)
target['unearnedCommissionCurrent']=round(target['unearnedCommissionCurrent'],0)
source['unearnedCommissionCurrent']=round(source['unearnedCommissionCurrent'],0)

final_df=pd.merge(source,target, how='left',left_on=['acctngMonth', 'acctngYear', 'companycode', 'contractcode',
       'contractPeriod', 'productcode', 'experienceProduct',
       'aslobcode', 'policynumber', 'writtenPremium',
       'cededCommissionAmt', 'unearnedPremiumPrior', 'unearnedCommissionPrior',
       'unearnedPremiumCurrent', 'unearnedCommissionCurrent'],right_on=['acctngMonth', 'acctngYear', 'companycode', 'contractcode',
       'contractPeriod', 'productcode', 'experienceProduct',
       'aslobcode', 'policynumber', 'writtenPremium',
       'cededCommissionAmt', 'unearnedPremiumPrior', 'unearnedCommissionPrior',
       'unearnedPremiumCurrent', 'unearnedCommissionCurrent'],indicator=True)

source=source.add_prefix('S_')
target=target.add_prefix('T_')                                                                        
                                                                        
final_df_outside=pd.merge(source,target, how='outer',left_on=['S_acctngMonth', 'S_acctngYear', 'S_companycode', 'S_contractcode',
       'S_contractPeriod', 'S_productcode',
       'S_experienceProduct', 'S_aslobcode', 'S_policynumber',
       'S_writtenPremium', 'S_cededCommissionAmt',
       'S_unearnedPremiumPrior', 'S_unearnedCommissionPrior',
       'S_unearnedPremiumCurrent', 'S_unearnedCommissionCurrent'],right_on=['T_acctngMonth', 'T_acctngYear', 'T_companycode', 'T_contractcode',
       'T_contractPeriod', 'T_productcode',
       'T_experienceProduct', 'T_aslobcode', 'T_policynumber',
       'T_writtenPremium', 'T_cededCommissionAmt',
       'T_unearnedPremiumPrior', 'T_unearnedCommissionPrior',
       'T_unearnedPremiumCurrent', 'T_unearnedCommissionCurrent'],indicator=True)

is_right_only=final_df_outside['_merge']!='both'
final_df_outside = final_df_outside[is_right_only]

final_df_outsideS=final_df_outside.loc[:,['S_acctngMonth', 'S_acctngYear', 'S_companycode', 'S_contractcode',
       'S_contractPeriod', 'S_productcode',
       'S_experienceProduct', 'S_aslobcode', 'S_policynumber',
       'S_writtenPremium', 'S_cededCommissionAmt',
       'S_unearnedPremiumPrior', 'S_unearnedCommissionPrior',
       'S_unearnedPremiumCurrent', 'S_unearnedCommissionCurrent']]
final_df_outsideT=final_df_outside.loc[:,['T_acctngMonth', 'T_acctngYear', 'T_companycode', 'T_contractcode',
       'T_contractPeriod', 'T_productcode',
       'T_experienceProduct', 'T_aslobcode', 'T_policynumber',
       'T_writtenPremium', 'T_cededCommissionAmt',
       'T_unearnedPremiumPrior', 'T_unearnedCommissionPrior',
       'T_unearnedPremiumCurrent', 'T_unearnedCommissionCurrent']]

final_df_outsideS = final_df_outsideS.dropna(how='all')
final_df_outsideT = final_df_outsideT.dropna(how='all')

final_df_outsideTol=pd.merge(final_df_outsideS,final_df_outsideT,how='outer',left_on=('S_acctngMonth', 'S_acctngYear', 'S_companycode', 'S_contractcode',
       'S_contractPeriod', 'S_productcode', 'S_experienceProduct', 'S_aslobcode', 'S_policynumber'),right_on=('T_acctngMonth', 'T_acctngYear', 'T_companycode', 'T_contractcode',
       'T_contractPeriod', 'T_productcode',
       'T_experienceProduct', 'T_aslobcode', 'T_policynumber'), indicator=True)

final_df_outsideTol['difference'] = (abs(final_df_outsideTol['S_writtenPremium']+final_df_outsideTol['S_cededCommissionAmt']))-(abs(final_df_outsideTol['T_writtenPremium']+final_df_outsideTol['T_cededCommissionAmt']))
