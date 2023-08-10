# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 19:57:16 2022

@author: lkarpo
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

os.chdir('*****')
val = os.getcwd()
dir_list = os.listdir(val)
dir_list= [string for string in dir_list if string.endswith("xlsx")]    
file ="/"+ dir_list[0]
file1 ="/"+ dir_list[1]
file2 ="/"+ dir_list[2]
file=str(val)+file
file1=str(val)+file1
file2=str(val)+file2
file2str=file2.replace(' ','')
date=file2str[-12:-9]+" "
dateyr=file2[-7:-5]
date=date+dateyr
date=datetime.strptime(date,'%b %y').date()
date=pd.to_datetime(date, format='%Y-%M-%d').strftime('%#Y%M')

## LOAD
Load=pd.read_excel(file,sheet_name = None)
LoadO=pd.read_excel(file1,sheet_name = None)
LoadC=pd.read_excel(file2,sheet_name = None)
##WP

Written_PremiumF=LoadC.get('Written Premium')
Written_PremiumF=Written_PremiumF[Written_PremiumF['Unnamed: 4'].notna()]
header=Written_PremiumF.iloc[0]
Written_PremiumF=Written_PremiumF[1:]
Written_PremiumF.columns = header
Written_PremiumF['PolicyID']=Written_PremiumF['PolicyID'].astype(str)
Written_PremiumF['Tran ID']=Written_PremiumF['Tran ID'].astype(str)
Written_PremiumF['Total Written Premium']=Written_PremiumF['Total Written Premium'].astype('int64')
Written_PremiumF['Fed Pol Fee']=Written_PremiumF['Fed Pol Fee'].astype('int64')
Written_PremiumF['Reserve Fund']=Written_PremiumF['Reserve Fund'].astype('int64')
Written_PremiumF['HFIAA Surcharge']=Written_PremiumF['HFIAA Surcharge'].astype('int64')
Written_PremiumF['Date Issued']= pd.to_datetime(Written_PremiumF['Date Issued'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
Written_PremiumF['Policy Effective Date']= pd.to_datetime(Written_PremiumF['Policy Effective Date'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
Written_PremiumF=Written_PremiumF.replace(np.nan,"")
Written_PremiumF=Written_PremiumF.set_index('PolicyID')
Written_Premium_N="/WrittenPremium_"+date
Written_Premium_P=val+Written_Premium_N+".csv"
Written_PremiumF.to_csv(Written_Premium_P)
#CP

ClaimPaymentsF=LoadC.get('Claim Payments Annual Stmt')
ClaimPaymentsF=ClaimPaymentsF[ClaimPaymentsF['Unnamed: 4'].notna()]
header=ClaimPaymentsF.iloc[0]
ClaimPaymentsF=ClaimPaymentsF[1:]
ClaimPaymentsF.columns = header
ClaimPaymentsF['Amount']=ClaimPaymentsF['Amount'].astype('float')
ClaimPaymentsF['Payment Date']=pd.to_datetime(ClaimPaymentsF['Payment Date'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimPaymentsF['Date of  Loss']=pd.to_datetime(ClaimPaymentsF['Date of  Loss'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimPaymentsF['Policy Effective Date']=pd.to_datetime(ClaimPaymentsF['Policy Effective Date'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimPaymentsF['Pre Tax Adjuster Payment']=ClaimPaymentsF['Pre Tax Adjuster Payment'].astype('float')
ClaimPaymentsF['State Tax']=ClaimPaymentsF['State Tax'].astype('float')
ClaimPaymentsF['Total Adjuster Payment']=ClaimPaymentsF['Total Adjuster Payment'].astype('float')
ClaimPaymentsF['Reissue Prior Date']=pd.to_datetime(ClaimPaymentsF['Reissue Prior Date'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimPaymentsF['Gross Loss RCVBldg']=ClaimPaymentsF['Gross Loss RCVBldg'].astype('float')
ClaimPaymentsF['Gross Loss RCVCont']=ClaimPaymentsF['Gross Loss RCVCont'].astype('float')
ClaimPaymentsF=ClaimPaymentsF.set_index('Amount')
ClaimPaymentsN="/ClaimPayments_"+date
ClaimPaymentsP=val+ClaimPaymentsN+".csv"
ClaimPaymentsF.to_csv(ClaimPaymentsP)

#UP

Unearned_PremiumF=LoadC.get('Unearned Premium')
Unearned_PremiumF=Unearned_PremiumF[Unearned_PremiumF['Unnamed: 4'].notna()]
header=Unearned_PremiumF.iloc[0]
Unearned_PremiumF=Unearned_PremiumF[1:]
Unearned_PremiumF.columns = header
Unearned_PremiumF['Policy Issued Date ']=pd.to_datetime(Unearned_PremiumF['Policy Issued Date '], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
Unearned_PremiumF['Transaction Issued Date ']=pd.to_datetime(Unearned_PremiumF['Transaction Issued Date '], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
Unearned_PremiumF['Effective Date']=pd.to_datetime(Unearned_PremiumF['Effective Date'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
Unearned_PremiumF['Expiration Date']=pd.to_datetime(Unearned_PremiumF['Expiration Date'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
Unearned_PremiumF['Summary Date']=pd.to_datetime(Unearned_PremiumF['Summary Date'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
Unearned_PremiumF['Written Premium']=Unearned_PremiumF['Written Premium'].astype('float')
Unearned_PremiumF['Earned to Month End Written Premium ']=Unearned_PremiumF['Earned to Month End Written Premium '].astype('float')
Unearned_PremiumF['Unearned Written Premium ']=Unearned_PremiumF['Unearned Written Premium '].astype('float')
Unearned_PremiumF=Unearned_PremiumF.set_index('pid')
Unearned_PremiumN="/UnearnedPremium_"+date
Unearned_PremiumP=val+Unearned_PremiumN+".csv"
Unearned_PremiumF.to_csv(Unearned_PremiumP)

#OC
OpenClaimF=LoadO.get('Detail')
OpenClaimF=OpenClaimF[OpenClaimF['Unnamed: 3'].notna()]
header=OpenClaimF.iloc[0]
OpenClaimF=OpenClaimF[1:]
OpenClaimF.columns = header
OpenClaimF=OpenClaimF.loc[:,['Claim Number','Opened Date','Days Open','Policy Number','Building Reserves','Content Reserves',
                             'ICC Reserves','Total Reserves','Insured Name 1','Property Address',' Loss Date','Property State',
                             'Property County','Company','Affiliate/Division','Agency Name','Agency Producer Code','Agency Prior Producer Code',
                             'Agency Address','Agency City','Agency County','Agency State','Agency Zip','Agency Phone Number',
                             'Agency Email Address']]
OpenClaimF['Opened Date']=pd.to_datetime(OpenClaimF['Opened Date'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
OpenClaimF[' Loss Date']=pd.to_datetime(OpenClaimF[' Loss Date'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
OpenClaimF['Building Reserves']=OpenClaimF['Building Reserves'].astype('float')
OpenClaimF['Content Reserves']=OpenClaimF['Content Reserves'].astype('float')
OpenClaimF['ICC Reserves']=OpenClaimF['ICC Reserves'].astype('float')
OpenClaimF['Total Reserves']=OpenClaimF['Total Reserves'].astype('float')
OpenClaimF=OpenClaimF.set_index('Claim Number')
OpenClaimN="/OpenClaims_"+date
OpenClaimP=val+OpenClaimN+".csv"
OpenClaimF.to_csv(OpenClaimP)

#CA
ClaimActivityF=Load.get('Detail')
ClaimActivityF=ClaimActivityF[ClaimActivityF['Unnamed: 4'].notna()]
header=ClaimActivityF.iloc[0]
ClaimActivityF=ClaimActivityF[1:]
ClaimActivityF.columns = header
ClaimActivityF['Date Of Loss']=pd.to_datetime(ClaimActivityF['Date Of Loss'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimActivityF['Report Date']=pd.to_datetime(ClaimActivityF['Report Date'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimActivityF['Prelim Report Received']=pd.to_datetime(ClaimActivityF['Prelim Report Received'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimActivityF['Final Report Received']=pd.to_datetime(ClaimActivityF['Final Report Received'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimActivityF['Closed Date']=pd.to_datetime(ClaimActivityF['Closed Date'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimActivityF['Reopen Date']=pd.to_datetime(ClaimActivityF['Reopen Date'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimActivityF['Prior Loss Date']=pd.to_datetime(ClaimActivityF['Prior Loss Date'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimActivityF['Bldg Advanced Payment Date']=pd.to_datetime(ClaimActivityF['Bldg Advanced Payment Date'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimActivityF['Bldg Advanced Payment Processed']=pd.to_datetime(ClaimActivityF['Bldg Advanced Payment Processed'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimActivityF['Cont Advanced Payment Date']=pd.to_datetime(ClaimActivityF['Cont Advanced Payment Date'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimActivityF['Cont Advanced Payment Processed']=pd.to_datetime(ClaimActivityF['Cont Advanced Payment Processed'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimActivityF['Invoice Payment Date']=pd.to_datetime(ClaimActivityF['Invoice Payment Date'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimActivityF['Invoice Payment Processed']=pd.to_datetime(ClaimActivityF['Invoice Payment Processed'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimActivityF['Bldg Payment Date']=pd.to_datetime(ClaimActivityF['Bldg Payment Date'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimActivityF['Bldg Payment Processed']=pd.to_datetime(ClaimActivityF['Bldg Payment Processed'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimActivityF['Cont Payment Date']=pd.to_datetime(ClaimActivityF['Cont Payment Date'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimActivityF['Cont Payment Processed']=pd.to_datetime(ClaimActivityF['Cont Payment Processed'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimActivityF['Special Expense Payment Date']=pd.to_datetime(ClaimActivityF['Special Expense Payment Date'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimActivityF['Special Expense Payment Processed']=pd.to_datetime(ClaimActivityF['Special Expense Payment Processed'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%m/%d/%Y")
ClaimActivityF['Building Reserves']=ClaimActivityF['Building Reserves'].astype('float')
ClaimActivityF['Content Reserves']=ClaimActivityF['Content Reserves'].astype('float')
ClaimActivityF['Loss Outstanding']=ClaimActivityF['Loss Outstanding'].astype('float')
ClaimActivityF['Salvage']=ClaimActivityF['Salvage'].astype('float')
ClaimActivityF['Subrogation']=ClaimActivityF['Subrogation'].astype('float')
ClaimActivityF['Dwelling Gross Loss']=ClaimActivityF['Dwelling Gross Loss'].astype('float')
ClaimActivityF['Contents Gross Loss']=ClaimActivityF['Contents Gross Loss'].astype('float')
ClaimActivityF['Gross Total']=ClaimActivityF['Gross Total'].astype('float')
ClaimActivityF['Dwelling Indemnity']=ClaimActivityF['Dwelling Indemnity'].astype('float')
ClaimActivityF['Contents Indemnity']=ClaimActivityF['Contents Indemnity'].astype('float')
ClaimActivityF['Bldg Advanced Amt']=ClaimActivityF['Bldg Advanced Amt'].astype('float')
ClaimActivityF['Cont Advanced Amt']=ClaimActivityF['Cont Advanced Amt'].astype('float')
ClaimActivityF['Invoice Total']=ClaimActivityF['Invoice Total'].astype('float')
ClaimActivityF['Bldg Payment']=ClaimActivityF['Bldg Payment'].astype('float')
ClaimActivityF['Cont Payment']=ClaimActivityF['Cont Payment'].astype('float')
ClaimActivityF['Special Expense']=ClaimActivityF['Special Expense'].astype('float')
ClaimActivityF['Bldg Coverage']=ClaimActivityF['Bldg Coverage'].astype('float')
ClaimActivityF['Cont Coverage']=ClaimActivityF['Cont Coverage'].astype('float')
ClaimActivityF=ClaimActivityF.set_index('Policy Number')
ClaimActivityF = ClaimActivityF.drop('Rate Method', axis=1)
ClaimActivityN="/ClaimsActivity_"+date
ClaimActivityP=val+ClaimActivityN+".csv"
ClaimActivityF.to_csv(ClaimActivityP)

