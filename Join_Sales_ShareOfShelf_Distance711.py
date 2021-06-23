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


def Read_Ext711_and_DIM_LOC_CVM_CUST_NEW(province):
    print('------------- Start ReadDB -------------')    
    conn = pyodbc.connect('Driver={SQL Server};'
                            'Server=SBNDCBIPBST02;'
                            'Database=TSR_ADHOC;'
                        'Trusted_Connection=yes;')

    cursor = conn.cursor()
    if(len(province)>0):
        #- Select data  all records from the table
        sql="""
            SELECT [custm_code]
        ,[custm_name]
        ,[province]
        ,[custm_lat]
        ,[custm_lng]
        ,[name_711]
        ,[711_lat]
        ,[711_lng]
        ,[distance]
        ,[DBCreatedAt]
            FROM [TSR_ADHOC].[dbo].[Ext711_and_DIM_LOC_CVM_CUST_NEW]
            where province=N'"""+str(province)+"""'

        """
    else:
        sql="""
            SELECT [custm_code]
        ,[custm_name]
        ,[province]
        ,[custm_lat]
        ,[custm_lng]
        ,[name_711]
        ,[711_lat]
        ,[711_lng]
        ,[distance]
        ,[DBCreatedAt]
            FROM [TSR_ADHOC].[dbo].[Ext711_and_DIM_LOC_CVM_CUST_NEW]         

        """

    
    dfout=pd.read_sql(sql,conn)
    
    #print(len(dfout.columns),' :: ',dfout.columns)
    #print(dfout)    
    del conn, cursor, sql
    print(' --------- Reading End -------------')
    return dfout

####################### Store Sales Data #############################################################
############# from Tha, Local/ xlsx : \sales_data\cvm_sale_all_202101-202105_cvmetl.xlsx  
######################################################################################################

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

################  Store distance from clostest 711   #####################################################
###### from Sandbox 2 = \project2021\CVM_Location_Analysis\CVM_Store_Location_Summary_rev6.py
##### data - database : dbo.Ext711_and_DIM_LOC_CVM_CUST_NEW
##########################################################################################################
df711=Read_Ext711_and_DIM_LOC_CVM_CUST_NEW('')
print(len(df711),' 711 ==> ',df711['custm_code'].head(10), ' -----  ',df711.columns)
df711.rename(columns={'custm_code':'Customer_Code'}, inplace=True)

df711=Clean_CustomerId('Customer_Code', df711)
print(len(df711),' 711 Add 12 digits ==> ',df711['Customer_Code'].head(10), ' -----  ',df711.columns)
###########################################################################################################
dfMerge = pd.merge(dfIn_2, df711, how="outer", on=["Customer_Code"])
print(len(dfMerge),' merge ==> ',dfMerge['Customer_Code'].head(10),' ----- ',dfMerge.columns)
dfMerge.to_csv(file_path+'\\output\\'+'merged_Sales_711.csv')
#dfMerge.to_excel(file_path+'\\output\\'+'merged_Sales_711.xlsx',sheet_name='Sheet_name_1')


del dfIn_2, df711


########################## Share of Shelf ###################################################################
####### from Tha, Local xlsx  : \sales_Data\Beer5sku_M3-5_2021_all_shareofshelf.xlsx 
############################################################################################################
file_name='Beer5sku_M3-5_2021_all_shareofshelf.xlsx'
cvt={'ShopID':str}
dfSoS=pd.read_excel(file_path+'\\sales_data\\'+file_name, sheet_name='SV', converters=cvt)
print(len(dfSoS),' ======= > ',dfSoS.columns)
includeList=['ShopID','SOS_CHANG_COLDBREW','SOS_CHANG_CC','SOS_LEO','SOS_Signha','SOS_ThaiBev','SOS_Boonrawd','SOS_DIFF_ThaiBev-Boonrawd','SOS_GREEN']
dfSoS_2=dfSoS[includeList].copy()
del dfSoS
dfSoS_2.rename(columns={'ShopID':'Customer_Code'},inplace=True)

dfSoS_2=Clean_CustomerId('Customer_Code', dfSoS_2)
print(len(dfSoS_2),' SoS 12 digits ==> ',dfSoS_2['Customer_Code'].head(10), ' -----  ',dfSoS_2.columns)
#########################################################################################################

dfMerge_2 = pd.merge(dfMerge, dfSoS_2, how="outer", on=["Customer_Code"])
print(len(dfMerge_2),' merge 2 ==> ',dfMerge_2['Customer_Code'].head(10),' ----- ',dfMerge_2.columns)
dfMerge_2.to_csv(file_path+'\\output\\'+'merged_Sales_711_SoS.csv')


del dfSoS_2, dfMerge
######################## รายชื่อร้านค้าดวงดาวทั้งหมด ################################################################################
########## from Tha, local xlsx, \sales_data\รายชื่อร้านค้าดวงดาวทั้งหมด (59,961 ร้านค้า).xlsx
############################################################################################################################
file_name='รายชื่อร้านค้าดวงดาวทั้งหมด (59,961 ร้านค้า).xlsx'
cvt={'CustomerCode':str}
dfStore=pd.read_excel(file_path+'\\sales_data\\'+file_name, sheet_name='Sheet1', converters=cvt)
print(len(dfStore),' ======= > ',dfStore.columns)
includeList=['CustomerCode','CustomerName','CustomerAddress','CustomerType','Column','SaleTeam','SaleTeamHeadId','Latitude_60K','Longitude_60K']
dfStore_2=dfStore[includeList].copy()
del dfStore
dfStore_2.rename(columns={'CustomerCode':'Customer_Code'},inplace=True)

dfStore_2=Clean_CustomerId('Customer_Code', dfStore_2)
print(len(dfStore_2),' Store 12 digits ==> ',dfStore_2['Customer_Code'].head(10), ' -----  ',dfStore_2.columns)

####################################################################################################
dfMerge_3 = pd.merge(dfMerge_2, dfStore_2, how="outer", on=["Customer_Code"])
print(len(dfMerge_3),' merge 3 ==> ',dfMerge_3['Customer_Code'].head(10),' ----- ',dfMerge_3.columns)
dfMerge_3.to_csv(file_path+'\\output\\'+'merged_Sales_711_SoS_Store.csv')
del dfStore_2, dfMerge_2

############################  Population on h3 level 8 Grid (0.7 km2) ################################
######  Copy \sales_data\maindf_population_by_province_PAT_R18.csv from sandbox1, \project2021\experiment\find_population_by_location\
######  Output generated by, On sandbox 1, script  Search_population_by_location_rev3.py
######################################################################################################
file_name='maindf_population_by_province_PAT_R18.csv'   #############################  R18's Lat Lng based
cvt={'Customer_Code':str}
dfPop=pd.read_csv(file_path+'\\sales_data\\'+file_name, converters=cvt)
dfPop.rename(columns={'CustomerCode':'Customer_Code'},inplace=True)
print(len(dfPop),' Population ======= > ',dfPop.columns)

dfPop=Clean_CustomerId('Customer_Code', dfPop)
print(len(dfPop),' Pop 12 digits ==> ',dfPop['Customer_Code'].head(10), ' -----  ',dfPop.columns)
####################################################################################################
dfMerge_4 = pd.merge(dfMerge_3, dfPop, how="outer", on=["Customer_Code"])
print(len(dfMerge_4),' merge 4 ==> ',dfMerge_4['Customer_Code'].head(10),' ----- ',dfMerge_4.columns)
del dfPop, dfMerge_3
############ population by tambon ##########################################################################
#### 1.Use input: R18.csv => r18_pat.csv  by Local:  \Project2021\Ad-Hoc\UpdateFile\Append_File\R18_Get_PAT.py  (toget p_name_t, a_name_t, t_name_t)
#### 2.use input : (from Tha, population by subdistrict grouped by data in [dbo].[H3_Grid_Lv8_Province_PAT] ) \sales_data\pop_tambon.csv + r18_pat.csv
####                                     => merged_18_tambon.csv by Local: \Project2021\Ad-Hoc\UpdateFile\Append_File\Join_R18_noDupe_popTambon.py
#############################################################################################################
file_name='merged_18_tambon.csv'
cvt={'Customer_Code_R18':str}
dfTP=pd.read_csv(file_path+'\\sales_data\\'+file_name, converters=cvt)
print(len(dfTP),' ==  TP  ==== ',dfTP.head(10))

dfTP=Clean_CustomerId('Customer_Code_R18', dfTP)
dfTP.rename(columns={'Customer_Code_R18':'Customer_Code'}, inplace=True)
print(len(dfTP),' TP 12 digits ==> ',dfTP['Customer_Code'].head(10), ' -----  ',dfTP.columns)

dfMerge_5 = pd.merge(dfMerge_4, dfTP, how="outer", on=["Customer_Code"])
print(len(dfMerge_5),' merge 5 ==> ',dfMerge_5['Customer_Code'].head(10),' ----- ',dfMerge_5.columns)
del dfTP, dfMerge_4

############## Remove duplicates   ######################################################################
### Duplicates of customer code which might come from the merging operations
########################################################################################################

dfMerge_5.to_csv(file_path+'\\output\\'+'merged_Sales_711_SoS_Store_Population_R18_PopTambon_brefore_DupeRemoval.csv')

mainDf=dfMerge_5.drop_duplicates(subset=['Customer_Code'], keep='first')
del dfMerge_5
#######################################################################################################

mainDf.to_csv(file_path+'\\output\\'+'merged_Sales_711_SoS_Store_R18Pop_R18_PopT_NoD.csv')
mainDf.to_excel(file_path+'\\output\\'+'merged_Sales_711_SoS_Store_R18Pop_R18_PopT_NoD.xlsx', sheet_name='Sheet_name_1')



del mainDf
###****************************************************************
end_datetime = datetime.now()
print ('---Start---',start_datetime)
print('---complete---',end_datetime)
DIFFTIME = end_datetime - start_datetime 
DIFFTIMEMIN = DIFFTIME.total_seconds()
print('Time_use : ',round(DIFFTIMEMIN,2), ' Seconds')