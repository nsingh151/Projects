# Importing Required Libraries
import pandas as pd
import numpy as np
import xlrd
import os


## User driven Location of Source to target file
location = input(r"Enter the location of Source to target mapping (for e.g. : C:\Users\nsingh1\Documents\fun world\test_source_to_target.xlsx) : ")

data = pd.read_excel(location)
print("\n"+"*"*10 + "  File imported Successfully  " + "*"*10)

print("\n Shape of the data\n ", data.shape)
print("\n Columns in Excels\n ", data.columns )


## Cleaning DataFrame for empty values
data.dropna(axis=0, subset=['Column_Name'], inplace=True)
print("\nShape of the data after removal unwanted rows", data.shape)

# Replacing Pandas NA to String 'NA'

data = data.replace(np.nan, 'NA', regex=True)
print("\nShape of the data after replacing NaN", data.shape)

## Final DDL Creation Script
file_name = data['Table_Name'][0].upper()+".sql"
print("\nDDL File Name : ",file_name)

file_path = input(r"Enter the location ( Folder location ) where you want to save the DDL File: ")

file_path = "{}\{}".format(file_path,
                                   file_name)
								   
print("\nDDL File Path : ",file_path )
with open(file_path, 'w') as f:
    
    #Table related Analysis
    f.write("/* \n\n Definition: {}\n\n Rational: {} \n\n Data Analysis: \n\n {}\n\n Attribution Level Information: \n\n{}\n\n\n */ \n\n\n  Create Table Wars.bi.{}  \n\n   ( \n".format(data['Table_Defination'][0],
                                                                                                                            data['Table_Rational'][0],
                                                                                                                            data['Table_Data_Analysis'][0],
                                                                                                                            data['Attribution_Level_Information'][0],
                                                                                                                            data['Table_Name'][0]))
    column_count = 0
    #Column related Analysis
    for elem in range(len(data)):

        column_name =data['Column_Name'][elem].upper()
        data_type = data['Data_Type'][elem].upper()

        # Size and Precision Block 
        if data['Size'][elem] == 'NA' :   # Checking whether the size of the column is present or not for e.g. integer has no size and precision whereas decimal has 
            precisions=""

        else:
            size = str(int(data['Size'][elem]))
            
    #       For precision 
            if data['Precision'][elem] == 'NA':
                precisions = "( "+ size + " )"

            else:            
                precisions = "( " + size + "," + str(int(data['Precision'][elem])) + " )"


        # Nullability Check, whether the column is null or not
        if data['Nullable'][elem].lower() == "no":
            Null_check = " NOT NULL ,"

        else:
            Null_check = " ,"
      
        #Comment String with Column Analysis
        comment = "  --" + data['Column_Defination'][elem] + " | " + data['Column_Defination'][elem] + " | "  +  data['Column_Rational'][elem] + " | "  + data['Column_Is_SCD'][elem] + " | " + data['Column_SCD_Reason'][elem] + " | "  +    str(data['Column_Null_Percent'][elem]) + "% | " + str(data['Column_Group_Count'][elem])
        
        # Column row in DDL
        text = "{:>45}{:>18}{:>12}{:>12}{:>100}".format(column_name,
                                                        data_type,
                                                        precisions,
                                                        Null_check,
                                                        comment)
        f.write(text)
        f.write("\n")
        column_count = column_count + 1
    f.write("\n\n")
    
    # Constraint Block in DDl
    constraint_cnt = 0 
    for index in range(len(data)):
        
        if data['Key'][index].upper()=='PK':
            line ="  CONSTRAINT PK_{} PRIMARY KEY NONCLUSTERED ({})".format(data['Table_Name'][0],
                                                                          data['Column_Name'][index].upper())
            f.write(line+"\n")
            constraint_cnt = constraint_cnt +1
            
        elif data['Key'][index].upper()=='FK':
            f.write(" ,")
            line = "CONSTRAINT FK_{}_{} FOREIGN KEY ({}) REFERENCES {} ({})".format(data['Table_Name'][0],
                                                                                     data['Column_Name'][index].upper(),
                                                                                     data['Column_Name'][index].upper(),
                                                                                     data['Source_Table'][index],
                                                                                     data['Source_Column'][index].upper())
            f.write(line+"\n")
            constraint_cnt = constraint_cnt +1
            
        else:
            continue
            
    f.write("\n);")
    f.close()

print("\nTotal Column inserted : ", column_count)
print("\nTotal Constraints (Inc. 1 Primary Key constraint) : ", constraint_cnt)
print("\n"+"*"*10 + "  DDL Created Successfully at \"" + file_path + "\"    "+"*"*10)
