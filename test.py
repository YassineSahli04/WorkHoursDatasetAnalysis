import pandas as pd
import matplotlib.pyplot as plt
from df_transformer import clean_dataset, clean_week_column
from data_visualizer import visualize_monthly_hours

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

df = pd.read_csv('Data/Transformed Data 2022.csv', sep=';', decimal=",")

df = clean_dataset(df)

by_name_or_role = 'role'
initial_df = df
year = 2022

df = initial_df[initial_df['WEEK'] == 'Total']
df = df.set_index('MONTH')
df = df.drop(columns=['YEAR', 'WEEK', 'Total'])

if by_name_or_role == 'name':
    df.columns = [col[0] for col in df.columns]
    title = "Monthly Hours by Person in " , year
if by_name_or_role == 'role':
    df.columns = [col[1] for col in df.columns]
    df = df.T.groupby(level=0).sum().T
    title = "Monthly Hours by Role in ", year

df.plot(kind='bar', figsize=(10, 5), stacked=True)
plt.title(title)
plt.ylabel("Hours")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

df.head()