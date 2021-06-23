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
file_name='df_main2.csv'    # score file by 2021-06-17
cvt={'Customer_Code':str}
dfIn=pd.read_csv(file_path+'\\sales_data\\'+file_name, converters=cvt)

dfIn=Clean_CustomerId('Customer_Code', dfIn)
print(len(dfIn),' ------- rawdata score ======= > ',dfIn.head(10),' ======= ',dfIn.columns)

file_name='province_score.xlsx'
dfScore=pd.read_excel(file_path+'\\sales_data\\'+file_name, sheet_name='Sheet1', converters=cvt)
print(len(dfScore),' ======= > ',dfScore.columns)


provinceList=list(dfIn['p_name_t_R18'].unique())
print('  province : ',len(provinceList))
#dfProvince=pd.DataFrame(provinceList, columns=['prov'])
# dfProvince.to_excel(file_path+'\\output\\province.xlsx')

mainDf=pd.DataFrame(columns=['Customer_Code', 'CustomerName_R18', 'RR_GRP',
       'CustomerCatId_R18', 'SalesTeamCode_R18', 'SaleofficeName_R18',
       'WorkSubDistrict_R18', 'WorkDistrict_R18', 'WorkProvince_R18',
       's_region_R18', 'p_name_t_R18', 'a_name_t_R18', 't_name_t_R18',
       'Latitude_R18', 'Longitude_R18', 'SOS_ThaiBev', 'SOS_Boonrawd',
       'SOS_GREEN', 'TOTAL_5M', 'AVG_AMT', 'AVG_AMT_MIN_byPrv',
       'AVG_AMT_MAX_byPrv', 'population', 'population_tambon',
       'P_Pop_Tambon_Min_byPrv', 'P_Pop_Tambon_Max_byPrv', 'distance',
       '%pop_cust_tambon', 'P_SCORE', 'P_SCORE_W', 'D_SCORE', 'D_SCORE_W',
       'flg_sale', 'S_SCORE', 'S_SCORE_W', 'TotalScore','Order_Prv'])

for province in provinceList:  #[:2]:
    dfDummy=dfScore[dfScore['prov']==province].copy().reset_index(drop=True)
    prov_score=dfDummy['Score'].values[0]
    print(province, ' ------- score ------ ',prov_score)
    dfIn_2=dfIn[dfIn['p_name_t_R18']==province].copy().reset_index(drop=True)
    dfDummy=dfIn_2[dfIn_2['TotalScore']>=prov_score].copy().reset_index(drop=True)
    dfDummy=dfDummy[(dfDummy['RR_GRP']=='รุ่งอรุณ') | (dfDummy['RR_GRP']=='รุ่งเรือง') ].copy().reset_index(drop=True)
    dfDummy=dfDummy[dfDummy['flg_sale']==1].copy().reset_index(drop=True)
    dfDummy=dfDummy.sort_values(by='TotalScore', ascending=False).reset_index(drop=True)
    dfDummy['Order_Prv'] = dfDummy.index
    dfDummy['Order_Prv'] =dfDummy['Order_Prv']+1
    dfDummy.drop("Unnamed: 0", axis=1, inplace=True)
    print(len(dfDummy),' ====== >',dfDummy)
    
    mainDf=mainDf.append(dfDummy).reset_index(drop=True)


mainDf=mainDf.sort_values(by='TotalScore', ascending=False).reset_index(drop=True)
mainDf['Order_Country'] = mainDf.index
mainDf['Order_Country'] =mainDf['Order_Country']+1
print(len(mainDf),' == main ==== >',mainDf)

saleList=list(mainDf['SaleofficeName_R18'].unique())

filterDf=pd.DataFrame(columns=['Customer_Code', 'CustomerName_R18', 'RR_GRP', 'CustomerCatId_R18',
       'SalesTeamCode_R18', 'SaleofficeName_R18', 'WorkSubDistrict_R18',
       'WorkDistrict_R18', 'WorkProvince_R18', 's_region_R18', 'p_name_t_R18',
       'a_name_t_R18', 't_name_t_R18', 'Latitude_R18', 'Longitude_R18',
       'SOS_ThaiBev', 'SOS_Boonrawd', 'SOS_GREEN', 'TOTAL_5M', 'AVG_AMT',
       'AVG_AMT_MIN_byPrv', 'AVG_AMT_MAX_byPrv', 'population',
       'population_tambon', 'P_Pop_Tambon_Min_byPrv', 'P_Pop_Tambon_Max_byPrv',
       'distance', '%pop_cust_tambon', 'P_SCORE', 'P_SCORE_W', 'D_SCORE',
       'D_SCORE_W', 'flg_sale', 'S_SCORE', 'S_SCORE_W', 'TotalScore',
       'Order_Prv', 'Order_Country', 'Order_salesOffice_Country'])

for n in saleList:  #[:2]:
    dfDummy=mainDf[mainDf['SaleofficeName_R18']==n].copy().reset_index(drop=True)
    dfDummy=dfDummy.sort_values(by='TotalScore', ascending=False).reset_index(drop=True)
    dfDummy['Order_salesOffice_Country'] = dfDummy.index
    dfDummy['Order_salesOffice_Country'] =dfDummy['Order_salesOffice_Country']+1
    print(len(dfDummy),' ====== >',dfDummy, ' ----- ',dfDummy.columns)
    filterDf=filterDf.append(dfDummy).reset_index(drop=True)




filterDf.to_excel(file_path+'\\output\\'+'selected_customer_by_provincial_score_Filtered_020.xlsx', sheet_name='Sheet_name_1')
filterDf.to_csv(file_path+'\\output\\'+'selected_customer_by_provincial_score_Filtered_020.csv')



del dfDummy, prov_score, dfIn, mainDf, dfIn_2, filterDf

###****************************************************************
end_datetime = datetime.now()
print ('---Start---',start_datetime)
print('---complete---',end_datetime)
DIFFTIME = end_datetime - start_datetime 
DIFFTIMEMIN = DIFFTIME.total_seconds()
print('Time_use : ',round(DIFFTIMEMIN,2), ' Seconds')
