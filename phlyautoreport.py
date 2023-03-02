import pyodbc 
import pandas as pd 

EvaluationDate = str(20221231)
Year=int(EvaluationDate[0:4])
YearP=int(EvaluationDate[0:4])-1
PriorYearEnd = str(YearP) + '1231'

policies=('PHPR118135-J', 'PHPR118135-K','PHPR118135-L','PHPR118135-M','PHPR118135-N','PHPR118135-P','PHPR118135-Q','PHPR118135-R','PHPR118135-S','PHPR118135-T',
        'PHPR118135-U','PHPR118135-V','PHPK2352419','PHPR118136-J','PHPR118136-K','PHPR118136-L','PHPR118136-M','PHPR118136-N','PHPR118136-P','PHPR118136-Q',
        'PHPR118136-R','PHPR118136-S','PHPR118136-T','PHPR118136-U','PHPR118136-V','PHPK118136-W','PHPK2345053','PHPR126507-I','PHPR126507-J','PHPR126507-K',
        'PHPR126507-L','PHPR126507-M','PHPR126507-P','PHPR126507-Q','PHPR126507-R','PHPR126507-S','PHPR126507-T','PHPR126507-U','PHPK2352428')

report=pd.DataFrame()
report['Policies']=policies
report['Policies']=report.Policies.astype('str')


conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=P00NORSQL049;'
                      'Database=PHLYWarehouse;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
Gross_Premiumsql='''SELECT policynumber as Policies, sum(earnedpremiumamount) FROM FactPremiumAccountingPeriodSnapshot where AccountingPeriodKey>? and AccountingPeriodKey<=? group by policynumber order by 1'''
Gross_Premium=pd.read_sql_query(sql=Gross_Premiumsql, params=[EvaluationDate,EvaluationDate] ,con=conn )
Net_Premiumsql='''Select policynumber, sum(ep) as NetPremium from (select policynumber, sum(earnedpremiumamount) as EP from PHLYWarehouse..FactPremiumAccountingPeriodSnapshot f where AccountingPeriodKey>20211231 and AccountingPeriodKey<=20220331 group by policynumber UNION ALL select policynumber, sum(-1 *CededEarnedPremiumAmount) as EP from PHLYWarehouse..FactCededPremiumDetail f join PHLYWarehouse..DimPolicy dc on f.policykey=dc.PolicyKey where AccountingPeriodKey>? and AccountingPeriodKey<=? group by policynumber)a group by policynumber order by 1'''
Net_Premium =pd.read_sql_query(sql=Net_Premiumsql, params=[EvaluationDate,EvaluationDate] ,con=conn )
Case_and_Paid_Losssql='''select dp.policynumber as Policies,AccountingPeriodKey, dc.lossdate, cededindicator, sum([Case Incurred Loss and ALAE]) as CaseIncurredLossandALAE from PHLYWarehouse..FactClaimAccountingPeriodSnapshot f join phlywarehouse..dimclaim dc on f.claimnumber=dc.claimnumber and dc.iscurrentrow=1 join phlywarehouse..dimpolicy dp on f.policykey=dp.policykey where AccountingPeriodKey>? and AccountingPeriodKey<=? group by dp.policynumber,AccountingPeriodKey, dc.lossdate, cededindicator'''
Case_and_Paid_Loss=pd.read_sql_query(sql=Case_and_Paid_Losssql, params=[EvaluationDate,EvaluationDate] ,con=conn)
Case_and_Paid_Loss=Case_and_Paid_Loss[Case_and_Paid_Loss.cededindicator=='N']
IBNRsql='''select policynumber,CededIndicator,EvaluationDateKey,AccidentYear,sum(IBNRLossAmount),sum(IBNRDCCAmount),sum(IBNRANOAmount) from PHLYWarehouse..FactLERExCat_NetBased f join phlywarehouse..dimpolicy dp on f.policykey=dp.policykey group by policynumber,CededIndicator,EvaluationDateKey,AccidentYear'''
IBNR=pd.read_sql_query(sql=IBNRsql, params=[EvaluationDate,EvaluationDate] ,con=conn)

Gross_Premium['Policies']=Gross_Premium.Policies.astype('str')
Case_and_Paid_Loss['AccountingPeriodKey']=Case_and_Paid_Loss.AccountingPeriodKey.astype('str')
Case_and_Paid_Loss['lossdate']=Case_and_Paid_Loss.lossdate.astype('str')
Gross_Premium_fltr= Gross_Premium[Gross_Premium['Policies'].isin(policies)]
Net_Premium= Net_Premium[Net_Premium['policynumber'].isin(policies)]
Case_and_Paid_Loss_fltr= Case_and_Paid_Loss[Case_and_Paid_Loss['Policies'].isin(policies)]
Case_and_Paid_Loss_fltr['AccountingPeriodKey']= Case_and_Paid_Loss_fltr['AccountingPeriodKey'].str[:4]
Case_and_Paid_Loss_fltr['lossdate']= Case_and_Paid_Loss_fltr['lossdate'].str[:4]
Case_and_Paid_Loss['AccountingPeriodKey']=Case_and_Paid_Loss.AccountingPeriodKey.astype('int')
Case_and_Paid_Loss_fltr_AY=Case_and_Paid_Loss_fltr
Case_and_Paid_Loss_fltr_AY=(Case_and_Paid_Loss_fltr_AY[Case_and_Paid_Loss_fltr_AY.AccountingPeriodKey==Year])
Case_and_Paid_Loss_fltr_AY=Case_and_Paid_Loss_fltr.groupby('Policies')['CaseIncurredLossandALAE'].sum()

report=pd.merge(report,Gross_Premium,how='left',left_on=['Policies'],right_on=['Policies'])
report=pd.merge(report,Case_and_Paid_Loss_fltr_AY,how='left',left_on=['Policies'],right_on=['Policies'])
report=report.loc[:,['Policies', '_x','_y']]


