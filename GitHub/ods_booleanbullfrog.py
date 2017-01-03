import csv
from collections import defaultdict
from pyexcel_ods3 import get_data
import json
try:
    target_ods_read = input('Enter the name of an ods spreadsheet containing a column with '\
    'text that you want to convert to boolean: ')
except IOError:
    print('Can\'t find that ods file')

try:
    target_column_read = int(input('Which spreadsheet column do you want to convert to boolean (enter a number): '))
except ValueError:
    print('Oops, not an integer \n\n')

# Create ordered list
ods_col = get_data(target_ods_read, start_column = target_column_read, column_limit = target_column_read)
ods_col = list(ods_col.items())
ods_col = ods_col[0]
ods_col = ods_col[1]

# Convert ods_col values to 1 if there's text in the column row, ' ' if there's no text.
boolcolumns = []
for val in ods_col:
    boolcolumns.append(1)  # But get_data is ignoring rows with missing data 
print(boolcolumns)   

# Write boolean column to target spreadsheet
target_ods_write = input('Name of target ods spreadsheet: ')
target_col_write = input('Which target spreadsheet column do you want to write to (enter a number). Use 6 for default work: ')

target_col_write_data = get_data(target_ods_write, start_column = target_col_write, column_limit = target_col_write)


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
            boolcolumns.append(' ')
"""

"""
### Testing updating a column using pandas
import pandas as pd

# Create the following practice data frame: 
#    colA  colB
#0    dog     0
#1    cat     1
#2   bear     0
#3  sheep     1

df = pd.DataFrame([['dog',0],['cat',1],['bear',0],['sheep',1]], columns=['colA', 'colB'])

# Replace column A
# The syntax of subsetting a data frame is dfname.loc[startrow:endrow,startcolumn:endcolumn]

df.loc[:, 'colA'] = [1, 0 , 1, 0]
print (df)

# New data frame will be:
#    colA  colB
#0     1     0
#1     0     1
#2     1     0
#3     0     1

ods_col = get_data('/Users/Megatron/Documents/throwaway.ods', start_column = 1, column_limit = 1)
#print(ods_col, '\n')
ods_col = list(ods_col.items())
#print(ods_col, '\n')
ods_col = ods_col[0]
#print(ods_col, '\n')
ods_col = ods_col[1]
#print(ods_col, '\n')

new_list = []
for i in ods_col:
    new_list.append(i[0])   

### Testing complete
"""