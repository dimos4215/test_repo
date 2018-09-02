from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import pairwise_distances
from Upini_thesis_project.Utilities.Utils import entity_to_index_map,utility_matrix_populate,index_to_entity_map,export_array_to_csv_dataframe
from Upini_thesis_project.Utilities.Calculations import generate_prediction_matrix,calculate_RMSE
import numpy as np


def collaborative_filtering(raw_data_dataframe,cf):

    df = raw_data_dataframe


    print('=============Initialize Recommender=============')

    '''
    1.Get number of unique users and items
    2.Get list of unique users and items
    3.Generate dictionary with indexes
    '''

    n_users = df.user_id.nunique()
    n_items = df.item_id.nunique()
    print('n_users', n_users)
    print('n_items', n_items,'\n')

    user_list = df.user_id.unique()
    item_list = df.item_id.unique()

    user_index_map = entity_to_index_map(user_list)
    item_index_map = entity_to_index_map(item_list)

    index_user_map = index_to_entity_map(user_list)
    index_item_map = index_to_entity_map(item_list)

    '''
    1. Split data to test and trainset
    2. Populate 2 utility matrixes (train/test)
    3. Calculate user similarity matrix
    '''


    print('Split dataset to train/test:', 1-cf.test_size,'/',cf.test_size)
    train_data, test_data = train_test_split(df, test_size=cf.test_size)

    train_data_matrix = np.zeros((n_users, n_items))
    test_data_matrix = np.zeros((n_users, n_items))

    train_data_matrix = utility_matrix_populate(train_data_matrix, user_index_map, item_index_map, train_data, cf)
    test_data_matrix = utility_matrix_populate(train_data_matrix, user_index_map, item_index_map, train_data, cf)

    print('Calculate User-similarity Matrix')
    user_similarity = pairwise_distances(train_data_matrix, metric='cosine')

    '''
    1. Generate prediction matrix for users
    2. Test accuracy
    '''
    print('Calculate Predicted Values Matrix')
    user_prediction = generate_prediction_matrix(train_data_matrix, user_similarity)

    print('Calculate RMSE','\n')
    rmse_error = calculate_RMSE(user_prediction, test_data_matrix)

    print('User-based CF RMSE: ' + str(rmse_error))

    export_array_to_csv_dataframe(cf.dataframe_fname, user_prediction, test_data_matrix, index_item_map, index_user_map)
