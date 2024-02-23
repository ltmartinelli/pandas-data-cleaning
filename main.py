import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Create DataFrame
df = pd.read_excel(r'customer-list.xlsx')

# Remove duplicates
df = df.drop_duplicates()

# Remove undesired columns
df = df.drop(columns='Not_Useful_Column')

# String Strip with Regex
df['Last_Name'] = df['Last_Name'].str.strip('123._/')

# Phone Standardizing:

# Remove all non-alphanumeric character
df['Phone_Number'] = df['Phone_Number'].str.replace('[^a-zA-Z0-9]', '', regex=True)

# Convert values to string
# Use Lambda and slicing to add - after every the 3rd and 6th digits
# Remove the nan-- and Na-- values

df['Phone_Number'] = df['Phone_Number'].apply(lambda x: str(x))
df['Phone_Number'] = df['Phone_Number'].apply(lambda x: x[0:3] + '-' + x[3:6] + '-' + x[6:10])
df['Phone_Number'] = df['Phone_Number'].str.replace('nan--', '')
df['Phone_Number'] = df['Phone_Number'].str.replace('Na--', '')

# Atomize/Split address column

df[['Street', 'State', 'ZIP']] = df['Address'].str.split(',', n=2, expand=True)

# Standardize Paying Customer and Do Not Contact

df['Do_Not_Contact'] = df['Do_Not_Contact'].str.replace('Yes', 'Y')
df['Do_Not_Contact'] = df['Do_Not_Contact'].str.replace('No', 'N')

df['Paying Customer'] = df['Paying Customer'].str.replace('Yes', 'Y')
df['Paying Customer'] = df['Paying Customer'].str.replace('No', 'N')

df = df.replace('N/a', '')
df = df.fillna('')

# Filtering Down Rows without number or with prohibition of contact

for x in df.index:
    if df.loc[x, "Do_Not_Contact"] == 'Y':
        df.drop(x, inplace=True)

for x in df.index:
    if df.loc[x, "Phone_Number"] == '':
        df.drop(x, inplace=True)

# Reset index (drop removes the column with the old indexes, which would remain otherwise)

df = df.reset_index(drop=True)

print(df)
