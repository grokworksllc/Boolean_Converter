import csv
from collections import defaultdict
from pyexcel_ods import get_data
import json

try:
    target_ods_read = input('Enter the name of an ods spreadsheet containing a column with '\
    'text that you want to convert to boolean: ')
except IOError:
    print('Can\'t find input that ods file')

try:
    target_column_read = int(input('Which spreadsheet column do you want to convert to boolean (enter a number): '))
    if not int(target_column_read):
        raise ValueError('Error: please enter a number')
except ValueError as e:
    print(e)

ods_col = get_data(target_ods_read, start_column = target_column_read, column_limit = target_column_read)
print('ods_col is', ods_col)

# Convert ods_col values to 1 if there's text in the column row, ' ' if there's no text.
boolcolumns = []
for val in ods_col:
    if bool(val) == True:
        boolcolumns.append(1)
    else:
        boolcolumns.append(' ')
print('boolcolumns = ', boolcolumns)

#print(json.dumps(ods_col))
#print('len(ods_col) is', len(ods_col))
#print('len((json.dumps(ods_col)) is', len((json.dumps(ods_col))))


### Testing updating a column using pandas
import pandas as pd

# practice data frame
df = pd.DataFrame([[1,0],[0,1],[1,0],[0,1]], columns=['colA', 'colB'])
print('df is ', df)
# The syntax of subsetting a data frame is dfname.loc[startrow:endrow,startcolumn:endcolumn]
# Use this to write the boolean column to the target spreadsheet
df_subset = df[['colA']]
# The syntax of replacing column A
dummycol = list('1' * len(df_subset))
print(dummycol)
df.loc[:, 'colA'] = ['dog','cat','bear','sheep']
print (df)

### Testing complete


# Write boolean column to target spreadsheet
target_ods_write = input('Name of target ods spreadsheet: ')
target_col_write = input('Which target spreadsheet column do you want to write to (enter a number). Use 6 for default work: ')

target_col_write_data = get_data(target_ods_write, start_column = target_col_write, column_limit = target_col_write)

file.close(target_ods_read)


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
