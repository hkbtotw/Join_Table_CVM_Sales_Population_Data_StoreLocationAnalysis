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


file_path='C:\\Users\\70018928\\Documents\\Project2021\\Ad-Hoc\\UpdateFile\\Append_File\\'
file_name='merged_Sales_711_SoS_Store_Population_R18_PopTambon_MinMax.csv'
cvt={'Customer_Code':str}
dfMerge=pd.read_csv(file_path+'\\sales_data\\'+file_name, converters=cvt)

dfMerge=Clean_CustomerId('Customer_Code', dfMerge)
print(len(dfMerge),' ==  Merge  ==== ',dfMerge.head(10))


file_name='assign_cc.csv'
cvt={'Customer_Code':str}
dfCC=pd.read_csv(file_path+'\\output\\'+file_name, converters=cvt)

dfCC=Clean_CustomerId('Customer_Code', dfCC)
print(len(dfCC),' ==  CC  ==== ',dfCC.head(10))


def Assign_RR_GRP(x, dfCC):
    dfDummy=dfCC[dfCC['Customer_Code']==x].copy()
    if(len(dfDummy)>0):
        return dfDummy['RR_GRP'].values[0]
    else:
        return ''


def Assign_FLGS(x, dfCC):
    dfDummy=dfCC[dfCC['Customer_Code']==x].copy()
    if(len(dfDummy)>0):
        return dfDummy['FLGS'].values[0]
    else:
        return ''

dfMerge['RR_GRP']=dfMerge.apply(lambda x: Assign_RR_GRP(x['Customer_Code'],dfCC),axis=1)
dfMerge['Flagship_shop']=dfMerge.apply(lambda x: Assign_FLGS(x['Customer_Code'],dfCC),axis=1)

print(len(dfMerge), ' --  Merge --  ',dfMerge.head(10))
dfMerge.to_excel(file_path+'\\output\\merged_Sales_711_SoS_Store_Population_R18_PopTambon_MinMax_RR_F.xlsx', sheet_name='Sheet_name_1')
dfMerge.to_csv(file_path+'\\output\\merged_Sales_711_SoS_Store_Population_R18_PopTambon_MinMax_RR_F.csv')

###****************************************************************
end_datetime = datetime.now()
print ('---Start---',start_datetime)
print('---complete---',end_datetime)
DIFFTIME = end_datetime - start_datetime 
DIFFTIMEMIN = DIFFTIME.total_seconds()
print('Time_use : ',round(DIFFTIMEMIN,2), ' Seconds')