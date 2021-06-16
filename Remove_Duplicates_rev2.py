import pandas as pd
from datetime import datetime, date,  timedelta
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
file_name='merged_Sales_711_SoS_Store_Population_2.csv'
cvt={'Customer_Code':str}
dfIn=pd.read_csv(file_path+'\\output\\'+file_name, converters=cvt)

print(len(dfIn), ' ------- ',dfIn.head(10),' ----  ',dfIn.columns)

mainDf=dfIn.drop_duplicates(subset=['Customer_Code'], keep='first')

print('**************************************************')
print(len(mainDf), '== after drop  == ',mainDf)
file_name='merged_Sales_711_SoS_Store_Population_2_noDupe.csv'
mainDf.to_csv(file_path+'\\output\\'+file_name)
# file_name='merged_Sales_711_SoS_Store_Population_2_noDupe.xlsx'
# mainDf.to_excel(file_path+'\\output\\'+file_name, sheet_name='Sheet_name_1' )
###****************************************************************
end_datetime = datetime.now()
print ('---Start---',start_datetime)
print('---complete---',end_datetime)
DIFFTIME = end_datetime - start_datetime 
DIFFTIMEMIN = DIFFTIME.total_seconds()
print('Time_use : ',round(DIFFTIMEMIN,2), ' Seconds')