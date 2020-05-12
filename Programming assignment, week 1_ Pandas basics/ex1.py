# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 22:42:24 2020

@author: david.hoyos
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
#%matplotlib inline 

from grader import Grader

DATA_FOLDER = 'data/'

transactions = pd.read_csv(os.path.join(DATA_FOLDER, 'sales_train.csv.gz'))
items = pd.read_csv(os.path.join(DATA_FOLDER, 'items.csv'))
item_categories = pd.read_csv(os.path.join(DATA_FOLDER, 'item_categories.csv'))
shops = pd.read_csv(os.path.join(DATA_FOLDER, 'shops.csv'))

grader = Grader()

# YOUR CODE GOES HERE
transx = transactions.shape
itemx = items.shape
categx = item_categories.shape
shopx = shops.shape

print ("shape of transaction is {}".format(transx), "| shape of items is {}".format(itemx), "| shape of categories is {}".format(categx), "| shape of shops is {}".format(shopx))

transactions.head()
items.head()
item_categories.head()
shops.head()

'''
#________________________________________________________________________________
# YOUR CODE GOES HERE 1
# What was the maximum total revenue among all the shops in September, 2014?
'''
transactions['date'] = pd.to_datetime(transactions['date'], format = '%d.%m.%Y')
transactions['day'] = transactions['date'].dt.day
transactions['month'] = transactions['date'].dt.month
transactions['year'] = transactions['date'].dt.year

# Adding filters for transactions from Sep 2014
df_sep_14 = transactions[(transactions.month == 9) & (transactions.year == 2014)]
df_sep_14.head()

df_sep_14['revenue'] = (df_sep_14.item_price) * (df_sep_14.item_cnt_day)
answer1 = df_sep_14[['shop_id', 'revenue']].groupby('shop_id').sum().max().values

# PUT YOUR ANSWER IN THIS VARIABLE
max_revenue = answer1
grader.submit_tag('max_revenue', max_revenue)

'''
#________________________________________________________________________________
# YOUR CODE GOES HERE 2
# What item category generated the highest revenue in summer 2014?
'''
summer = [6,7,8]
df_summer_14 = transactions[(transactions.month.isin(summer)) & (transactions.year == 2014)]

#join to get the category id of the transaction
items_with_categories = pd.merge(items, item_categories, how = 'left', on = 'item_category_id')
tx_with_categories = pd.merge(df_summer_14, items_with_categories, how = 'left', on = 'item_id')
tx_with_categories['revenue'] = (tx_with_categories.item_price) * (tx_with_categories.item_cnt_day)

# Grouping by category id and sorting
tx_cat_sum = tx_with_categories[tx_with_categories['revenue'] > 0]
grouped_df = tx_cat_sum.groupby('item_category_id').agg({'revenue':sum})
grouped_df = grouped_df.sort_values(by='revenue', ascending=False)
answer2 = grouped_df.idxmax().values

# PUT YOUR ANSWER IN THIS VARIABLE
category_id_with_max_revenue = answer2
grader.submit_tag('category_id_with_max_revenue', category_id_with_max_revenue)

'''
#________________________________________________________________________________
# YOUR CODE GOES HERE 3
# How many items are there, such that their price stays constant (to the best of our knowledge) during the whole period of time?
'''
columns = ['date','date_block_num','item_cnt_day','shop_id','day','month','year']
trans3_df = transactions.drop(columns, axis=1)
unique_item_count = trans3_df.groupby(['item_id','item_price']).count()
unique_prices = unique_item_count.reset_index().groupby('item_id')['item_price'].nunique()
y = unique_prices.value_counts()
answer3 = y[1]

# PUT YOUR ANSWER IN THIS VARIABLE
num_items_constant_price = answer3
grader.submit_tag('num_items_constant_price', num_items_constant_price)

'''
#________________________________________________________________________________
# YOUR CODE GOES HERE 4
# What was the variance of the number of sold items per day sequence for the shop with shop_id = 25 in December, 2014?
# Do not count the items, that were sold but returned back later.
'''

shop_id = 25
#transx in Dec 14
df_id25_dec_14 = transactions[(transactions.month == 12) & (transactions.year == 2014) & (transactions.shop_id == shop_id)]

# YOUR CODE GOES HERE
total_num_items_sold = df_id25_dec_14.loc[:, ['day','item_cnt_day']].groupby(['day']).sum().values
days = df_id25_dec_14.day.sort_values().unique()

# Plot it
plt.plot(days, total_num_items_sold)
plt.ylabel('Num items')
plt.xlabel('Day')
plt.title("Daily revenue for shop_id = 25")
plt.show()

answer4 = np.var(total_num_items_sold, ddof = 1)

total_num_items_sold_var = answer4 # PUT YOUR ANSWER IN THIS VARIABLE
grader.submit_tag('total_num_items_sold_var', total_num_items_sold_var)

STUDENT_EMAIL = 'davidhoga@gmail.com' # EMAIL HERE
STUDENT_TOKEN = 'sNjAAE6uyZ0hAXhe' # TOKEN HERE
grader.status()

grader.submit(STUDENT_EMAIL, STUDENT_TOKEN)