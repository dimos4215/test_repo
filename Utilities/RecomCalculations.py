from sklearn.metrics import mean_squared_error
from math import sqrt
import numpy as np
'''
Recommender: Generate the predictions from the initial utility matrix and the similarity matrix
'''


def generate_prediction_matrix(initial_utility_matrix, entity_similarity_matrix, recommendation_type='user'):
    '''
    :param initial_utility_matrix: the utility matrix as it was loaded from the raw data
    :param entity_similarity_matrix: the table that contains the similarity between users
    :param recommendation_type: select user for user-user or item for item collaborative filtering default = 'user'
    :return: a fully completed utility matrix with calculated values
    '''

    if recommendation_type == 'user':
        '''
        1. For each user calculate average rating behaviour.. 
        2. Convert average rating shape by adding a dimension m-> m x 1
        3. Calculate rating difference rating-mean_rating
        4. Calculate the product of the entity_similarity_matrix matrix of users with normalized 
           initial_utility_matrix(ratings_diff) row-> column and sum to calculate each rating 
        5. Calculate normalization factor of each predicted rating for each movie
        6.Calculate matrix with predictions
        '''
        mean_user_rating = initial_utility_matrix.mean(axis=1)
        mean_user_rating_dim = mean_user_rating[:, np.newaxis]
        ratings_diff = (initial_utility_matrix - mean_user_rating_dim)
        table_product = np.dot(entity_similarity_matrix, ratings_diff)
        normalizing_factor = np.array([np.abs(entity_similarity_matrix).sum(axis=1)]).T
        matrix_of_predicted_ratings = mean_user_rating_dim + (table_product / normalizing_factor)

    elif recommendation_type == 'item':
        table_product = np.dot(initial_utility_matrix, entity_similarity_matrix)
        normalizing_factor = np.array([np.abs(entity_similarity_matrix).sum(axis=1)])
        matrix_of_predicted_ratings = table_product / normalizing_factor

    else:
        return []
    return matrix_of_predicted_ratings


'''
Recommender: Metric to calculate Recommender accuracy
'''


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
    predicted_values = matrix_with_predictions[indexes_of_test_values]  # (Flatten?).flatten()
    test_values = matrix_with_test_data[indexes_of_test_values]  # .flatten()

    return sqrt(mean_squared_error(predicted_values, test_values))
