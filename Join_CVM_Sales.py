import pandas as pd
import os
from Text_PreProcessing import *



file_path='C:\\Users\\70018928\\Documents\\Project2021\\Ad-Hoc\\UpdateFile\\Append_File\\'
file_name='cvm_sale_all_202101-202105_cvmetl.xlsx'

cvt={'Customer_Code':str,'CustomerCatId':str}
dfIn=pd.read_excel(file_path+'\\sales_data\\'+file_name, sheet_name='data', converters=cvt)
print(len(dfIn),' ======= > ',dfIn.columns)
print(' check before ==> ',dfIn['Customer_Code'].head(10))

dfIn=Clean_CustomerId('Customer_Code', dfIn)

print(len(dfIn),' Sales ==> ',dfIn['Customer_Code'].head(10), ' -----  ',dfIn.columns)
#dfIn.to_csv(file_path+'\\output\\sale_data.csv')
includeList=['Customer_Code','Customer_Name','CustomerCatId','Jan','Feb','Mar','Apr','May','Count_MONTH','TOTAL_5M','AVG_AMT','PROVINCE_AVG','>AVG','%SALEinProvince']
dfIn_2=dfIn[includeList].copy()
print(len(dfIn_2),' Sales 2 ==> ',dfIn_2['Customer_Code'].head(10), ' -----  ',dfIn_2.columns)
del dfIn

dfin2List=list(dfIn_2['Customer_Code'].unique())
print(len(set(dfin2List)),' --in2---  ',len(dfIn_2))


###########################################################################################
# def intersection(lst1, lst2):
#     lst3 = [value for value in lst1 if value in lst2]
#     return lst3

# smallList=list(set(dfIn_2['Customer_Code']))
# allList=list(dfIn_2['Customer_Code'])

# resultList=intersection(smallList, allList)
# print(len(smallList),' ===> ',len(allList))
# print(' ==> ', len(resultList))

# main_list = [item for item in smallList if item not in resultList]
# print(' small=> ', len(main_list))


# main_list = [item for item in allList if item not in resultList]
# print(' all==> ', len(main_list))
#################################################################################################

file_name='R18.csv'
cvt={'Customer_Code':str}
dfR=pd.read_csv(file_path+'\\output\\'+file_name, converters=cvt)
print(len(dfR),' R ==> ',dfR['Customer_Code'].head(10),' ----- ',dfR.columns)
includeList=['RegionId','ZoneId','SalesTeamCode','SaleofficeName','CustomerId','Customer_Code','CustomerName','CustomerCatId','CustomerSubCatId',
'ActiveFlag','Latitude','Longitude','WorkSubDistrict','WorkDistrict','WorkProvince','WorkZipCode']

dfR_2=dfR[includeList].copy()
print(len(dfR_2),' R 2 ==> ',dfR_2['Customer_Code'].head(10),' ----- ',dfR_2.columns)

dfr2List=list(dfR_2['Customer_Code'].unique())
print(len(set(dfr2List)),' --R2---  ',len(dfR_2))
del dfR

dfMerge = pd.merge(dfR_2, dfIn_2, how="left", on=["Customer_Code"])
print(len(dfMerge),' merge ==> ',dfMerge['Customer_Code'].head(10),' ----- ',dfMerge.columns)
del dfIn_2, dfR_2

#dfMerge.to_csv(file_path+'\\output\\'+'merged.csv')

mergeList=list(dfMerge['Customer_Code'].unique())
print(len(set(mergeList)),' -----  ',len(mergeList))
