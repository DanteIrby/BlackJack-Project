
#import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('Basic Strategy.csv')

# Define the values for T2 and U2
T2_value = 'value_for_T2'
U2_value = 'value_for_U2'

# Define the ranges for the index and match functions
range_E3_O30 = df.iloc[2:30, 4:15]  # Indexing starts at 0, so 2:30 represents rows 3 to 31, and 4:15 represents columns E to O
range_D3_D12 = df.iloc[2:12, 3]    # Rows 3 to 12 of column D
range_F2_O2 = df.iloc[1, 5:15]     # Row 2 of columns F to O

# Use the index and match functions to retrieve the value
result = range_E3_O30.iloc[
    range_D3_D12[
        range_D3_D12 == T2_value
    ].index[0],
    range_F2_O2[
        range_F2_O2 == U2_value
    ].index[0]
]

# Print the result
print(result)
