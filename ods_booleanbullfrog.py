import csv
from collections import defaultdict
from pyexcel_ods import get_data
import json

# Load the spreadsheet with a column you want to convert to a boolean
ods_in = input("Name of input ods spreadsheet: ")
ods_in_col = input("Which target spreadsheet column do you want to write to (enter a number): ")

ods_colB = get_data(ods_in, start_column=2, column_limit=2)
print(json.dumps(ods_colB))

print('len(ods_colB) is', len(ods_colB))
print('len((json.dumps(ods_colB)) is', len((json.dumps(ods_colB))))

boolcolumns = []
for val in ods_colB:
    if bool(val) == True:
        boolcolumns.append(1)
    else:
        boolcolumns.append(" ")
print("boolcolumns = ", boolcolumns)


### Updating a column using pandas
import pandas as pd

# practice data frame
df = pd.DataFrame([[1,0],[0,1],[1,0],[0,1]], columns=["colA", "colB"])

# The syntax of subsetting a data frame is dfname.loc[startrow:endrow,startcolumn:endcolumn]
# Use this to write the boolean column to the target spreadsheet
df_subset = df[["colA"]]
# The syntax of replacing column A
dummycol = list("1" * len(df_subset))
print(dummycol)
df.loc[:, "colA"] = ["dog","cat","bear","sheep"]
print (df)

# Write boolean column to target spreadsheet
target_ods = input("Name of target ods spreadsheet: ")
target_col = input("Which target spreadsheet column do you want to write to (enter a number): ")

target_col_data = get_data(target_ods, start_column = target_col, column_limit = target_col)


"""
# For reading Start_Stop_Continue in csv format
columns = defaultdict(list)       # Each value in each column is appended to a list
    
with open('Start_Stop_Continue.csv') as f:
    reader = csv.DictReader(f)    # Reads rows into a dictionary object
    for row in reader:            # Reads each row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # Goes over each column name and value 
            columns[k].append(v)  # Appends the value into the appropriate list based on column name k

    boolcolumns = []
    for val in columns['Start']:
        #print(val)
        if bool(val) == True:
            boolcolumns.append(1)
        else:
            boolcolumns.append(" ")
"""
