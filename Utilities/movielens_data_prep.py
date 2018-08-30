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
min_number_of_rated_items = cf.min_number_of_rated_items

print('==========Start Loading Raw data==========')
'''
Load movielens dataset into a dataframe and merge with movie titles???
'''


column_names = ['user_id', 'item_id', 'rating', 'timestamp']
df = pd.read_csv(data_dir , sep='\t', names=column_names)
# movie_titles = pd.read_csv(data_dir+"Movie_Id_Titles")
# df = pd.merge(df,movie_titles,on='item_id')
# create new dataframe to filter user/items



print('Filter users with less than',min_number_of_rated_items,'ratings')
'''
1.count ratings grouped by user and create new dataframe
2. filter out users with less ratings than threshold (min_number_of_rated_items)
3. Join with initial dataset (inner join) to keep only user with more ratings than min_number_of_rated_items
4. Drop aggregated column
5. Rename rating column
'''

grouped_by_user = pd.DataFrame(df.groupby('user_id')['rating'].count())
grouped_by_user = grouped_by_user[grouped_by_user.rating > min_number_of_rated_items]##edit row after testing < to >
df = pd.merge(df, grouped_by_user, left_on='user_id', right_index=True)
df = df.drop('rating_y', axis=1)
df.rename(columns={'rating_x': 'rating'}, inplace=True)


print('Data Load Completed\n')


collaborative_filtering(df,cf)


'''
f = open("demofile.txt", "a")

line = 'user'
for item_index, value in np.ndenumerate(user_prediction[0,:]):
    line += ','+ str( index_item_map[item_index[0]] )

f.write(line)

print(line)




for user_index , items_list in enumerate(user_prediction):

    line ="\n"+str(index_user_map[user_index])

    for item_index , value in enumerate(items_list):
        line += ',' + str(value)

    print ('line',line)
    f.write(line)

'''

'''
for (user_index,item_index) ,value in np.ndenumerate(user_prediction):

    if item_index == 0:
        line = str(index_user_map[user_index])+',' + str(value)
    else:
        line += ',' + str(value)

    #f.write(line+"\n")

print(line)

result = df.groupby('user_id')['rating'].count().sort_values(ascending=True).head()
print(result)

n_users = df.user_id.nunique()
n_items = df.item_id.nunique()

grouped_by_user.filter(lambda x: x['rating'].count() > 1000)
print('n_users',n_users)
print(grouped_by_user.user_id.nunique().sum())

ratings = pd.DataFrame(df.groupby('user_id')['rating'].mean())
ratings['num of ratings'] = pd.DataFrame(df.groupby('user_id')['rating'].count())

'''

'''
plt.figure(figsize=(10,4))
ratings['num of ratings'].hist(bins=20)

plt.figure(figsize=(10,6))
ratings['rating'].hist(bins=20)

sns.jointplot(x='rating',y='num of ratings',data=ratings,alpha=0.5)

plt.show()

'''

''' 
from sklearn.model_selection import train_test_split
train_data, test_data = train_test_split(df, test_size=0.25)


train_data_matrix = np.zeros((n_users, n_items))
for line in train_data.itertuples():
    train_data_matrix[line[1]-1, line[2]-1] = line[3]

test_data_matrix = np.zeros((n_users, n_items))
for line in test_data.itertuples():
    test_data_matrix[line[1]-1, line[2]-1] = line[3]


from sklearn.metrics.pairwise import pairwise_distances
user_similarity = pairwise_distances(train_data_matrix, metric='cosine')






def generate_prediction_matrix(ratings, similarity, type='user'):
    if type == 'user':
        mean_user_rating = ratings.mean(axis=1)
        print(ratings)
        #You use np.newaxis so that mean_user_rating has same format as ratings
        ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
        pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
    elif type == 'item':
        pred = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
    return pred



user_prediction = generate_prediction_matrix(train_data_matrix, user_similarity, type='user')

from sklearn.metrics import mean_squared_error
from math import sqrt
def rmse(prediction, ground_truth):
    prediction = prediction[ground_truth.nonzero()].flatten()
    #print('prediction[ground_truth.nonzero()]',prediction[ground_truth.nonzero()])
    ground_truth = ground_truth[ground_truth.nonzero()].flatten()
    return sqrt(mean_squared_error(prediction, ground_truth))


print('User-based CF RMSE: ' + str(rmse(user_prediction, test_data_matrix)) )
#print(user_prediction)
#input("Press Enter to END...")
'''
'''
train_data_matrix = np.zeros((n_users, n_items))
for line in train_data.itertuples():

    user_id=line[1]
    item_id=line[2]
    rating = line[3]
    train_data_matrix[user_index_map[user_id], item_index_map[item_id]] = rating

test_data_matrix = np.zeros((n_users, n_items))
for line in test_data.itertuples():
    user_id = line[1]
    item_id = line[2]
    rating = line[3]
    test_data_matrix[user_index_map[user_id], item_index_map[item_id]] = rating
'''