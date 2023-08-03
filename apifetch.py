import requests
import pandas as pd
import numpy as np

access_key = 'fe66583bfe5185048c66571293e0d358'

header = {'access_token': access_key}

baseurl = 'https://globalmart-api.onrender.com'
endpoint = '/mentorskool/v1/sales?offset=1&limit=100'

data=[]
for i in range(5):
    response = requests.get(baseurl+endpoint, headers=header)
    response_data = response.json()
    endpoint = response_data['next']
    data.extend(response.json()['data'])

df = pd.json_normalize(data)

df[:5]

df = df.replace('null', np.nan)
null_counts = df.isnull().sum()
print(null_counts)

duplicate_records = df[df.duplicated(keep=False)]
print("Duplicate records:")
print(duplicate_records)


df['order.order_purchase_date'] = pd.to_datetime(df['order.order_purchase_date'])
df['day_of_week'] = df['order.order_purchase_date'].dt.dayofweek
weekend_orders = df[df['day_of_week'].isin([5, 6])]
num_weekend_orders = len(weekend_orders)
print("Number of orders placed on weekends:", num_weekend_orders)
df['order.order_purchase_date'] = pd.to_datetime(df['order.order_purchase_date'])
df['day_of_week'] = df['order.order_purchase_date'].dt.dayofweek
sales_by_day = df.groupby('day_of_week')['sales_amt'].sum()
weekend_sales = sales_by_day.loc[[5, 6]].sum()
weekday_sales = sales_by_day.loc[[0, 1, 2, 3, 4]].sum()
print("weekend_sales: ", weekend_sales)
print("weekday_sales: ", weekday_sales)
if weekend_sales > weekday_sales:
    print("Weekend has the highest sales.")
elif weekend_sales < weekday_sales:
    print("Weekdays have the highest sales.")
else:
    print("Weekends and weekdays have the same sales.")