# from Config import Config
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import pairwise_distances
from Upini_thesis_project.Utilities.Utils import list_map
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.pyplot import axis

plt.interactive(False)
sns.set_style('white')

'''
Load movielens dataset into a dataframe and merge with movie titles???
'''

data_dir = '../files/1_raw_data/movielens/'
column_names = ['user_id', 'item_id', 'rating', 'timestamp']
df = pd.read_csv(data_dir + 'u.data', sep='\t', names=column_names)
# movie_titles = pd.read_csv(data_dir+"Movie_Id_Titles")
# df = pd.merge(df,movie_titles,on='item_id')


# create new dataframe to filter user/items

min_number_of_rated_items = 5
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

print('============================================')

'''
1.Get number of unique users and items
2.Get list of unique users and items
3.Generate dictionary with indexes
'''

n_users = df.user_id.nunique()
n_items = df.item_id.nunique()
print('n_users', n_users)
print('n_items', n_items)

user_list = df.user_id.unique()
item_list = df.item_id.unique()

user_map_index = list_map(user_list)
item_map_index = list_map(item_list)

'''
1. Split data to test and trainset
2. Populate 2 utility matrixes (train/test)
3. Calculate user similarity matrix
'''

train_data, test_data = train_test_split(df, test_size=0.25)


def utility_matrix_populate(matrix, user_index, item_index, data):
    for line in data.itertuples():
        user_id = line[1]
        item_id = line[2]
        rating = line[3]
        matrix[user_index[user_id], item_index[item_id]] = rating

    return matrix


train_data_matrix = np.zeros((n_users, n_items))
test_data_matrix = np.zeros((n_users, n_items))
train_data_matrix = utility_matrix_populate(train_data_matrix, user_map_index, item_map_index, train_data)
test_data_matrix = utility_matrix_populate(train_data_matrix, user_map_index, item_map_index, train_data)

print(train_data_matrix)



user_similarity = pairwise_distances(train_data_matrix, metric='cosine')
print('user_similarity', user_similarity)
print('type user_similarity', type (user_similarity) )

print('==========================================================================')


def generate_prediction_matrix(ratings, similarity, type='user'):
    if type == 'user':

        '''
        1. For each user calculate average rating behaviour.. 
        2. Convert average rating shape by adding a dimension m-> m x 1
        3. Calculate rating difference rating-mean_rating
        4. Calculate the product of the similarity matrix of users with normalized ratings(ratings_diff) row-> column 
           and sum to calculate each rating 
        5. Calculate normalization factor of each predicted rating for each movie
        6.Calculate matrix with predictions
        '''
        mean_user_rating = ratings.mean(axis=1)
        mean_user_rating_dim = mean_user_rating[:, np.newaxis]
        ratings_diff = (ratings - mean_user_rating_dim)
        table_product = np.dot(similarity,ratings_diff)
        normalizing_factor = np.array([np.abs(similarity).sum(axis=1)]).T
        matrix_of_predicted_ratings = mean_user_rating_dim + (table_product / normalizing_factor)


    elif type == 'item':

        table_product = np.dot(ratings,similarity)
        normalizing_factor = np.array([np.abs(similarity).sum(axis=1)])
        matrix_of_predicted_ratings = table_product / normalizing_factor

    else:
        return []
    return matrix_of_predicted_ratings


'''
1. Generate prediction matrix for users
2. Test accuracy
'''
user_prediction = generate_prediction_matrix(train_data_matrix, user_similarity, type='user')
print('==============================accuracy============================================')


def calculate_RMSE(matrix_with_predictions, matrix_with_test_data):

    '''
    :param matrix_with_predictions: np_array
    :param matrix_with_test_data: np_array
    :return: RMSE

    1. Get the indexes of test values (rows-columns) from the test data matrix of the non-zero elements
    2. Get the values of the calculated ratings based on the indexes_of_test_values
    3. Get the values of the test ratings based on the indexes_of_test_values
    4. Calculate RMSE
    '''


    indexes_of_test_values = matrix_with_test_data.nonzero()
    predicted_values = matrix_with_predictions[indexes_of_test_values]# (Flatten?).flatten()
    test_values = matrix_with_test_data[indexes_of_test_values]#.flatten()
    return sqrt(mean_squared_error(predicted_values, test_values))


print('User-based CF RMSE: ' + str(calculate_RMSE(user_prediction, test_data_matrix)) )




'''
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
    train_data_matrix[user_map_index[user_id], item_map_index[item_id]] = rating

test_data_matrix = np.zeros((n_users, n_items))
for line in test_data.itertuples():
    user_id = line[1]
    item_id = line[2]
    rating = line[3]
    test_data_matrix[user_map_index[user_id], item_map_index[item_id]] = rating
'''