import pandas as pd
from datetime import datetime, date,  timedelta
import os
from csv_join_tambon import *

file_path='C:\\Users\\70018928\\Documents\\Project2021\\Ad-Hoc\\UpdateFile\\Append_File\\'
file_name='R18.csv'
cvt={'Customer_Code':str, 'CustomerId':str}
dfIn=pd.read_csv(file_path+'\\output\\'+file_name, converters=cvt)

print(len(dfIn),' ======= ',dfIn.head(10), ' ----  ',dfIn.columns)

dfIn['Latitude'].replace({'กรุงเทพมหานคร':0},inplace=True)

dfIn_2=Reverse_GeoCoding(dfIn)
del dfIn
print(len(dfIn_2),' === after==== ',dfIn_2.head(10),' ------ ',dfIn_2.columns)

includeList=['SalesTeamCode','SaleofficeName','Customer_Code','CustomerName','CustomerCatId','Latitude','Longitude',
'WorkSubDistrict','WorkDistrict','WorkProvince', 'p_name_t', 
       'a_name_t',  't_name_t',  's_region']

dfIn_3=dfIn_2[includeList].copy()
print(len(dfIn_3),' === 3 ==== ',dfIn_3.head(10),' ------ ',dfIn_3.columns)
file_name='r18_pat.csv'
dfIn_3.to_csv(file_path+'\\output\\'+file_name)
file_name='r18_pat.xlsx'
dfIn_3.to_excel(file_path+'\\output\\'+file_name, sheet_name='Sheet_name_1')