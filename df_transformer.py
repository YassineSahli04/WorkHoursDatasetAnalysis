import pandas as pd 
import re

def clean_dataset(df):
    replace_hours_NaN_by_0(df)
    transform_header_to_tuple(df)
    df = remove_rows_with_ND_vals_week_col(df)
    clean_week_column(df)
    return df

def remove_rows_with_ND_vals_week_col(df):
    return df[df['WEEK'].apply(lambda x: '-' in str(x) or x == 'Total')].reset_index(drop=True) 


def replace_hours_NaN_by_0(df):
    for index, row in df.iterrows():
        for col in df.columns:
            if col not in ['YEAR', 'MONTH', 'WEEK', 'WEEK LENGTH'] and pd.isna(df.at[index, col]):
               df.at[index, col] = 0.0

def transform_header_to_tuple(df):
    new_columns = {}
    for col in df.columns:
        if col not in ['YEAR', 'MONTH', 'WEEK', 'PERIOD', 'WEEK LENGTH']:
            if "," not in col:
                continue
            new_col = []
            name, role = col.split(",")
            new_columns[col] = (name.strip(), role.strip())

    df.rename(columns=new_columns, inplace=True)

def clean_week_column(df):
    for index, row in df.iterrows():
        val = row['WEEK']

        if isinstance(val, str) and 'Total' in val:
            continue
    
        if val.isdigit():
            val = int(val)
            df.at[index, 'WEEK'] = f"{val}-{val}"
               
        elems = re.findall(r'\w+|[-]',val)
        count_other = 0
        int_list = []
        for elem in elems:
            try:
                int_list.append(int(elem))
            except:
                count_other += 1
 
        if '-' in elems and len(int_list) == 2:
            if count_other == 1:
                continue
            else:
                df.at[index, 'WEEK'] = f"{int_list[0]}-{int_list[1]}"





def check_week_interval(df):
    index = 0
    while index < len(df) - 1:
        week = str(df.at[index, 'WEEK'])
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
      
def calculate_total_worked_hours(df, by_name_or_role= 'name'):
    if(by_name_or_role == 'name'):
        idx =0
    if by_name_or_role == 'role':
        idx = 1
    hours_count = {}
    for index, row in df.iterrows():
        if row['WEEK'] == 'Total':
            for col in df.columns:
                if col not in ['YEAR', 'MONTH', 'WEEK', 'PERIOD','WEEK LENGTH']:
                    if isinstance(col, tuple):
                        key = col[idx]
                        hours = row[col]
                        if isinstance(hours, float): 
                            if key not in hours_count:
                                hours_count[key] = 0.0
                            hours_count[key] += hours
    sorted_count = dict(sorted(hours_count.items(), key=lambda item: item[1], reverse=True))
    return sorted_count 

# def calculate_monthly_work(df, by_name_or_role= 'name'):
#     if(by_name_or_role == 'name'):
#         idx =0
#     if by_name_or_role == 'role':
#         idx = 1
#     monthly_count = {}
#     for index, row in df.iterrows():
#         if row['WEEK'] == 'Total':
#             month = row['MONTH']
#             if month not in monthly_count:
#                 monthly_count[month] = {}
#             for col in df.columns:
#                 if col not in ['YEAR', 'MONTH', 'WEEK']:
#                     if isinstance(col, tuple):
#                         key = col[idx]
#                         hours = row[col]
#                         if isinstance(hours, float): 
#                             if key not in monthly_count[month]:
#                                 monthly_count[month][key] = 0.0
#                             monthly_count[month][key] += hours
#     return monthly_count
    
def add_column_week_length(df):
    for index, row in df.iterrows():
        week = row['WEEK']
        if '-' in str(week):
            start_day,end_day = week.split("-")
            try:
                length = int(end_day.strip()) - int(start_day.strip()) +1
                df.at[index,'WEEK'] = length
            except Exception:
                df.at[index,'WEEK'] = -1
        else:
            df.at[index,'WEEK'] = -1
    
    df.rename(columns={'WEEK': 'WEEK LENGTH'}, inplace=True)


def assign_equal_weekly_periods(df):
    df = df[df['WEEK LENGTH'] != -1].reset_index(drop=True)

    def merge_if_different(val1, val2):
        return f"{val1} / {val2}" if val1 != val2 else str(val1)

    col_to_not_sum = ['YEAR', 'MONTH', 'WEEK LENGTH']
    cols_to_sum = [col for col in df.columns if col not in col_to_not_sum]

    index = 0
    while index < len(df):
        if df.at[index, 'WEEK LENGTH'] == 7:
            index += 1
            continue

        target_index = index
        total_length = df.at[target_index, 'WEEK LENGTH']

        while total_length < 7 and target_index + 1 < len(df):
            target_index += 1
            total_length += df.at[target_index, 'WEEK LENGTH']

        if total_length > 7 and total_length != 7:
            total_length -= df.at[target_index, 'WEEK LENGTH']
            target_index -= 1

        rows_to_merge = list(range(index, target_index + 1))

        summed = df.loc[rows_to_merge, cols_to_sum].sum()
        year_vals = df.loc[rows_to_merge, 'YEAR'].unique()
        month_vals = df.loc[rows_to_merge, 'MONTH'].unique()

        year_val = ' / '.join(map(str, year_vals)) if len(year_vals) > 1 else str(year_vals[0])
        month_val = ' / '.join(map(str, month_vals)) if len(month_vals) > 1 else str(month_vals[0])

        new_row = pd.Series({**summed, 'YEAR': year_val, 'MONTH': month_val, 'WEEK LENGTH': total_length})


        
        for col in new_row.index:
            df.at[index, col] = new_row[col]

        df = df.drop(index=rows_to_merge[1:]).reset_index(drop=True)
        index += 1


    return df
