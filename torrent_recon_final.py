# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 16:02:51 2022

@author: lkarpo
"""
import pandas as pd
import numpy as np
import pyodbc 
 
        
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=PHLYDWHPROD;'
                      'Datacbase=PHLYWarehouse_Staging;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
sourceCP=pd.read_csv('C:/Users/lkarpo/Downloads/ClaimPayments_202301.csv')
sourceRC=pd.read_csv('C:/Users/lkarpo/Downloads/OpenClaims_202301.csv')
sourceCA=pd.read_csv('C:/Users/lkarpo/Downloads/ClaimsActivity_202301.csv')
sourceUP=pd.read_csv('C:/Users/lkarpo/Downloads/UnearnedPremium_202301.csv')
sourceWP=pd.read_csv('C:/Users/lkarpo/Downloads/WrittenPremium_202301.csv')

targetCP=pd.read_sql_query("""select * From PHLYWarehouse_Staging.dbo.src_Torrent_ClaimPayments_Current""",conn)
targetRC=pd.read_sql_query("""select * From PHLYWarehouse_Staging.dbo.src_Torrent_ClaimReserves_Current""",conn)
targetCA=pd.read_sql_query("""select * From PHLYWarehouse_Staging.dbo.src_Torrent_ClaimsActivity_Current""",conn)
targetUP=pd.read_sql_query("""select * From PHLYWarehouse_Staging.dbo.src_Torrent_UnearnedPremium_Current""",conn)
targetWP=pd.read_sql_query("""select * From PHLYWarehouse_Staging.dbo.src_Torrent_WrittenPremium_Current""",conn)


targetCP=targetCP.loc[:,['ClaimNumber', 'Amount', 'PaymentDate', 'DateofLoss', 'PropertyState',
       'PolicyNumber', 'PolicyEffectiveDate', 'FICONumber', 'PaymentType',
       'PaidTo', 'PID', 'CheckNumber', 'ClaimSpecialExpenseTypeDesc',
       'IsReissue', 'PreTaxAdjusterPayment', 'StateTax',
       'TotalAdjusterPayment', 'ReissuePriorDate', 'ReissueCheckNumber',
       'GrossLossRCVBldg', 'GrossLossRCVCont', 'CompanyName',
       'AffiliateDivision', 'BldgCWOP', 'ContCWOP', 'ICCCWOP', 'BldgDescLOB']]

targetRC=targetRC.loc[:,['ClaimNumber', 'OpenedDate', 'DaysOpen', 'PolicyNumber',
       'BuildingReserves', 'ContentReserves', 'ICCReserves', 'TotalReserves',
       'InsuredName', 'PropertyAddress', 'LossDate', 'PropertyState',
       'PropertyCounty', 'Company', 'AffiliateDivision', 'AgencyName',
       'AgencyProducerCode', 'AgencyPriorProducerCode', 'AgencyAddress',
       'AgencyCity', 'AgencyCounty', 'AgencyState', 'AgencyZip',
       'AgencyPhoneNumber', 'AgencyEmailAddress']]

targetCA=targetCA.loc[:,['PolicyNumber', 'PolicyType', 'FloodZoneDesc', 'PolicyTerm',
       'AdjustingCompany', 'ClaimState', 'ClaimNumber', 'BuildingReserves',
       'ContentReserves', 'LossOutstanding', 'Salvage', 'Subrogation',
       'DateOfLoss', 'ReportDate', 'PrelimReportReceived',
       'FinalReportReceived', 'ClosedDate', 'ReopenDate', 'NumberOfDaysOpen',
       'ReasonClaimStillOpen', 'ClaimCause', 'Status', 'InsuredName',
       'MailingAddress', 'PropertyAddress', 'InsuredEmail', 'InsuredPhone',
       'InsuredCellPhone', 'InsuredWorkPhone', 'PrimaryClaimContactName',
       'PrimaryClaimContactPhone', 'PrimaryClaimContactCellPhone',
       'PrimaryClaimContactEmail', 'NFIPCommunity', 'County', 'ZipCode',
       'PriorLossDate', 'DwellingGrossLoss', 'ContentsGrossLoss', 'GrossTotal',
       'DwellingIndemnity', 'ContentsIndemnity', 'BldgAdvancedAmt',
       'BldgAdvancedPaymentDate', 'BldgAdvancedPaymentProcessed',
       'ContAdvancedAmt', 'ContAdvancedPaymentDate',
       'ContAdvancedPaymentProcessed', 'InvoiceTotal', 'InvoicePaymentDate',
       'InvoicePaymentProcessed', 'BldgPayment', 'BldgPaymentDate',
       'BldgPaymentProcessed', 'ContPayment', 'ContPaymentDate',
       'ContPaymentProcessed', 'SpecialExpense', 'SpecialExpensePaymentDate',
       'SpecialExpensePaymentProcessed', 'AgencyName', 'AgencyCode',
       'AgencyState', 'FICONumber', 'PolicyForm', 'BldgCoverage',
       'ContCoverage', 'ProvisionallyorTenatively', 'IntitalLossCreatedBy',
       'IntialLossCreatedByType', 'CompanyName', 'ClaimsExaminer', 'ICC',
       'Supplemental', 'CWOPCodeBldg', 'CWOPCodeContents', 'RemoteAdjusting']]

targetUP=targetUP.loc[:,['PolicyNumber', 'pid', 'PolicyIssueDate', 'TransactionIssuedDate',
       'EffectiveDate', 'ExpirationDate', 'Insured', 'WrittenPremium',
       'DaysEarned', 'EarnedtoMonthEndWrittenPremium',
       'UnearnedWrittenPremium', 'TranType', 'Address1', 'City', 'State',
       'Zip', 'DerivedStatus', 'Company', 'AffiliateDivision', 'SummaryDate']]


targetWP=targetWP.loc[:,['PolicyID', 'TranID', 'StatusID', 'PolicyNumber', 'NewRolloverIndDesc',
       'FirstName', 'LastName', 'TotalWrittenPremium', 'FedPolFee',
       'ReserveFund', 'HFIAASurcharge', 'NFIPTransCode', 'NFIPTransType',
       'DateIssued', 'Company', 'Agency', 'PropertyAddress', 'PropertyCity',
       'PropertyZip', 'PropertyState', 'PropertyCounty', 'ProducerNumber',
       'OccupancyType', 'PolicyForm', 'BuildingDescriptionLOB',
       'HFIAATransaction', 'AffiliateDivision', 'PolicyEffectiveDate']]

#CP
sourceCP=sourceCP.rename(columns={'Amount':'Amount', 'Payment Date':'PaymentDate', 'Date of  Loss':'DateofLoss', 'Property State':'PropertyState',
       'Policy Number':'PolicyNumber', 'Policy Effective Date':'PolicyEffectiveDate', 'FICO Number':'FICONumber', 'Payment Type':'PaymentType',
       'Paid To':'PaidTo', 'PID':'PID', 'Check Number':'CheckNumber', 'Claim Special Expense Type Desc':'ClaimSpecialExpenseTypeDesc',
       'Is Reissue':'IsReissue', 'Pre Tax Adjuster Payment':'PreTaxAdjusterPayment', 'State Tax':'StateTax',
       'Total Adjuster Payment':'TotalAdjusterPayment', 'Reissue Prior Date':'ReissuePriorDate', 'Reissue Check Number':'ReissueCheckNumber',
       'Gross Loss RCVBldg':'GrossLossRCVBldg', 'Gross Loss RCVCont':'GrossLossRCVCont', 'Claim Number':'ClaimNumber',
       'Company Name':'CompanyName', 'Affiliate/Division':'AffiliateDivision', 'Bldg CWOP':'BldgCWOP', 'Cont CWOP':'ContCWOP',
       'ICCCWOP':'ICCCWOP', 'Bldg Desc LOB':'BldgDescLOB'})

targetCP=targetCP.replace('',np.nan)
targetCP=targetCP.replace(' ',np.nan)
targetCP['PaymentDate'] = pd.to_datetime(targetCP['PaymentDate'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')
targetCP['DateofLoss'] = pd.to_datetime(targetCP['DateofLoss'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')

targetCP['PaymentDate'] = pd.to_datetime(targetCP['PaymentDate'].astype('datetime64[ns]'))
targetCP['DateofLoss'] = pd.to_datetime(targetCP['DateofLoss'].astype('datetime64[ns]'))
sourceCP['PaymentDate'] = pd.to_datetime(sourceCP['PaymentDate'].astype('datetime64[ns]'))
sourceCP['DateofLoss'] = pd.to_datetime(sourceCP['DateofLoss'].astype('datetime64[ns]'))

targetCP['PolicyEffectiveDate'] = pd.to_datetime(targetCP['PolicyEffectiveDate'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')
targetCP['ReissuePriorDate'] = pd.to_datetime(targetCP['ReissuePriorDate'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')
targetCP['PolicyEffectiveDate'] = pd.to_datetime(targetCP['PaymentDate'].astype('datetime64[ns]'))
targetCP['ReissuePriorDate'] = pd.to_datetime(targetCP['DateofLoss'].astype('datetime64[ns]'))
sourceCP['PolicyEffectiveDate'] = pd.to_datetime(sourceCP['PaymentDate'].astype('datetime64[ns]'))
sourceCP['ReissuePriorDate'] = pd.to_datetime(sourceCP['DateofLoss'].astype('datetime64[ns]'))

targetCP['PolicyNumber']=targetCP['PolicyNumber'].astype('int64')
targetCP['PID']=targetCP['PID'].astype('int64')
targetCP['CheckNumber']=targetCP['CheckNumber'].astype('int64')
targetCP['ClaimNumber']=targetCP['ClaimNumber'].astype('int64')
targetCP['ReissueCheckNumber']=targetCP['ReissueCheckNumber'].astype('float64')
targetCP['BldgCWOP']=targetCP['BldgCWOP'].astype('float64')
targetCP['ContCWOP']=targetCP['ContCWOP'].astype('float64')

targetCP=targetCP.replace('1/1/1900',np.nan)


final_dfCP=pd.merge(sourceCP,targetCP,how='left',left_on=['ClaimNumber', 'Amount', 'PaymentDate', 'DateofLoss', 'PropertyState',
       'PolicyNumber', 'PolicyEffectiveDate', 'FICONumber', 'PaymentType',
       'PaidTo', 'PID', 'CheckNumber', 'ClaimSpecialExpenseTypeDesc',
       'IsReissue', 'PreTaxAdjusterPayment', 'StateTax',
       'TotalAdjusterPayment', 'ReissuePriorDate', 'ReissueCheckNumber',
       'GrossLossRCVBldg', 'GrossLossRCVCont', 'CompanyName',
       'AffiliateDivision', 'BldgCWOP', 'ContCWOP', 'ICCCWOP', 'BldgDescLOB'],
                   right_on=['ClaimNumber', 'Amount', 'PaymentDate', 'DateofLoss', 'PropertyState',
       'PolicyNumber', 'PolicyEffectiveDate', 'FICONumber', 'PaymentType',
       'PaidTo', 'PID', 'CheckNumber', 'ClaimSpecialExpenseTypeDesc',
       'IsReissue', 'PreTaxAdjusterPayment', 'StateTax',
       'TotalAdjusterPayment', 'ReissuePriorDate', 'ReissueCheckNumber',
       'GrossLossRCVBldg', 'GrossLossRCVCont', 'CompanyName',
       'AffiliateDivision', 'BldgCWOP', 'ContCWOP', 'ICCCWOP', 'BldgDescLOB'], indicator=True)

sourceCP=sourceCP.add_prefix('S_')
targetCP=targetCP.add_prefix('T_')

final_dfCP_outer=pd.merge(sourceCP,targetCP,how='outer',left_on=['S_Amount', 'S_PaymentDate', 'S_DateofLoss', 'S_PropertyState',
       'S_PolicyNumber', 'S_PolicyEffectiveDate', 'S_FICONumber',
       'S_PaymentType', 'S_PaidTo', 'S_PID', 'S_CheckNumber',
       'S_ClaimSpecialExpenseTypeDesc', 'S_IsReissue',
       'S_PreTaxAdjusterPayment', 'S_StateTax', 'S_TotalAdjusterPayment',
       'S_ReissuePriorDate', 'S_ReissueCheckNumber', 'S_GrossLossRCVBldg',
       'S_GrossLossRCVCont', 'S_ClaimNumber', 'S_CompanyName',
       'S_AffiliateDivision', 'S_BldgCWOP', 'S_ContCWOP', 'S_ICCCWOP',
       'S_BldgDescLOB'],
                   right_on=['T_Amount', 'T_PaymentDate', 'T_DateofLoss', 'T_PropertyState',
       'T_PolicyNumber', 'T_PolicyEffectiveDate', 'T_FICONumber',
       'T_PaymentType', 'T_PaidTo', 'T_PID', 'T_CheckNumber',
       'T_ClaimSpecialExpenseTypeDesc', 'T_IsReissue',
       'T_PreTaxAdjusterPayment', 'T_StateTax', 'T_TotalAdjusterPayment',
       'T_ReissuePriorDate', 'T_ReissueCheckNumber', 'T_GrossLossRCVBldg',
       'T_GrossLossRCVCont', 'T_ClaimNumber', 'T_CompanyName',
       'T_AffiliateDivision', 'T_BldgCWOP', 'T_ContCWOP', 'T_ICCCWOP',
       'T_BldgDescLOB'], indicator=True)

is_right_only=final_dfCP_outer['_merge']!='both'
final_dfCP_outer = final_dfCP_outer[is_right_only]

#RC
sourceRC=sourceRC.rename(columns={'Claim Number':'ClaimNumber', 'Opened Date':'OpenedDate', 'Days Open':'DaysOpen','Policy Number':'PolicyNumber', 'Building Reserves':'BuildingReserves', 'Content Reserves':'ContentReserves', 
                                  'ICC Reserves':'ICCReserves','Total Reserves':'TotalReserves', 'Insured Name 1':'InsuredName', 'Property Address':'PropertyAddress',' Loss Date':'LossDate','Property State':'PropertyState', 'Property County':'PropertyCounty', 'Company':'Company', 
                                  'Affiliate/Division':'AffiliateDivision','Agency Name':'AgencyName', 'Agency Producer Code':'AgencyProducerCode','Agency Prior Producer Code':'AgencyPriorProducerCode','Agency Address':'AgencyAddress', 'Agency City':'AgencyCity', 
                                  'Agency County':'AgencyCounty', 'Agency State':'AgencyState','Agency Zip':'AgencyZip', 'Agency Phone Number':'AgencyPhoneNumber', 'Agency Email Address':'AgencyEmailAddress'})

targetRC['OpenedDate'] = pd.to_datetime(targetRC['OpenedDate'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')
targetRC['LossDate'] = pd.to_datetime(targetRC['LossDate'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')
targetRC['OpenedDate'] = pd.to_datetime(targetRC['OpenedDate'].astype('datetime64[ns]'))
sourceRC['LossDate'] = pd.to_datetime(sourceRC['LossDate'].astype('datetime64[ns]'))
targetRC['LossDate'] = pd.to_datetime(targetRC['LossDate'].astype('datetime64[ns]'))
sourceRC['OpenedDate'] = pd.to_datetime(sourceRC['OpenedDate'].astype('datetime64[ns]'))
targetRC['ClaimNumber']=targetRC['ClaimNumber'].astype('int64')
targetRC['PolicyNumber']=targetRC['PolicyNumber'].astype('int64')
targetRC['AffiliateDivision']=targetRC['AffiliateDivision'].astype('float64')
targetRC['AgencyCounty']=targetRC['AgencyCounty'].astype('float64')
targetRC['AgencyZip']=targetRC['AgencyZip'].astype('int64')

final_dfRC=pd.merge(sourceRC,targetRC,how='left',left_on=['ClaimNumber', 'OpenedDate', 'DaysOpen', 'PolicyNumber',
       'BuildingReserves', 'ContentReserves', 'ICCReserves', 'TotalReserves',
       'InsuredName', 'PropertyAddress', 'LossDate', 'PropertyState',
       'PropertyCounty', 'Company', 'AffiliateDivision', 'AgencyName',
       'AgencyProducerCode', 'AgencyPriorProducerCode', 'AgencyAddress',
       'AgencyCity', 'AgencyCounty', 'AgencyState', 'AgencyZip',
       'AgencyPhoneNumber', 'AgencyEmailAddress'],
                   right_on=['ClaimNumber', 'OpenedDate', 'DaysOpen', 'PolicyNumber',
       'BuildingReserves', 'ContentReserves', 'ICCReserves', 'TotalReserves',
       'InsuredName', 'PropertyAddress', 'LossDate', 'PropertyState',
       'PropertyCounty', 'Company', 'AffiliateDivision', 'AgencyName',
       'AgencyProducerCode', 'AgencyPriorProducerCode', 'AgencyAddress',
       'AgencyCity', 'AgencyCounty', 'AgencyState', 'AgencyZip',
       'AgencyPhoneNumber', 'AgencyEmailAddress'], indicator=True)

sourceRC=sourceRC.add_prefix('S_')
targetRC=targetRC.add_prefix('T_')

final_dfRC_outer=pd.merge(sourceRC,targetRC,how='outer',left_on=['S_ClaimNumber', 'S_OpenedDate', 'S_DaysOpen', 'S_PolicyNumber',
       'S_BuildingReserves', 'S_ContentReserves', 'S_ICCReserves',
       'S_TotalReserves', 'S_InsuredName', 'S_PropertyAddress', 'S_LossDate',
       'S_PropertyState', 'S_PropertyCounty', 'S_Company',
       'S_AffiliateDivision', 'S_AgencyName', 'S_AgencyProducerCode',
       'S_AgencyPriorProducerCode', 'S_AgencyAddress', 'S_AgencyCity',
       'S_AgencyCounty', 'S_AgencyState', 'S_AgencyZip', 'S_AgencyPhoneNumber',
       'S_AgencyEmailAddress'],
                   right_on=['T_ClaimNumber', 'T_OpenedDate', 'T_DaysOpen', 'T_PolicyNumber',
       'T_BuildingReserves', 'T_ContentReserves', 'T_ICCReserves',
       'T_TotalReserves', 'T_InsuredName', 'T_PropertyAddress', 'T_LossDate',
       'T_PropertyState', 'T_PropertyCounty', 'T_Company',
       'T_AffiliateDivision', 'T_AgencyName', 'T_AgencyProducerCode',
       'T_AgencyPriorProducerCode', 'T_AgencyAddress', 'T_AgencyCity',
       'T_AgencyCounty', 'T_AgencyState', 'T_AgencyZip', 'T_AgencyPhoneNumber',
       'T_AgencyEmailAddress'], indicator=True)

is_right_only=final_dfRC_outer['_merge']!='both'
final_dfRC_outer = final_dfRC_outer[is_right_only]

#CA
sourceCA=sourceCA.rename(columns={'Policy Number':'PolicyNumber', 'Policy Type':'PolicyType', 
                                  'Flood Zone Desc':'FloodZoneDesc', 'Policy Term':'PolicyTerm',
                                  'Adjusting Company':'AdjustingCompany', 'Claim State':'ClaimState', 
                                  'Claim Number':'ClaimNumber', 'Building Reserves':'BuildingReserves',
                                  'Content Reserves':'ContentReserves', 'Loss Outstanding':'LossOutstanding', 
                                  'Salvage':'Salvage', 'Subrogation':'Subrogation','Date Of Loss':'DateOfLoss', 
                                  'Report Date':'ReportDate', 'Prelim Report Received':'PrelimReportReceived',
                                  'Final Report Received':'FinalReportReceived', 'Closed Date':'ClosedDate', 
                                  'Reopen Date':'ReopenDate', 'Number Of Days Open':'NumberOfDaysOpen', 
                                  'Reason Claim Still Open':'ReasonClaimStillOpen', 'Claim Cause':'ClaimCause',
                                  'Status':'Status', 'Insured Name':'InsuredName', 'Mailing Address':'MailingAddress', 
                                  'Property Address':'PropertyAddress','Insured Email':'InsuredEmail', 'Insured Phone':'InsuredPhone', 
                                  'Insured Cell Phone':'InsuredCellPhone','Insured Work Phone':'InsuredWorkPhone', 
                                  'Primary Claim Contact Name':'PrimaryClaimContactName','Primary Claim Contact Phone':'PrimaryClaimContactPhone', 
                                  'Primary Claim Contact Cell Phone':'PrimaryClaimContactCellPhone','Primary Claim Contact Email':'PrimaryClaimContactEmail', 
                                  'NFIP Community':'NFIPCommunity', 'County':'County', 'Zip Code':'ZipCode',
                                  'Prior Loss Date':'PriorLossDate', 'Dwelling Gross Loss':'DwellingGrossLoss', 'Contents Gross Loss':'ContentsGrossLoss',
                                  'Gross Total':'GrossTotal', 'Dwelling Indemnity':'DwellingIndemnity', 'Contents Indemnity':'ContentsIndemnity',
                                  'Bldg Advanced Amt':'BldgAdvancedAmt', 'Bldg Advanced Payment Date':'BldgAdvancedPaymentDate',
                                  'Bldg Advanced Payment Processed':'BldgAdvancedPaymentProcessed', 'Cont Advanced Amt':'ContAdvancedAmt',
                                  'Cont Advanced Payment Date':'ContAdvancedPaymentDate', 'Cont Advanced Payment Processed':'ContAdvancedPaymentProcessed',
                                  'Invoice Total':'InvoiceTotal', 'Invoice Payment Date':'InvoicePaymentDate', 'Invoice Payment Processed':'InvoicePaymentProcessed',
                                  'Bldg Payment':'BldgPayment', 'Bldg Payment Date':'BldgPaymentDate', 'Bldg Payment Processed':'BldgPaymentProcessed',
                                  'Cont Payment':'ContPayment', 'Cont Payment Date':'ContPaymentDate', 'Cont Payment Processed':'ContPaymentProcessed','Special Expense':'SpecialExpense', 'Special Expense Payment Date':'SpecialExpensePaymentDate',
                                  'Special Expense Payment Processed':'SpecialExpensePaymentProcessed', 'Agency Name':'AgencyName', 'Agency Code':'AgencyCode',
                                  'Agency State':'AgencyState', 'FICO Number':'FICONumber', 'Policy Form':'PolicyForm', 'Bldg Coverage':'BldgCoverage',
                                  'Cont Coverage':'ContCoverage', 'Provisionally or Tenatively':'ProvisionallyorTenatively',
                                  'Intital Loss Created By':'IntitalLossCreatedBy', 'Intial Loss Created By Type':'IntialLossCreatedByType',
                                  'Company Name':'CompanyName', 'Claims Examiner':'ClaimsExaminer', 'ICC':'ICC', 'Supplemental':'Supplemental',
                                  'CWOP Code  Bldg':'CWOPCodeBldg', 'CWOP Code Contents':'CWOPCodeContents', 'Remote Adjusting':'RemoteAdjusting'})
sourceCA=sourceCA.loc[:,['PolicyNumber', 'PolicyType', 'FloodZoneDesc', 'PolicyTerm',
       'AdjustingCompany', 'ClaimState', 'ClaimNumber', 'BuildingReserves',
       'ContentReserves', 'LossOutstanding', 'Salvage', 'Subrogation',
       'DateOfLoss', 'ReportDate', 'PrelimReportReceived',
       'FinalReportReceived', 'ClosedDate', 'ReopenDate', 'NumberOfDaysOpen',
       'ReasonClaimStillOpen', 'ClaimCause', 'Status', 'InsuredName',
       'MailingAddress', 'PropertyAddress', 'InsuredEmail', 'InsuredPhone',
       'InsuredCellPhone', 'InsuredWorkPhone', 'PrimaryClaimContactName',
       'PrimaryClaimContactPhone', 'PrimaryClaimContactCellPhone',
       'PrimaryClaimContactEmail', 'NFIPCommunity', 'County', 'ZipCode',
       'PriorLossDate', 'DwellingGrossLoss', 'ContentsGrossLoss', 'GrossTotal',
       'DwellingIndemnity', 'ContentsIndemnity', 'BldgAdvancedAmt',
       'BldgAdvancedPaymentDate', 'BldgAdvancedPaymentProcessed',
       'ContAdvancedAmt', 'ContAdvancedPaymentDate',
       'ContAdvancedPaymentProcessed', 'InvoiceTotal', 'InvoicePaymentDate',
       'InvoicePaymentProcessed', 'BldgPayment', 'BldgPaymentDate',
       'BldgPaymentProcessed', 'ContPayment', 'ContPaymentDate',
       'ContPaymentProcessed', 'SpecialExpense', 'SpecialExpensePaymentDate',
       'SpecialExpensePaymentProcessed', 'AgencyName', 'AgencyCode',
       'AgencyState', 'FICONumber', 'PolicyForm', 'BldgCoverage',
       'ContCoverage', 'ProvisionallyorTenatively', 'IntitalLossCreatedBy',
       'IntialLossCreatedByType', 'CompanyName', 'ClaimsExaminer', 'ICC',
       'Supplemental', 'CWOPCodeBldg', 'CWOPCodeContents', 'RemoteAdjusting']]
targetCA['PolicyNumber']=targetCA['PolicyNumber'].astype('int64')
targetCA['ClaimNumber']=targetCA['ClaimNumber'].astype('int64')
targetCA = targetCA.replace('1/1/1900',np.nan)
targetCA = targetCA.replace('N/A',np.nan)


targetCA['DateOfLoss'] = pd.to_datetime(targetCA['DateOfLoss'].astype('datetime64[ns]'))
sourceCA['DateOfLoss'] = pd.to_datetime(sourceCA['DateOfLoss'].astype('datetime64[ns]'))
targetCA['ReportDate'] = pd.to_datetime(targetCA['ReportDate'].astype('datetime64[ns]'))
sourceCA['ReportDate'] = pd.to_datetime(sourceCA['ReportDate'].astype('datetime64[ns]'))
targetCA['PrelimReportReceived'] = pd.to_datetime(targetCA['PrelimReportReceived'].astype('datetime64[ns]'))
sourceCA['PrelimReportReceived'] = pd.to_datetime(sourceCA['PrelimReportReceived'].astype('datetime64[ns]'))
targetCA['PrelimReportReceived'] = pd.to_datetime(targetCA['PrelimReportReceived'].astype('datetime64[ns]'))
sourceCA['PrelimReportReceived'] = pd.to_datetime(sourceCA['PrelimReportReceived'].astype('datetime64[ns]'))
targetCA['FinalReportReceived'] = pd.to_datetime(targetCA['FinalReportReceived'].astype('datetime64[ns]'))
sourceCA['FinalReportReceived'] = pd.to_datetime(sourceCA['FinalReportReceived'].astype('datetime64[ns]'))


targetCA['PriorLossDate'] = pd.to_datetime(targetCA['PriorLossDate'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')
targetCA['BldgAdvancedPaymentDate'] =pd.to_datetime(targetCA['BldgAdvancedPaymentDate'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')
targetCA['BldgAdvancedPaymentProcessed'] = pd.to_datetime(targetCA['BldgAdvancedPaymentProcessed'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')
sourceCA['BldgAdvancedPaymentProcessed'] = pd.to_datetime(sourceCA['BldgAdvancedPaymentProcessed'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')
targetCA['SpecialExpensePaymentProcessed'] = pd.to_datetime(targetCA['SpecialExpensePaymentProcessed'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')
targetCA['ContAdvancedPaymentDate'] = pd.to_datetime(targetCA['ContAdvancedPaymentDate'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')
targetCA['ContAdvancedPaymentProcessed'] = pd.to_datetime(targetCA['ContAdvancedPaymentProcessed'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')
targetCA['InvoicePaymentDate'] = pd.to_datetime(targetCA['InvoicePaymentDate'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')
targetCA['InvoicePaymentProcessed'] = pd.to_datetime(targetCA['InvoicePaymentProcessed'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')
targetCA['BldgPaymentDate'] = pd.to_datetime(targetCA['BldgPaymentDate'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')
targetCA['BldgPaymentProcessed'] = pd.to_datetime(targetCA['BldgPaymentProcessed'].astype('datetime64[ns]'))
targetCA['BldgPaymentDate'] = pd.to_datetime(targetCA['BldgPaymentDate'].astype('str'))
sourceCA['BldgPaymentProcessed'] = pd.to_datetime(sourceCA['BldgPaymentProcessed'].astype('datetime64[ns]'))
sourceCA['BldgPaymentDate'] = pd.to_datetime(sourceCA['BldgPaymentDate'].astype('str'))
targetCA['DateOfLoss'] = pd.to_datetime(targetCA['DateOfLoss'].astype('datetime64[ns]'))
sourceCA['DateOfLoss'] = pd.to_datetime(sourceCA['DateOfLoss'].astype('datetime64[ns]'))
targetCA['ReportDate'] = pd.to_datetime(targetCA['ReportDate'].astype('datetime64[ns]'))
sourceCA['ReportDate'] = pd.to_datetime(sourceCA['ReportDate'].astype('datetime64[ns]'))
targetCA['PriorLossDate'] = pd.to_datetime(targetCA['PriorLossDate'].astype('datetime64[ns]'))
sourceCA['PriorLossDate'] = pd.to_datetime(sourceCA['PriorLossDate'].astype('datetime64[ns]'))
targetCA['BldgAdvancedPaymentDate'] = pd.to_datetime(targetCA['BldgAdvancedPaymentDate'].astype('datetime64[ns]'))
sourceCA['BldgAdvancedPaymentDate'] = pd.to_datetime(sourceCA['BldgAdvancedPaymentDate'].astype('datetime64[ns]'))


targetCA['ContPaymentDate'] = pd.to_datetime(targetCA['ContPaymentDate'].astype('datetime64[ns]'))
targetCA['ContPaymentProcessed'] = pd.to_datetime(targetCA['ContPaymentProcessed'].astype('datetime64[ns]'))
sourceCA['ContPaymentDate'] = pd.to_datetime(sourceCA['ContPaymentDate'].astype('datetime64[ns]'))
sourceCA['ContPaymentProcessed'] = pd.to_datetime(sourceCA['ContPaymentProcessed'].astype('datetime64[ns]'))
sourceCA['SpecialExpensePaymentDate'] = pd.to_datetime(sourceCA['SpecialExpensePaymentDate'].astype('str'))
targetCA['SpecialExpensePaymentDate'] = pd.to_datetime(targetCA['SpecialExpensePaymentDate'].astype('str'))
targetCA['ContAdvancedPaymentDate']=targetCA['ContAdvancedPaymentDate'].astype('str')
targetCA['ContAdvancedPaymentProcessed']=targetCA['ContAdvancedPaymentProcessed'].astype('str')
sourceCA['ContAdvancedPaymentDate']=sourceCA['ContAdvancedPaymentDate'].astype('str')
sourceCA['ContAdvancedPaymentProcessed']=sourceCA['ContAdvancedPaymentProcessed'].astype('str')
targetCA['BldgAdvancedPaymentProcessed'] = pd.to_datetime(targetCA['BldgAdvancedPaymentProcessed'].astype('datetime64[ns]'))
sourceCA['BldgAdvancedPaymentProcessed'] = pd.to_datetime(sourceCA['BldgAdvancedPaymentProcessed'].astype('datetime64[ns]'))

targetCA['ReasonClaimStillOpen']=targetCA['ReasonClaimStillOpen'].astype('float64')
targetCA['InsuredPhone']=targetCA['InsuredPhone'].astype('str')
targetCA['InsuredCellPhone']=targetCA['InsuredCellPhone'].astype('str')
sourceCA['InsuredPhone']=sourceCA['InsuredPhone'].astype('str')
sourceCA['InsuredCellPhone']=sourceCA['InsuredCellPhone'].astype('str')
targetCA['ZipCode']=targetCA['ZipCode'].astype('int')
sourceCA['ZipCode']=sourceCA['ZipCode'].astype('int')

sourceCA['Subrogation']=sourceCA['Subrogation'].astype('int')
targetCA['Subrogation']=sourceCA['Subrogation'].astype('int')

sourceCA['ClosedDate']=sourceCA['ClosedDate'].astype('datetime64[ns]')
sourceCA['ReopenDate']=sourceCA['ReopenDate'].astype('datetime64[ns]')

sourceCA['SpecialExpensePaymentProcessed']=sourceCA['SpecialExpensePaymentProcessed'].astype('float64')
sourceCA['FICONumber']=sourceCA['FICONumber'].astype('float')
targetCA['FICONumber']=targetCA['FICONumber'].astype('float')

targetCA['ICC']=targetCA['ICC'].astype('float64')
targetCA['Supplemental']=targetCA['Supplemental'].astype('float64')
targetCA['CWOPCodeBldg']=targetCA['CWOPCodeBldg'].astype('float64')
targetCA['CWOPCodeContents']=targetCA['CWOPCodeContents'].astype('float64')
targetCA['RemoteAdjusting']=targetCA['RemoteAdjusting'].astype('float64')
targetCA['InsuredWorkPhone']=targetCA['InsuredWorkPhone'].astype('str')
targetCA['InsuredPhone']=targetCA['InsuredPhone'].replace('None',np.nan)
targetCA['InsuredCellPhone']=targetCA['InsuredCellPhone'].replace('None',np.nan)
sourceCA['InsuredPhone']=sourceCA['InsuredPhone'].replace('nan',np.nan)
sourceCA['InsuredCellPhone']=sourceCA['InsuredCellPhone'].replace('nan',np.nan)
targetCA['InsuredWorkPhone']=targetCA['InsuredWorkPhone'].replace('None',np.nan)
targetCA = targetCA.replace('None',np.nan)

final_dfCA=pd.merge(sourceCA,targetCA,how='left', left_on=['PolicyNumber', 'PolicyType', 'FloodZoneDesc', 'PolicyTerm',
       'AdjustingCompany', 'ClaimState', 'ClaimNumber', 'BuildingReserves',
       'ContentReserves', 'LossOutstanding', 'Salvage', 'Subrogation',
       'DateOfLoss', 'ReportDate', 'PrelimReportReceived',
       'FinalReportReceived', 'ClosedDate', 'ReopenDate', 'NumberOfDaysOpen',
       'ReasonClaimStillOpen', 'ClaimCause', 'Status', 'InsuredName',
       'MailingAddress', 'PropertyAddress', 'InsuredEmail', 'InsuredPhone',
       'InsuredCellPhone', 'InsuredWorkPhone', 'PrimaryClaimContactName',
       'PrimaryClaimContactPhone', 'PrimaryClaimContactCellPhone',
       'PrimaryClaimContactEmail', 'NFIPCommunity', 'County', 'ZipCode',
       'PriorLossDate', 'DwellingGrossLoss', 'ContentsGrossLoss', 'GrossTotal',
       'DwellingIndemnity', 'ContentsIndemnity', 'BldgAdvancedAmt',
       'BldgAdvancedPaymentDate', 'BldgAdvancedPaymentProcessed',
       'ContAdvancedAmt', 'ContAdvancedPaymentDate',
       'ContAdvancedPaymentProcessed', 'InvoiceTotal', 'InvoicePaymentDate',
       'InvoicePaymentProcessed', 'BldgPayment', 'BldgPaymentDate',
       'BldgPaymentProcessed', 'ContPayment', 'ContPaymentDate',
       'ContPaymentProcessed', 'SpecialExpense', 'SpecialExpensePaymentDate',
       'SpecialExpensePaymentProcessed', 'AgencyName', 'AgencyCode',
       'AgencyState', 'FICONumber', 'PolicyForm', 'BldgCoverage',
       'ContCoverage', 'ProvisionallyorTenatively', 'IntitalLossCreatedBy',
       'IntialLossCreatedByType', 'CompanyName', 'ClaimsExaminer', 'ICC','Supplemental', 'CWOPCodeBldg', 'CWOPCodeContents', 'RemoteAdjusting'],
                    right_on=['PolicyNumber', 'PolicyType', 'FloodZoneDesc', 'PolicyTerm',
       'AdjustingCompany', 'ClaimState', 'ClaimNumber', 'BuildingReserves',
       'ContentReserves', 'LossOutstanding', 'Salvage', 'Subrogation',
       'DateOfLoss', 'ReportDate', 'PrelimReportReceived',
       'FinalReportReceived', 'ClosedDate', 'ReopenDate', 'NumberOfDaysOpen',
       'ReasonClaimStillOpen', 'ClaimCause', 'Status', 'InsuredName',
       'MailingAddress', 'PropertyAddress', 'InsuredEmail', 'InsuredPhone',
       'InsuredCellPhone', 'InsuredWorkPhone', 'PrimaryClaimContactName',
       'PrimaryClaimContactPhone', 'PrimaryClaimContactCellPhone',
       'PrimaryClaimContactEmail', 'NFIPCommunity', 'County', 'ZipCode',
       'PriorLossDate', 'DwellingGrossLoss', 'ContentsGrossLoss', 'GrossTotal',
       'DwellingIndemnity', 'ContentsIndemnity', 'BldgAdvancedAmt',
       'BldgAdvancedPaymentDate', 'BldgAdvancedPaymentProcessed',
       'ContAdvancedAmt', 'ContAdvancedPaymentDate',
       'ContAdvancedPaymentProcessed', 'InvoiceTotal', 'InvoicePaymentDate',
       'InvoicePaymentProcessed', 'BldgPayment', 'BldgPaymentDate',
       'BldgPaymentProcessed', 'ContPayment', 'ContPaymentDate',
       'ContPaymentProcessed', 'SpecialExpense', 'SpecialExpensePaymentDate',
       'SpecialExpensePaymentProcessed', 'AgencyName', 'AgencyCode',
       'AgencyState', 'FICONumber', 'PolicyForm', 'BldgCoverage',
       'ContCoverage', 'ProvisionallyorTenatively', 'IntitalLossCreatedBy',
       'IntialLossCreatedByType', 'CompanyName', 'ClaimsExaminer', 'ICC',
       'Supplemental', 'CWOPCodeBldg', 'CWOPCodeContents', 'RemoteAdjusting'], indicator=True)

sourceCA=sourceCA.add_prefix('S_')
targetCA=targetCA.add_prefix('T_')

final_dfCA_outside=pd.merge(sourceCA,targetCA,how='outer', left_on=['S_PolicyNumber', 'S_PolicyType', 'S_FloodZoneDesc', 'S_PolicyTerm',
       'S_AdjustingCompany', 'S_ClaimState', 'S_ClaimNumber', 'S_BuildingReserves',
       'S_ContentReserves', 'S_LossOutstanding', 'S_Salvage', 'S_Subrogation',
       'S_DateOfLoss', 'S_ReportDate', 'S_PrelimReportReceived',
       'S_FinalReportReceived', 'S_ClosedDate', 'S_ReopenDate', 'S_NumberOfDaysOpen',
       'S_ReasonClaimStillOpen', 'S_ClaimCause', 'S_Status', 'S_InsuredName',
       'S_MailingAddress', 'S_PropertyAddress', 'S_InsuredEmail', 'S_InsuredPhone',
       'S_InsuredCellPhone', 'S_InsuredWorkPhone', 'S_PrimaryClaimContactName',
       'S_PrimaryClaimContactPhone', 'S_PrimaryClaimContactCellPhone',
       'S_PrimaryClaimContactEmail', 'S_NFIPCommunity', 'S_County', 'S_ZipCode',
       'S_PriorLossDate', 'S_DwellingGrossLoss', 'S_ContentsGrossLoss', 'S_GrossTotal',
       'S_DwellingIndemnity', 'S_ContentsIndemnity', 'S_BldgAdvancedAmt',
       'S_BldgAdvancedPaymentDate', 'S_BldgAdvancedPaymentProcessed',
       'S_ContAdvancedAmt', 'S_ContAdvancedPaymentDate',
       'S_ContAdvancedPaymentProcessed', 'S_InvoiceTotal', 'S_InvoicePaymentDate',
       'S_InvoicePaymentProcessed', 'S_BldgPayment', 'S_BldgPaymentDate',
       'S_BldgPaymentProcessed', 'S_ContPayment', 'S_ContPaymentDate',
       'S_ContPaymentProcessed', 'S_SpecialExpense', 'S_SpecialExpensePaymentDate',
       'S_SpecialExpensePaymentProcessed', 'S_AgencyName', 'S_AgencyCode',
       'S_AgencyState', 'S_FICONumber', 'S_PolicyForm', 'S_BldgCoverage',
       'S_ContCoverage', 'S_ProvisionallyorTenatively', 'S_IntitalLossCreatedBy',
       'S_IntialLossCreatedByType', 'S_CompanyName', 'S_ClaimsExaminer', 'S_ICC','S_Supplemental', 'S_CWOPCodeBldg', 'S_CWOPCodeContents', 'S_RemoteAdjusting'],
                    right_on=['T_PolicyNumber', 'T_PolicyType', 'T_FloodZoneDesc', 'T_PolicyTerm',
       'T_AdjustingCompany', 'T_ClaimState', 'T_ClaimNumber', 'T_BuildingReserves',
       'T_ContentReserves', 'T_LossOutstanding', 'T_Salvage', 'T_Subrogation',
       'T_DateOfLoss', 'T_ReportDate', 'T_PrelimReportReceived',
       'T_FinalReportReceived', 'T_ClosedDate', 'T_ReopenDate', 'T_NumberOfDaysOpen',
       'T_ReasonClaimStillOpen', 'T_ClaimCause', 'T_Status', 'T_InsuredName',
       'T_MailingAddress', 'T_PropertyAddress', 'T_InsuredEmail', 'T_InsuredPhone',
       'T_InsuredCellPhone', 'T_InsuredWorkPhone', 'T_PrimaryClaimContactName',
       'T_PrimaryClaimContactPhone', 'T_PrimaryClaimContactCellPhone',
       'T_PrimaryClaimContactEmail', 'T_NFIPCommunity', 'T_County', 'T_ZipCode',
       'T_PriorLossDate', 'T_DwellingGrossLoss', 'T_ContentsGrossLoss', 'T_GrossTotal',
       'T_DwellingIndemnity', 'T_ContentsIndemnity', 'T_BldgAdvancedAmt',
       'T_BldgAdvancedPaymentDate', 'T_BldgAdvancedPaymentProcessed',
       'T_ContAdvancedAmt', 'T_ContAdvancedPaymentDate',
       'T_ContAdvancedPaymentProcessed', 'T_InvoiceTotal', 'T_InvoicePaymentDate',
       'T_InvoicePaymentProcessed', 'T_BldgPayment', 'T_BldgPaymentDate',
       'T_BldgPaymentProcessed', 'T_ContPayment', 'T_ContPaymentDate',
       'T_ContPaymentProcessed', 'T_SpecialExpense', 'T_SpecialExpensePaymentDate',
       'T_SpecialExpensePaymentProcessed', 'T_AgencyName', 'T_AgencyCode',
       'T_AgencyState', 'T_FICONumber', 'T_PolicyForm', 'T_BldgCoverage',
       'T_ContCoverage', 'T_ProvisionallyorTenatively', 'T_IntitalLossCreatedBy',
       'T_IntialLossCreatedByType', 'T_CompanyName', 'T_ClaimsExaminer', 'T_ICC',
       'T_Supplemental', 'T_CWOPCodeBldg', 'T_CWOPCodeContents', 'T_RemoteAdjusting'], indicator=True)

is_right_only=final_dfCA_outside['_merge']!='both'
final_dfCA_outside = final_dfCA_outside[is_right_only]

##tUP
sourceUP=sourceUP.rename(columns={'pid':'pid', 'Policy Issued Date ':'PolicyIssueDate', 'Transaction Issued Date ':'TransactionIssuedDate',
       'Effective Date':'EffectiveDate', 'Expiration Date':'ExpirationDate', 'Policy Number':'PolicyNumber', 'Insured1':'Insured',
       'Written Premium':'WrittenPremium', 'Days Earned':'DaysEarned',
       'Earned to Month End Written Premium ':'EarnedtoMonthEndWrittenPremium', 'Unearned Written Premium ':'UnearnedWrittenPremium',
       'Tran Type':'TranType', 'Address1':'Address1', 'City':'City', 'State':'State', 'Zip':'Zip', 'Derived Status':'DerivedStatus',
       'Company':'Company', 'Affiliate/Division':'AffiliateDivision', 'Summary Date':'SummaryDate'})
targetUP['PolicyIssueDate'] = pd.to_datetime(targetUP['PolicyIssueDate'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')
targetUP['TransactionIssuedDate'] = pd.to_datetime(targetUP['TransactionIssuedDate'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')
targetUP['EffectiveDate'] = pd.to_datetime(targetUP['EffectiveDate'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')
targetUP['ExpirationDate'] = pd.to_datetime(targetUP['ExpirationDate'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')
targetUP['SummaryDate'] = pd.to_datetime(targetUP['SummaryDate'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')
targetUP = targetUP.replace('None',np.nan)
targetUP['pid'] = targetUP['pid'].astype('int64')
targetUP['PolicyNumber'] = targetUP['PolicyNumber'].astype('int64')
sourceUP['DaysEarned'] = sourceUP['DaysEarned'].astype('int64')
targetUP['AffiliateDivision'] = targetUP['AffiliateDivision'].astype('float64')
targetUP['PolicyIssueDate'] = pd.to_datetime(targetUP['PolicyIssueDate'].astype('datetime64[ns]'))
sourceUP['PolicyIssueDate'] = pd.to_datetime(sourceUP['PolicyIssueDate'].astype('datetime64[ns]'))
targetUP['TransactionIssuedDate'] = pd.to_datetime(targetUP['TransactionIssuedDate'].astype('datetime64[ns]'))
sourceUP['TransactionIssuedDate'] = pd.to_datetime(sourceUP['TransactionIssuedDate'].astype('datetime64[ns]'))
sourceUP['EffectiveDate'] = pd.to_datetime(sourceUP['EffectiveDate'].astype('datetime64[ns]'))
targetUP['EffectiveDate'] = pd.to_datetime(targetUP['EffectiveDate'].astype('datetime64[ns]'))
targetUP['ExpirationDate'] = pd.to_datetime(targetUP['ExpirationDate'].astype('datetime64[ns]'))
sourceUP['ExpirationDate'] = pd.to_datetime(sourceUP['ExpirationDate'].astype('datetime64[ns]'))
sourceUP['SummaryDate'] = pd.to_datetime(sourceUP['SummaryDate'].astype('datetime64[ns]'))
targetUP['SummaryDate'] = pd.to_datetime(targetUP['SummaryDate'].astype('datetime64[ns]'))



final_dfUP=pd.merge(sourceUP,targetUP,how='left',left_on=['pid', 'PolicyIssueDate', 'TransactionIssuedDate', 'EffectiveDate',
       'ExpirationDate', 'PolicyNumber', 'Insured', 'WrittenPremium',
       'DaysEarned', 'EarnedtoMonthEndWrittenPremium',
       'UnearnedWrittenPremium', 'TranType', 'Address1', 'City', 'State',
       'Zip', 'DerivedStatus', 'Company', 'AffiliateDivision', 'SummaryDate'],right_on=['pid', 'PolicyIssueDate', 'TransactionIssuedDate', 'EffectiveDate',
       'ExpirationDate', 'PolicyNumber', 'Insured', 'WrittenPremium',
       'DaysEarned', 'EarnedtoMonthEndWrittenPremium',
       'UnearnedWrittenPremium', 'TranType', 'Address1', 'City', 'State',
       'Zip', 'DerivedStatus', 'Company', 'AffiliateDivision', 'SummaryDate'], indicator=True)
                                                                                        
sourceUP=sourceUP.add_prefix('S_')
targetUP=targetUP.add_prefix('T_')

final_dfUP_outside=pd.merge(sourceUP,targetUP,how='left',left_on=['S_pid', 'S_PolicyIssueDate', 'S_TransactionIssuedDate',
       'S_EffectiveDate', 'S_ExpirationDate', 'S_PolicyNumber', 'S_Insured',
       'S_WrittenPremium', 'S_DaysEarned', 'S_EarnedtoMonthEndWrittenPremium',
       'S_UnearnedWrittenPremium', 'S_TranType', 'S_Address1', 'S_City',
       'S_State', 'S_Zip', 'S_DerivedStatus', 'S_Company',
       'S_AffiliateDivision', 'S_SummaryDate'],right_on=['T_pid', 'T_PolicyIssueDate',
       'T_TransactionIssuedDate', 'T_EffectiveDate', 'T_ExpirationDate','T_PolicyNumber',
       'T_Insured', 'T_WrittenPremium', 'T_DaysEarned',
       'T_EarnedtoMonthEndWrittenPremium', 'T_UnearnedWrittenPremium',
       'T_TranType', 'T_Address1', 'T_City', 'T_State', 'T_Zip',
       'T_DerivedStatus', 'T_Company', 'T_AffiliateDivision', 'T_SummaryDate'], indicator=True)

                                                         
is_right_only=final_dfUP_outside['_merge']!='both'
final_dfUP_outside = final_dfUP_outside[is_right_only]

##tWP
sourceWP=sourceWP.rename(columns={'PolicyID':'PolicyID', 'Tran ID':'TranID', ' StatusID':'StatusID','Policy Nbr':'PolicyNumber','New Rollover Ind Desc':'NewRolloverIndDesc','First Name':'FirstName', 'Last Name':'LastName','Total Written Premium':'TotalWrittenPremium', 
                                    'Fed Pol Fee':'FedPolFee', 'Reserve Fund':'ReserveFund',
                                    'HFIAA Surcharge':'HFIAASurcharge', 'NFIP Trans Code':'NFIPTransCode', 'NFIP Trans Type':'NFIPTransType', 
                                    'Date Issued':'DateIssued','Company':'Company', 'Agency':'Agency', 
                                    'Property Address':'PropertyAddress', 'Property City':'PropertyCity',
                                    'Property Zip':'PropertyZip', 'Property State':'PropertyState', 'Property County':'PropertyCounty', 'Producer Number':'ProducerNumber',
                                    'Occupancy Type':'OccupancyType', 'Policy Form':'PolicyForm', 'Building Description/LOB':'BuildingDescriptionLOB',
                                    'HFIAATransaction':'HFIAATransaction', 'Affiliate/Division':'AffiliateDivision', 'Policy Effective Date':'PolicyEffectiveDate'})
targetWP['DateIssued'] = pd.to_datetime(targetWP['DateIssued'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')
targetWP['PolicyEffectiveDate'] = pd.to_datetime(targetWP['PolicyEffectiveDate'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%#m/%#d/%Y')

targetWP['PolicyID'] = targetWP['PolicyID'].astype('float64')
sourceWP['PolicyID'] = sourceWP['PolicyID'].astype('float64')
targetWP['TranID'] = targetWP['TranID'].astype('float64')
sourceWP['TranID'] = sourceWP['TranID'].astype('float64')

targetWP['StatusID'] = targetWP['StatusID'].astype('float64')
targetWP['PolicyNumber'] = targetWP['PolicyNumber'].astype('float64')
sourceWP['PolicyNumber'] = sourceWP['PolicyNumber'].astype('float64')
targetWP['HFIAATransaction'] = targetWP['HFIAATransaction'].astype('float64')
targetWP['AffiliateDivision'] = targetWP['AffiliateDivision'].astype('float64')
targetWP= targetWP.replace('1/1/1900',np.nan)
targetWP['PolicyEffectiveDate'] = pd.to_datetime(targetWP['PolicyEffectiveDate'].astype('datetime64[ns]'))
sourceWP['PolicyEffectiveDate'] = pd.to_datetime(sourceWP['PolicyEffectiveDate'].astype('datetime64[ns]'))
targetWP['DateIssued'] = pd.to_datetime(targetWP['DateIssued'].astype('datetime64[ns]'))
sourceWP['DateIssued'] = pd.to_datetime(sourceWP['DateIssued'].astype('datetime64[ns]'))

final_dfWP=pd.merge(sourceWP,targetWP,how='left',left_on=['PolicyID', 'TranID', 'StatusID', 'PolicyNumber', 'NewRolloverIndDesc',
       'FirstName', 'LastName', 'TotalWrittenPremium', 'FedPolFee',
       'ReserveFund', 'HFIAASurcharge', 'NFIPTransCode', 'NFIPTransType',
       'DateIssued', 'Company', 'Agency', 'PropertyAddress', 'PropertyCity',
       'PropertyZip', 'PropertyState', 'PropertyCounty', 'ProducerNumber',
       'OccupancyType', 'PolicyForm', 'BuildingDescriptionLOB',
       'HFIAATransaction', 'AffiliateDivision', 'PolicyEffectiveDate'],right_on=['PolicyID', 'TranID', 'StatusID', 'PolicyNumber', 'NewRolloverIndDesc',
       'FirstName', 'LastName', 'TotalWrittenPremium', 'FedPolFee',
       'ReserveFund', 'HFIAASurcharge', 'NFIPTransCode', 'NFIPTransType',
       'DateIssued', 'Company', 'Agency', 'PropertyAddress', 'PropertyCity',
       'PropertyZip', 'PropertyState', 'PropertyCounty', 'ProducerNumber',
       'OccupancyType', 'PolicyForm', 'BuildingDescriptionLOB',
       'HFIAATransaction', 'AffiliateDivision', 'PolicyEffectiveDate'],indicator=True)
                                                                                 
sourceWP=sourceWP.add_prefix('S_')
targetWP=targetWP.add_prefix('T_')                                                                                 

                                                                                 
final_dfWP_outside=pd.merge(sourceWP,targetWP,how='outer',left_on=['S_PolicyID', 'S_TranID', 'S_StatusID', 'S_PolicyNumber',
       'S_NewRolloverIndDesc', 'S_FirstName', 'S_LastName',
       'S_TotalWrittenPremium', 'S_FedPolFee', 'S_ReserveFund',
       'S_HFIAASurcharge', 'S_NFIPTransCode', 'S_NFIPTransType',
       'S_DateIssued', 'S_Company', 'S_Agency', 'S_PropertyAddress',
       'S_PropertyCity', 'S_PropertyZip', 'S_PropertyState',
       'S_PropertyCounty', 'S_ProducerNumber', 'S_OccupancyType',
       'S_PolicyForm', 'S_BuildingDescriptionLOB', 'S_HFIAATransaction',
       'S_AffiliateDivision', 'S_PolicyEffectiveDate'],right_on=['T_PolicyID', 'T_TranID', 'T_StatusID', 'T_PolicyNumber',
       'T_NewRolloverIndDesc', 'T_FirstName', 'T_LastName',
       'T_TotalWrittenPremium', 'T_FedPolFee', 'T_ReserveFund',
       'T_HFIAASurcharge', 'T_NFIPTransCode', 'T_NFIPTransType',
       'T_DateIssued', 'T_Company', 'T_Agency', 'T_PropertyAddress',
       'T_PropertyCity', 'T_PropertyZip', 'T_PropertyState',
       'T_PropertyCounty', 'T_ProducerNumber', 'T_OccupancyType',
       'T_PolicyForm', 'T_BuildingDescriptionLOB', 'T_HFIAATransaction',
       'T_AffiliateDivision', 'T_PolicyEffectiveDate'],indicator=True)

is_right_only=final_dfWP_outside['_merge']!='both'
final_dfWP_outside = final_dfWP_outside[is_right_only]                                                                                
