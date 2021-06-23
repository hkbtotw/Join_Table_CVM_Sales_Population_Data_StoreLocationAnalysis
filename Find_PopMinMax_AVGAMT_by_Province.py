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
file_name='merged_Sales_711_SoS_Store_R18Pop_R18_PopT_NoD.csv'
cvt={'Customer_Code':str}
dfMerge=pd.read_csv(file_path+'\\output\\'+file_name, converters=cvt)
print(len(dfMerge),' ==  Merge  ==== ',dfMerge.head(10))

dfMerge=Clean_CustomerId('Customer_Code', dfMerge)

dfMerge['Percent_Pop_Tambon']=dfMerge['population']/dfMerge['population_tambon']
dfMerge['Percent_Pop_Tambon'].replace({np.nan:0},inplace=True)

def RemoveFrontRearSpace(x):
    if(type(x)==str):
        return x.strip()
    else:
        return x


dfMerge['province']=dfMerge.apply(lambda x: RemoveFrontRearSpace(x['province']),axis=1)

print(len(dfMerge),' Merge ==> ',dfMerge['Percent_Pop_Tambon'].head(10), ' -----  ',dfMerge.columns)
#dfMerge.to_excel(file_path+'\\output\\check_pop_tambon.xlsx', sheet_name='Sheet_name_1')

provinceList=list(dfMerge['p_name_t_R18'].unique())
dfProvince=pd.DataFrame(provinceList, columns=['prv'])
dfProvince.to_excel(file_path+'\\output\\check_province.xlsx', sheet_name='Sheet_name_1')

mainDf=pd.DataFrame(columns=['Unnamed: 0', 'Customer_Code', 'Customer_Name', 'CustomerCatId', 'Jan',
       'Feb', 'Mar', 'Apr', 'May', 'Count_MONTH', 'TOTAL_5M', 'AVG_AMT',
       'PROVINCE_AVG', '>AVG', '%SALEinProvince', 'custm_name', 'province',
       'custm_lat', 'custm_lng', 'name_711', '711_lat', '711_lng', 'distance',
       'DBCreatedAt', 'SOS_CHANG_COLDBREW', 'SOS_CHANG_CC', 'SOS_LEO',
       'SOS_Signha', 'SOS_ThaiBev', 'SOS_Boonrawd',
       'SOS_DIFF_ThaiBev-Boonrawd', 'SOS_GREEN', 'CustomerName_x',
       'CustomerAddress_x', 'CustomerType_x', 'Column', 'SaleTeam',
       'SaleTeamHeadId', 'Latitude_60K', 'Longitude_60K', 'Unnamed: 0_x',
       'CustomerName_y', 'CustomerAddress_y', 'CustomerType_y', 'Latitude',
       'Longitude', 'p_name_t', 'a_name_t', 't_name_t', 's_region', 'hex_id',
       'population', 'Unnamed: 0_y', 'Unnamed: 0.1', 'SalesTeamCode_R18',
       'SaleofficeName_R18', 'CustomerName_R18', 'CustomerCatId_R18',
       'Latitude_R18', 'Longitude_R18', 'WorkSubDistrict_R18',
       'WorkDistrict_R18', 'WorkProvince_R18', 'p_name_t_R18', 'a_name_t_R18',
       't_name_t_R18', 's_region_R18', 'key', 'p_name_t_y', 'a_name_t_y',
       't_name_t_y', 's_region_y', 'population_tambon', 'Percent_Pop_Tambon',
       ])
count=0
for province in provinceList:
    count=count+1
    print(count,' ====== from ==== ',len(provinceList))
    #province='กรุงเทพมหานคร'
    dfDummy=dfMerge[dfMerge['p_name_t_R18']==province].copy().reset_index(drop=True)

    max_value =  dfDummy["AVG_AMT"].max()
    min_value =  dfDummy["AVG_AMT"].min()
    #print(' max: ',max_value, ' ,  min: ',min_value)
    dfDummy['AVG_AMT_MIN_byPrv']=min_value
    dfDummy['AVG_AMT_MAX_byPrv']=max_value

    max_value =  dfDummy["Percent_Pop_Tambon"].max()
    min_value =  dfDummy["Percent_Pop_Tambon"].min()
    #print(' max: ',max_value, ' ,  min: ',min_value)
    dfDummy['P_Pop_Tambon_Min_byPrv']=min_value
    dfDummy['P_Pop_Tambon_Max_byPrv']=max_value

    #print(len(dfDummy), ' ======== ',dfDummy.head(10),' === col : ',dfDummy.columns)

    mainDf=mainDf.append(dfDummy).reset_index(drop=True)
    del dfDummy




print(len(mainDf), ' === main ===== ',mainDf.head(10),' === col : ',mainDf.columns)
mainDf.to_excel(file_path+'\\output\\merged_Sales_711_SoS_Store_R18Pop_R18_PopT_MinMax_R18.xlsx', sheet_name='Sheet_name_1')
mainDf.to_csv(file_path+'\\output\\merged_Sales_711_SoS_Store_R18Pop_R18_PopT_MinMax_R18.csv')
del dfMerge,mainDf
###****************************************************************
end_datetime = datetime.now()
print ('---Start---',start_datetime)
print('---complete---',end_datetime)
DIFFTIME = end_datetime - start_datetime 
DIFFTIMEMIN = DIFFTIME.total_seconds()
print('Time_use : ',round(DIFFTIMEMIN,2), ' Seconds')