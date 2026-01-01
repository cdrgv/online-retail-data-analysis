import pandas as pd
import numpy as np
df=pd.read_csv('synthetic_online_retail_data.csv')
# print(df.head())
# print(df.shape)
# print(df.info())
# print(df.isnull().sum())
# print(df.describe())
df['review_score']=df['review_score'].fillna(df['review_score'].median())
df['gender']=df['gender'].fillna('unknown')
# print(df.isnull().sum())
# print(df[['quantity','price','age','review_score']].describe())
df['total_amount']=df['quantity']*df['price']
customer_df=df.groupby('customer_id').agg(
    total_spent=('total_amount','sum'),
    total_orders=('order_date','count'),
    avg_review_score=('review_score','mean')
).reset_index()
# print(customer_df.head())
# print(customer_df.describe())
high_spend_threshold=customer_df['total_spent'].quantile(0.75)
low_spend_threshold=customer_df['total_spent'].quantile(0.25)
low_review_threshold=customer_df['avg_review_score'].quantile(0.25)
def assign_segment(row):
    if row['total_spent']>=high_spend_threshold and row['avg_review_score']>=4:
        return 'High Value & Satisfied'
    elif row['total_spent']>=high_spend_threshold and row['avg_review_score']<4:
        return 'High Value & Unsatisfied'
    elif row['total_spent']<=low_spend_threshold and row['avg_review_score']>=4:
        return 'Low Value & Satisfied'
    else:
        return 'Low Value & At risk'
customer_df['customer_segment']=customer_df.apply(assign_segment,axis=1)
print(customer_df['customer_segment'].value_counts())
df.to_csv('cleaned_synthetic_online_retail_data.csv',index=False)
print(df.info())