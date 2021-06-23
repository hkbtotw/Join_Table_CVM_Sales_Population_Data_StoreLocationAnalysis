# Script to read data and do joining operation

# Data : Sales, 711 distance from store, 60000 Store list, Population on grid, Share of shelf

Update:
2021-06-16 Created, Tawan T.
2021-06-23 Add more detail description of how to run group of codes to produce result

Why:
1.Create Data to use in model store identification (countrywide)

How:
1.Prepare all sets of data in certain location (directories : data, output, sales_data, temp)
2.run selected scripts from list below to achieve the desire goal
    - Append_CVM_File_R18.py     to integrate data of each Region  1 - 8 to one Append_CVM_File_R18
        input: \Project2021\Ad-Hoc\UpdateFile\Append_File\data\R1.csv - R8.csv
        output: \Project2021\Ad-Hoc\UpdateFile\Append_File\output\R18.csv

    - R18_Get_PAT.py  to use appended R 1 - 8 data to find province, district and subdistrict from Geopandas's SHAPE
        input: \Project2021\Ad-Hoc\UpdateFile\Append_File\output\R18.csv
        output: \Project2021\Ad-Hoc\UpdateFile\Append_File\output\r18_pat.csv
    
    - Join_R18_noDupe_popTambon.py    to join appended R 1- 8 data with Sum  population by sub-district
        input: (from Tha) \sales_data\pop_tambon.csv
                \Project2021\Ad-Hoc\UpdateFile\Append_File\output\r18_pat.csv
        output: \output\merged_18_tambon.csv      1**** 
    
    - Join_Sales_ShareOfShelf_Distance711.py      to join Sales + 711 + 60000 store list, Population data and Share of Shelf
        input: \sales_data\cvm_sale_all_202101-202105_cvmetl.xlsx    sales (from Tha)
               .dbo.Ext711_and_DIM_LOC_CVM_CUST_NEW         distance to closest 711    (from sandbox 2: CVM_Store_Location_Summary_rev6)
               \sales_data\Beer5sku_M3-5_2021_all_shareofshelf.xlsx  SoS    (from Tha)
               \sales_data\maindf_population_by_province_PAT_R18.csv     Population by province based on R18 lat lng customer list   (from sandbox 2: Search_population_by_location _rev3)
               \output\merged_18_tambon.csv  1******
        output: \output\merged_Sales_711_SoS_Store_R18Pop_R18_PopT_NoD.csv  2****   

    - Find_PopMinMax_AVGAMT_by_Province.py   to find Min Max of AVG AMT and population by province
        input: \output\merged_Sales_711_SoS_Store_R18Pop_R18_PopT_NoD.csv  2****
        output: \output\merged_Sales_711_SoS_Store_R18Pop_R18_PopT_MinMax_R18.csv 3****

    - Find_RR_FalgShip_Store_rev2.py    to assign to each customer code the shop RR type
        input: \sales_data\merged_Sales_711_SoS_Store_Population_R18_PopTambon_MinMax_R18.csv  3*****
        output: \output\RR_GRP_Customer_Code.csv  4****

    - Integrate_Merge_MinMax_RR_GRP_rev2.py   to merge maindata with RR_GRP data
        input: \output\merged_Sales_711_SoS_Store_R18Pop_R18_PopT_MinMax_R18.csv  3*****
               \output\RR_GRP_Customer_Code.csv   4****
        output: \output\merged_Sales_711_SoS_Store_R18Pop_R18_PopT_MinMax_R18_RRGRP.csv  5****
    
    ###############  Then send to Tha to process the data to get SCORE
    - CustomerSelection_by_TotalScore_rev2.py  to order the score by province, sales office and countrywide
        input: \sales_data\df_main2.csv    (<*************  from Tha)  Scored spreadsheet
               \sales_data\province_score.xlsx     ********** Adjust the Scoring Criteria of each province before each run
        output: \output\selected_customer_by_provincial_score_Filtered_020.csv    Scored result based on criteria in province_score.xlsx (in this case 0.2)     ============> Send back to Tha for further processing and reporting



Note: 
Use Function in Text _PreProcessing to add 0 in front of Customer_Code which has length less than 12 to make sure the joined result retains all store data.

Code Archive:
1.Join_CVM_Sales.py          to join CVM store and Sales table
2.Remove_Duplicates_rev2.py   to remove duplicates of duped Customer_Code in dataframe