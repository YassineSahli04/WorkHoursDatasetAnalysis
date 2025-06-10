import pandas as pd
from df_transformer import clean_dataset

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

df = pd.read_csv('Transformed Data v2.csv', sep=';', decimal=",")

df = clean_dataset(df)

index = 0
while index < len(df) - 1:
    week = str(df.at[index, 'WEEK'])
    if(index == 21):
        print('')
    next_week = str(df.at[index + 1, 'WEEK'])
    
    if '-' in week:
        start_day, end_day = map(int, week.split("-"))
    else:
        index += 1
        continue
    
    while 'Total' in next_week and index + 2 < len(df):
        index += 1
        next_week = str(df.at[index + 1, 'WEEK'])

    if '-' in next_week:
        next_start_day, _ = map(int, next_week.split("-"))
    
        if not ((end_day in [28, 29, 30, 31] and next_start_day == 1) or end_day == next_start_day - 1):
            print('Check Row: ', index +1)
    index += 1