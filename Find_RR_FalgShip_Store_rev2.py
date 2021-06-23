import pandas as pd
from datetime import datetime, date,  timedelta
import numpy as np
import os
from Text_PreProcessing import *
import pyodbc

start_datetime = datetime.now()
print (start_datetime,'execute')
todayStr=date.today().strftime('%Y-%m-%d')
nowStr=datetime.today().strftime('%Y-%m-%d %H:%M:%S')
print("TodayStr's date:", todayStr,' -- ',type(todayStr))
print("nowStr's date:", nowStr,' -- ',type(nowStr))


def AssignRRColumn(RR, RN):
    if(len(RR)>0 and len(RN)>0):
        return 'รุ่งเรือง'
    elif(len(RR)>0 and len(RN)==0):
        return 'รุ่งเรือง'
    elif(len(RR)==0 and len(RN)>0):
        return 'รุ่งอรุณ'
    else:
        return ''


file_path='C:\\Users\\70018928\\Documents\\Project2021\\Ad-Hoc\\UpdateFile\\Append_File\\'
file_name='merged_Sales_711_SoS_Store_Population_R18_PopTambon_MinMax_R18.csv'
cvt={'Customer_Code':str}
dfMerge=pd.read_csv(file_path+'\\sales_data\\'+file_name, converters=cvt)

dfMerge=Clean_CustomerId('Customer_Code', dfMerge)
print(len(dfMerge),' ==  Merge  ==== ',dfMerge.head(10))


ccList=list(dfMerge['Customer_Code'].unique())
print(len(ccList),' ===== ',ccList[:10])
dfCC=pd.DataFrame(ccList, columns=['Customer_Code'])
print(len(dfCC), ' ------- ',dfCC.head(10))

file_name='RR_group.xlsx'
cvt={'10K_Rungrueng_CustomerCode':str,'60K_Rungaroon_CustomerCode':str, '86_Flagship_Shopcode':str}
dfRR=pd.read_excel(file_path+'\\sales_data\\'+file_name, sheet_name='idgroup', converters=cvt)

dfRR=Clean_CustomerId('10K_Rungrueng_CustomerCode', dfRR)
dfRR=Clean_CustomerId('60K_Rungaroon_CustomerCode', dfRR)
dfRR=Clean_CustomerId('86_Flagship_Shopcode', dfRR)
print(len(dfRR),' ======= > ',dfRR.columns,' :: ',dfRR.head(10))

dfRRG=dfRR[['10K_Rungrueng_CustomerCode']].copy()
dfRRN=dfRR[['60K_Rungaroon_CustomerCode']].copy()
dfFLG=dfRR[['86_Flagship_Shopcode']].copy()

def ReplaceNanToBlank(x):
    if(int(x[:len(x)-3])==0):
        return ''
    else:
        return x

dfRRG['10K_Rungrueng_CustomerCode']=dfRRG.apply(lambda x: ReplaceNanToBlank(x['10K_Rungrueng_CustomerCode']), axis=1)
dfRRG=dfRRG[dfRRG['10K_Rungrueng_CustomerCode']!=''].copy().reset_index(drop=True)
print(len(dfRRG),'== after =RRG===',dfRRG.head(10))

dfRRN['60K_Rungaroon_CustomerCode']=dfRRN.apply(lambda x: ReplaceNanToBlank(x['60K_Rungaroon_CustomerCode']), axis=1)
dfRRN=dfRRN[dfRRN['60K_Rungaroon_CustomerCode']!=''].copy().reset_index(drop=True)
print(len(dfRRN),'== after =RRN===',dfRRN.head(10))

dfFLG['86_Flagship_Shopcode']=dfFLG.apply(lambda x: ReplaceNanToBlank(x['86_Flagship_Shopcode']), axis=1)
dfFLG=dfFLG[dfFLG['86_Flagship_Shopcode']!=''].copy().reset_index(drop=True)
print(len(dfFLG),'== after =FLG===',dfFLG.head(10))


def Find_RRG(x, dfRR):
    dfResult=dfRR[dfRR['10K_Rungrueng_CustomerCode']==x].copy()
    if(len(dfResult)>0):
        #print(len(dfResult), ' ----- ', dfResult.head(10), ' :: ',dfResult['10K_Rungrueng_CustomerCode'].values[0],' --- ',x)
        return 'Rungrueng'
    else:
        return ''

def Find_RRN(x, dfRR):
    dfResult=dfRR[dfRR['60K_Rungaroon_CustomerCode']==x].copy()
    if(len(dfResult)>0):
        #print(len(dfResult), ' ----- ', dfResult.head(10), ' :: ',dfResult['60K_Rungaroon_CustomerCode'].values[0])
        return 'Rungaroon'
    else:
        return ''

def Find_FlagShip(x, dfRR):
    dfResult=dfRR[dfRR['86_Flagship_Shopcode']==x].copy()
    if(len(dfResult)>0):
        #print(len(dfResult), ' ----- ', dfResult.head(10), ' :: ',dfResult['86_Flagship_Shopcode'].values[0])
        return 'Flagship'
    else:
        return ''



#dfCC=dfCC.head(100)
print('step :1 RRG')
dfCC['RRG']=dfCC.apply(lambda x:Find_RRG(x['Customer_Code'],dfRRG),axis=1)
print('step :2 RRN')
dfCC['RRN']=dfCC.apply(lambda x:Find_RRN(x['Customer_Code'],dfRRN),axis=1)
print('step :3 FLGS')
dfCC['FLGS']=dfCC.apply(lambda x:Find_FlagShip(x['Customer_Code'],dfFLG),axis=1)
print('step :4 RR_GRP')
dfCC['RR_GRP']=dfCC.apply(lambda x:AssignRRColumn(x['RRG'],x['RRN']),axis=1)
print('step :5 Output')
dfCC.to_csv(file_path+'\\output\\RR_GRP_Customer_Code.csv')


#dfRR_M.rename(columns={'10K_Rungrueng_CustomerCode':'Customer_Code'}, inplace=True)





#dfCC=dfRR_M.head(1000)

# mainDf=pd.merge(dfMerge, dfCC, how="left", on=["Customer_Code"])
# print(len(mainDf), ' == main ====  ',mainDf.head(10))
# #mainDf.to_excel(file_path+'\\output\\check_merge_RR.xlsx', sheet_name='Sheet_name_1')
# mainDf.to_csv(file_path+'\\output\\check_merge_RR.csv')


del dfCC, dfRR, dfMerge
###****************************************************************
end_datetime = datetime.now()
print ('---Start---',start_datetime)
print('---complete---',end_datetime)
DIFFTIME = end_datetime - start_datetime 
DIFFTIMEMIN = DIFFTIME.total_seconds()
print('Time_use : ',round(DIFFTIMEMIN,2), ' Seconds')