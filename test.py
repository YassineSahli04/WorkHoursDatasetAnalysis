import pandas as pd
import matplotlib.pyplot as plt
from df_transformer import clean_dataset, add_column_week_length, assign_equal_weekly_periods
from data_visualizer import visualize_monthly_hours

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

df = pd.read_csv('Data/Transformed Data 2023.csv', sep=';', decimal=",")

df = clean_dataset(df)

add_column_week_length(df)
df = assign_equal_weekly_periods(df)