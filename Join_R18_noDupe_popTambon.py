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
file_name='pop_tambon.csv'
dfPop=pd.read_csv(file_path+'\\sales_data\\'+file_name)
dfPop['key']=dfPop['p_name_t']+'_'+dfPop['a_name_t']+'_'+dfPop['t_name_t']
print(len(dfPop),' ==  Pop  ==== ',dfPop.head(10))

file_name='r18_pat.csv'
cvt={'Customer_Code':str, 'CustomerCatId':str }
df18=pd.read_csv(file_path+'\\sales_data\\'+file_name, converters=cvt)
df18['key']=df18['p_name_t']+'_'+df18['a_name_t']+'_'+df18['t_name_t']
print(len(df18),' ===   18   === ',df18.head(10))

###########################################################################################

dfMerge = pd.merge(df18, dfPop, how="left", on=["key"])


dfMerge.rename(columns={'SalesTeamCode':'SalesTeamCode_R18','SaleofficeName':'SaleofficeName_R18','Customer_Code':'Customer_Code_R18','CustomerName':'CustomerName_R18',
'CustomerCatId':'CustomerCatId_R18','Latitude':'Latitude_R18','Longitude':'Longitude_R18','WorkSubDistrict':'WorkSubDistrict_R18',
'WorkDistrict':'WorkDistrict_R18','WorkProvince':'WorkProvince_R18','p_name_t_x':'p_name_t_R18','a_name_t_x':'a_name_t_R18',
't_name_t_x':'t_name_t_R18','s_region_x':'s_region_R18','population':'population_tambon'},inplace=True)
print(len(dfMerge),' merge ==> ',dfMerge.head(10),' ----- ',dfMerge.columns)
dfMerge.to_csv(file_path+'\\output\\'+'merged_18_tambon.csv')





###****************************************************************
end_datetime = datetime.now()
print ('---Start---',start_datetime)
print('---complete---',end_datetime)
DIFFTIME = end_datetime - start_datetime 
DIFFTIMEMIN = DIFFTIME.total_seconds()
print('Time_use : ',round(DIFFTIMEMIN,2), ' Seconds')