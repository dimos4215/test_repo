from Upini_thesis_project.Config import Config
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from Upini_thesis_project.Utilities.Recommender import collaborative_filtering

from matplotlib.pyplot import axis
cf = Config()
plt.interactive(False)
sns.set_style('white')

#Variables
data_dir = os.path.relpath(cf.dataset_dir)

min_std_of_item_ratings = cf.min_std_of_item_ratings
min_num_of_item_ratings = cf.min_num_of_item_ratings
min_num_of_user_ratings = cf.min_num_of_user_ratings
min_std_of_user_ratings = cf.min_std_of_user_ratings
print('==========Start Loading Raw data==========')


'''
Load movielens dataset into a dataframe and merge with movie titles???
'''
column_names = ['user_id', 'item_id', 'rating', 'timestamp']
df = pd.read_csv(data_dir , sep='\t', names=column_names)

print('Filter users with less than', min_num_of_user_ratings, 'ratings')


n_users = df.user_id.nunique()
n_items = df.item_id.nunique()
print('init_n_users',n_users)
print('init_n_items',n_items)

'''
Filter Items
    1.count ratings grouped by Item and create new dataframe
    2. filter out Items with less ratings than threshold (min_std_of_item_ratings)
    3. filter out Items with less ratings_std than threshold (min_std_of_item_ratings)
    4. Join with initial dataset (inner join) to keep only items with the above constrains
    5. Drop aggregated columns
'''
grouped_by_item_stats = pd.DataFrame(df.groupby('item_id')['rating'].std())
grouped_by_item_stats.rename(columns={'rating': 'rating_std'}, inplace=True)
grouped_by_item_stats['num_of_ratings'] = pd.DataFrame(df.groupby('item_id')['rating'].count())
p1 = sns.jointplot(x='rating_std', y='num_of_ratings', data=grouped_by_item_stats, alpha=0.5)
p1.fig.subplots_adjust(top=0.9)
p1.fig.suptitle('Initial Item Stats', fontsize=12)

grouped_by_item_stats = grouped_by_item_stats[grouped_by_item_stats['rating_std'] > min_std_of_item_ratings]
grouped_by_item_stats = grouped_by_item_stats[grouped_by_item_stats['num_of_ratings'] > min_num_of_item_ratings]
p2 = sns.jointplot(x='rating_std', y='num_of_ratings', data=grouped_by_item_stats, alpha=0.5)
p2.fig.subplots_adjust(top=0.9)
p2.fig.suptitle('Filtered Item Stats', fontsize=12)

df = pd.merge(df, grouped_by_item_stats, left_on='item_id', right_index=True)
df = df.drop(['rating_std','num_of_ratings'], axis=1)

print('df',df)

n_users = df.user_id.nunique()
n_items = df.item_id.nunique()

print('n_users',n_users)
print('n_items',n_items)


'''
Filter Users
    1.count ratings grouped by Users and create new dataframe
    2. filter out Users with less ratings than threshold (min_std_of_user_ratings)
    3. filter out Users with less ratings_std than threshold (min_std_of_user_ratings)
    4. Join with initial dataset (inner join) to keep only user with the above constrains
    5. Drop aggregated columns
'''
grouped_by_user_stats = pd.DataFrame(df.groupby('user_id')['rating'].std())
grouped_by_user_stats.rename(columns={'rating': 'rating_std'}, inplace=True)
grouped_by_user_stats['num_of_ratings'] = pd.DataFrame(df.groupby('user_id')['rating'].count())
p3 = sns.jointplot(x='rating_std', y='num_of_ratings', data=grouped_by_user_stats, alpha=0.5)
p3.fig.subplots_adjust(top=0.9)
p3.fig.suptitle('Initial User Stats', fontsize=12)

grouped_by_user_stats = grouped_by_user_stats[grouped_by_user_stats['rating_std'] > min_std_of_user_ratings]
grouped_by_user_stats = grouped_by_user_stats[grouped_by_user_stats['num_of_ratings'] > min_num_of_user_ratings]
p4 = sns.jointplot(x='rating_std', y='num_of_ratings', data=grouped_by_user_stats, alpha=0.5)
p4.fig.subplots_adjust(top=0.9)
p4.fig.suptitle('Filtered User Stats', fontsize=12)

df = pd.merge(df, grouped_by_user_stats, left_on='user_id', right_index=True)
df = df.drop(['rating_std','num_of_ratings'], axis=1)

print('df',df)

n_users = df.user_id.nunique()
n_items = df.item_id.nunique()

print('n_users',n_users)
print('n_items',n_items)

if cf.show_charts:
    plt.show()


'''
    Initialize Recommender
'''
collaborative_filtering(df,cf )#todo: fix colaborative settings


