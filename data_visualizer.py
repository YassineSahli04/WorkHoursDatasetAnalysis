import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

def visualize_dict_horiz_bar(dict, title):
    keys = list(dict.keys())
    values = list(dict.values())

    plt.figure(figsize=(8, 4))
    plt.barh(keys, values, color='skyblue')
    plt.xlabel("Total Hours Worked")
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

def visualize_dict_pie(data_dict, title):
    keys = list(data_dict.keys())
    values = list(data_dict.values())

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=keys, autopct='%1.1f%%', startangle=90)
    plt.title(title)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def visualize_monthly_hours(initial_df, by_name_or_role= 'name', year = 2024):
    df = initial_df[initial_df['WEEK'] == 'Total']
    df = df.set_index('MONTH')
    df = df.drop(columns=['YEAR', 'WEEK', 'Total'])

    if by_name_or_role == 'name':
        df.columns = [col[0] for col in df.columns]
        title = f"Monthly Hours by Person in {year}"
    if by_name_or_role == 'role':
        df.columns = [col[1] for col in df.columns]
        df = df.T.groupby(level=0).sum().T
        title = f"Monthly Hours by Role in {year}"

    df.plot(kind='bar', figsize=(10, 5), stacked=True)
    plt.title(title)
    plt.ylabel("Hours")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



def visualize_weekly_total_hours(df, year):
    df = df.copy()
    df['WEEK_ID'] = range(1, len(df) + 1)
    plt.figure(figsize=(10, 5))
    plt.plot(df['WEEK_ID'], df['Total'], marker='o')
    plt.xlabel('Week #')
    plt.ylabel('Total Hours Worked')
    plt.title(f'Weekly Total Hours Trend in {year}')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def visualize_weekly_hours_by_person(df, year):

    df = df.copy()
    df['WEEK_ID'] = range(1, len(df) + 1)

    other_cols = ['YEAR', 'MONTH', 'WEEK LENGTH', 'Total','WEEK_ID']
    df.columns = [
        col[0] if isinstance(col, tuple) and col not in other_cols else col
        for col in df.columns
    ]
    people_columns = [col for col in df.columns if col not in other_cols]

    plot_data = df.set_index('WEEK_ID')[people_columns]
    plot_data = plot_data.apply(pd.to_numeric, errors='coerce')

    plot_data.plot(kind='bar', stacked=True, figsize=(12, 6))
    plt.title(f'Weekly Workload by Person in {year}')
    plt.xlabel('Week #')
    plt.ylabel('Hours Worked')
    plt.legend(title='Person')
    plt.tight_layout()
    plt.show()

def visualize_weekly_hours_by_role(df, year):

    df = df.copy()
    df['WEEK_ID'] = range(1, len(df) + 1)

    other_cols = ['YEAR', 'MONTH', 'WEEK LENGTH', 'Total', 'WEEK_ID']
    people_columns = [col for col in df.columns if col not in other_cols]

    role_sums = defaultdict(lambda: pd.Series([0] * len(df)))

    for col in people_columns:
        if isinstance(col, tuple) and len(col) == 2:
            name, role = col
            role_sums[role] += pd.to_numeric(df[col], errors='coerce').fillna(0)

    if not role_sums:
        print("No numeric role columns to plot.")
        return

    role_df = pd.DataFrame(role_sums)
    role_df['WEEK_ID'] = df['WEEK_ID']
    role_df = role_df.set_index('WEEK_ID')

    role_df.plot(kind='bar', stacked=True, figsize=(12, 6))
    plt.title(f'Weekly Workload by Role in {year}')
    plt.xlabel('Week #')
    plt.ylabel('Hours Worked')
    plt.legend(title='Role')
    plt.tight_layout()
    plt.show()


