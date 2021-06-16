import pandas as pd
import os
from Text_PreProcessing import *



file_path='C:\\Users\\70018928\\Documents\\Project2021\\Ad-Hoc\\UpdateFile\\Append_File\\'

files = os.listdir(file_path+'\\data\\')

cvt={'SalesTeamCode':str,'CustomerId':str,'CustomerCode':str,'SalesTeamId':str,'SOCustomerId':str,'CustomerCatId':str,'CustomerSubCatId':str,
'BillSubDistrictCode':str,'BillSubDistrict':str,'BillDistrictCode':str,'BillProvinceCode':str,
'BillZipCode':str,'WorkSubDistrictCode':str,'WorkDistrictCode':str,'WorkProvinceCode':str}

mainDf=pd.DataFrame(columns=[ 'RegionId', 'ZoneId', 'SalesTeamCode', 'SaleofficeName', 'CustomerId',
       'CustomerCode', 'SalesTeamId', 'SOCustomerId', 'CustomerName',
       'CustomerCatId', 'CustomerSubCatId', 'BranchVatNo', 'CustomerShortName',
       'ActiveFlag', 'Latitude', 'Longitude', 'TaxNo', 'BillCompanyName',
       'BillNo', 'BillMoo', 'BillVillage', 'BillBuilding', 'BillFloor',
       'BillRoom', 'BillSoi', 'BillRoad', 'BillSubDistrictCode',
       'BillSubDistrict', 'BillDistrictCode', 'BillDistrict',
       'BillProvinceCode', 'BillProvince', 'BillZipCode', 'WorkNo', 'WorkMoo',
       'WorkVillage', 'WorkBuilding', 'WorkFloor', 'WorkRoom', 'WorkSoi',
       'WorkRoad', 'WorkSubDistrictCode', 'WorkSubDistrict',
       'WorkDistrictCode', 'WorkDistrict', 'WorkProvinceCode', 'WorkProvince',
       'WorkZipCode', 'WorkTelephone', 'WorkFax', 'CreatedDate',
       'CreatedByUserId', 'CreatedByUserName', 'UpdatedDate',
       'UpdatedByUserId', 'UpdatedByUserName', 'Status'  ])
for n in files:
    dfIn=pd.read_csv(file_path+'\\data\\'+n, converters=cvt)
    print(len(dfIn),' ======> ',dfIn.head(10), '===>',dfIn.columns)
    mainDf=mainDf.append(dfIn).reset_index(drop=True)

mainDf.rename(columns={'CustomerCode':'Customer_Code'}, inplace=True)

mainDf=Clean_CustomerId('Customer_Code', mainDf)

mainDf.to_csv(file_path+'\\output\\R18.csv')