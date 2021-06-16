# Script to read data and do joining operation

# Data : Sales, 711 distance from store, 60000 Store list, Population on grid, Share of shelf

Update:
2021-06-16 Created, Tawan T.

Why:
1.Create Data to use in model store identification (countrywide)

How:
1.Prepare all sets of data in certain location (directories : data, output, sales_data, temp)
2.run selected scripts from list below to achieve the desire goal
    - Append_CVM_File_R18.py     to integrate data of each Region  1 - 8 to one Append_CVM_File_R18
    - Join_CVM_Sales.py          to join CVM store and Sales table
    - Join_Sales_ShareOfShelf_Distance711.py      to join Sales + 711 + 60000 store list, Population data and Share of Shelf
    - R18_Get_PAT.py  to use appended R 1 - 8 data to find province, district and subdistrict from Geopandas's SHAPE
    - Remove_Duplicates_rev2.py   to remove duplicates of duped Customer_Code in dataframe
    - Join_R18_noDupe_popTambon.py    to join appended R 1- 8 data with Sum  population by sub-district

Note: 
Use Function in Text _PreProcessing to add 0 in front of Customer_Code which has length less than 12 to make sure the joined result retains all store data.