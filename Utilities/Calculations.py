from Upini_thesis_project.Utilities import Utils
import numpy as np
from sklearn.metrics import mean_squared_error
from math import sqrt
from Upini_thesis_project.Utilities.ProgressBar import ProgressBar
import sys
from collections import Counter
import itertools

NUM_CORE = 4  # set to the number of cores you want to use

'''
1.Iterate over all groups
2.Generate combinations based on the number of users
3.Iterate over each combination and check if the item should be given to each user based on the list of available objects
4.Keep valid combinations and their reting in an dictionary for further processing
'''


def combination_test(groups_map, usersobj, log):

    number_of_all_groups = len(list(groups_map.keys()))

    log.log_static_metric('number_of_all_groups', number_of_all_groups)

    progress = ProgressBar(number_of_all_groups, fmt=ProgressBar.FULL)


    print('number_of_all_groups:', number_of_all_groups)

    for group_id in groups_map:
        users_group_index = groups_map[group_id].users
        number_of_users = len(users_group_index)
        item_combination_list = Utils.combinations_generator(groups_map[group_id].rlist_of_items, number_of_users)
        progress.current += 1
        progress()
        tested_combinations = len(item_combination_list)
        log.log_static_metric('tested_combinations', tested_combinations)
        valid_combinations = 0
        for comb in item_combination_list:
            metric = 0
            rating_list = []
            pass_flag = True

            for user_group_index, item in enumerate(comb):
                temp_user_obj = usersobj[users_group_index[user_group_index]]

                if item in temp_user_obj.possible_items:
                    rating = temp_user_obj.possible_items[item]
                    metric += rating
                    rating_list.append(rating)

                else:
                    pass_flag = not pass_flag
                    break

            if pass_flag:
                groups_map[group_id].result_obj[comb] = {'rating_list': rating_list}
                valid_combinations+=1
        log.log_static_metric('valid_combinations', valid_combinations)
    progress.done()


def combination_test2(groups_map, usersobj, log) :#:todo remove combination_test2

    number_of_all_groups = len(list(groups_map.keys()))

    log.log_static_metric('number_of_all_groups', number_of_all_groups)

    progress = ProgressBar(number_of_all_groups, fmt=ProgressBar.FULL)


    print('number_of_all_groups:', number_of_all_groups)

    for group_id in groups_map:
        users_group_index = groups_map[group_id].users
        number_of_users = len(users_group_index)
        item_combination_list = Utils.combinations_generator_raw(groups_map[group_id].rlist_of_items, number_of_users)
        item_combination_map={}
        progress.current += 1
        #progress()
        #tested_combinations = len(item_combination_list)
        #log.log_static_metric('tested_combinations', tested_combinations)

        gen_comb=0
        test_comb = 0
        valid_combinations = 0
        broken_loops=0
        for comb in item_combination_list:
            #print('comb',comb)
            gen_comb+=1
            if comb in item_combination_map:
                broken_loops+=1
                break
            else:
                item_combination_map[comb]=''
                test_comb+=1
            metric = 0
            rating_list = []
            pass_flag = True

            for user_group_index, item in enumerate(comb):
                temp_user_obj = usersobj[users_group_index[user_group_index]]

                if item in temp_user_obj.possible_items:
                    rating = temp_user_obj.possible_items[item]
                    metric += rating
                    rating_list.append(rating)

                else:
                    pass_flag = not pass_flag
                    break

            if pass_flag:
                groups_map[group_id].result_obj[comb] = {'rating_list': rating_list}
                valid_combinations+=1
        log.log_static_metric('valid_combinations', valid_combinations)
        print('group_id',group_id,'gen_comb',gen_comb,'test_comb',test_comb,'valid_combinations',valid_combinations,'broken_loops',broken_loops,'item_combination_map',len(item_combination_map.keys()))
    progress.done()




def combination_test3(groups_map, usersobj, log): #:todo remove combination_test3

    number_of_all_groups = len(list(groups_map.keys()))

    log.log_static_metric('number_of_all_groups', number_of_all_groups)

    progress = ProgressBar(number_of_all_groups, fmt=ProgressBar.FULL)


    print('number_of_all_groups:', number_of_all_groups)

    for group_id in groups_map:
        users_group_index = groups_map[group_id].users
        number_of_users = len(users_group_index)


        progress.current += 1
        progress()
        #tested_combinations = len(item_combination_list)
        #log.log_static_metric('tested_combinations', tested_combinations)

        item_combination_map = {}



        gen_comb=0
        test_comb = 0
        valid_combinations = 0
        broken_loops=0
        for comb in itertools.permutations(groups_map[group_id].rlist_of_items, number_of_users):
            #print('comb',comb)
            gen_comb+=1
            if comb in item_combination_map:
                broken_loops+=1
                pass
            else:
                item_combination_map[comb]=''
                test_comb+=1
            metric = 0
            rating_list = []
            pass_flag = True

            for user_group_index, item in enumerate(comb):
                temp_user_obj = usersobj[users_group_index[user_group_index]]

                if item in temp_user_obj.possible_items:
                    rating = temp_user_obj.possible_items[item]
                    metric += rating
                    rating_list.append(rating)

                else:
                    pass_flag = not pass_flag
                    break

            if pass_flag:
                groups_map[group_id].result_obj[comb] = {'rating_list': rating_list}
                valid_combinations+=1
        log.log_static_metric('valid_combinations', valid_combinations)
        print('group_id',group_id,'gen_comb',gen_comb,'test_comb',test_comb,'valid_combinations',valid_combinations,'broken_loops',broken_loops,'item_combination_map',len(item_combination_map.keys()))
    progress.done()


 #:todo remove combination_test backup
'''
back up
    

    
====================(original)====================
def combination_test(groups, usersobj):
    number_of_all_groups = len(list(groups.keys()))

    progress = ProgressBar(number_of_all_groups, fmt=ProgressBar.FULL)

    print('number_of_all_groups:', number_of_all_groups)

    for group_id in groups:
        users_group_index = groups[group_id].users
        number_of_users = len(users_group_index)
        item_combination_list = Utils.combinations_generator(groups[group_id].rlist_of_items, number_of_users)
        progress.current += 1
        progress()

        for comb in item_combination_list:
            metric = 0
            rating_list = []
            pass_flag = True

            for user_group_index, item in enumerate(comb):
                temp_user_obj = usersobj[users_group_index[user_group_index]]

                if item in temp_user_obj.possible_items_list:
                    rating = temp_user_obj.possible_items[item]
                    metric += rating
                    rating_list.append(rating)

                else:
                    pass_flag = not pass_flag
                    break

            if pass_flag:
                groups[group_id].result_obj[comb] = {'rating_list': rating_list}

    progress.done()
    
    
====================(improvement with dict hash/ low results)====================    
def combination_test(groups, usersobj):

    number_of_all_groups = len(list(groups.keys()))

    progress = ProgressBar(number_of_all_groups, fmt=ProgressBar.FULL)

    print('number_of_all_groups:',number_of_all_groups)

    for group_id in groups:
        users_group_list = groups[group_id].users
        number_of_users = len(users_group_list)
        item_combination_list = Utils.combinations_generator(groups[group_id].rlist_of_items, number_of_users)
        progress.current += 1
        progress()

        temp_map_user_index_to_user_object = {}
        temp_map_user_index_to_user_possible_item_set= {}
        #print('group_id',group_id)
        for index in range(number_of_users):

            temp_map_user_index_to_user_object[index] = usersobj[users_group_list[index]]

        for comb in item_combination_list:
            metric = 0
            rating_list = []
            pass_flag = True



            for user_index, item in enumerate(comb):


                temp_user_obj = temp_map_user_index_to_user_object[user_index]

                if item in temp_user_obj.possible_items:
                    rating = temp_user_obj.possible_items[item]
                    metric += rating
                    rating_list.append(rating)

                else:
                    pass_flag = not pass_flag
                    break

            if pass_flag:
                groups[group_id].result_obj[comb] = {'rating_list': rating_list}


    progress.done()    
'''


def user_satisfaction_prep(groups, usersobj):
    for group_id in groups:
        users_top_items = groups[group_id].top_items
        users_group_index = groups[group_id].users

        '''
        Calculate total rating from top item list
        '''
        for g_user_index in users_group_index:
            user_id = usersobj[g_user_index].id

            item_rating = users_top_items[user_id]
            temp_sum = 0

            for item in item_rating:
                temp_sum += item_rating[item]

            usersobj[g_user_index].sum_of_top_ratings = temp_sum

        '''
        For each combination calculate the satisfaction per item/user
        '''
        group_combinations = groups[group_id].result_obj

        for comb in group_combinations:
            rating_list = group_combinations[comb]['rating_list']
            group_combinations[comb]['calculated_list'] = []

            '''
            get the total of each user and divide rating/total_sum_of_top_items
            '''
            for user_combination_index, rating in enumerate(rating_list):
                sum_of_top_ratings = usersobj[users_group_index[user_combination_index]].sum_of_top_ratings
                ratio = rating / sum_of_top_ratings
                group_combinations[comb]['calculated_list'].append(ratio)


'''
1.Iterate over all groups
2.Iterate over each combination 
3.calculate group metrics
'''


def group_feature_gereration(groups):
    for group_id in groups:
        group_combinations = groups[group_id].result_obj

        for comb in group_combinations:
            rating_list = group_combinations[comb]['calculated_list']

            group_combinations[comb]['least_misery'] = min(rating_list)
            group_combinations[comb]['variance'] = np.var(rating_list)
            group_combinations[comb]['min_max_ratio'] = min(rating_list)


def get_top_combination(groups, fairness_measure, item_stats, log):
    metric_times_item_rec='Item_id,Number_of_times_recommended'
    metric_groups_item_rec='Item_id,Number_of_groups_recommended'

    for group_id in groups:
        group_combinations = groups[group_id].result_obj

        best_comb = None
        best_score = -1111111

        stat_metric_best_comb = 'group_id_'+str(group_id)+' satisfaction'

        for comb in group_combinations:
            score = group_combinations[comb][fairness_measure]

            log.log_static_metric(stat_metric_best_comb, score)

            if best_score < score:
                best_score = score
                best_comb = comb

        item_times = Counter(best_comb)

        #print('item_times = Counter(best_comb)',item_times)
        for item in item_times:
            item_stats[item]['number_of_times']+=item_times[item]
            item_stats[item]['number_of_groups'] += 1


            log.log_dynamic_metric(metric_times_item_rec, item,item_stats[item]['number_of_times'])
            log.log_dynamic_metric(metric_groups_item_rec, item, item_stats[item]['number_of_groups'])

        groups[group_id].best_combination[best_comb] = best_score

        #print('-->group_id', group_id, 'best_comb', best_comb, 'best_score', best_score)


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
