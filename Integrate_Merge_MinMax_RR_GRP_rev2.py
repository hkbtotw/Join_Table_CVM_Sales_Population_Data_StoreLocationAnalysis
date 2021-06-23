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
file_name='merged_Sales_711_SoS_Store_R18Pop_R18_PopT_MinMax_R18.csv'
cvt={'Customer_Code':str}
dfMerge=pd.read_csv(file_path+'\\output\\'+file_name, converters=cvt)

dfMerge=Clean_CustomerId('Customer_Code', dfMerge)
print(len(dfMerge),' ==  Merge  ==== ',dfMerge.head(10))


file_name='RR_GRP_Customer_Code.csv'
cvt={'Customer_Code':str}
dfCC=pd.read_csv(file_path+'\\output\\'+file_name, converters=cvt)

dfCC=Clean_CustomerId('Customer_Code', dfCC)
print(len(dfCC),' ==  CC  ==== ',dfCC.head(10))

mainDf=pd.merge(dfMerge, dfCC, how="left", on=["Customer_Code"])

print(len(mainDf), ' --  mainDf --  ',mainDf.head(10))
mainDf.to_excel(file_path+'\\output\\merged_Sales_711_SoS_Store_R18Pop_R18_PopT_MinMax_R18_RRGRP.xlsx', sheet_name='Sheet_name_1')
mainDf.to_csv(file_path+'\\output\\merged_Sales_711_SoS_Store_R18Pop_R18_PopT_MinMax_R18_RRGRP.csv')

###****************************************************************
end_datetime = datetime.now()
print ('---Start---',start_datetime)
print('---complete---',end_datetime)
DIFFTIME = end_datetime - start_datetime 
DIFFTIMEMIN = DIFFTIME.total_seconds()
print('Time_use : ',round(DIFFTIMEMIN,2), ' Seconds')