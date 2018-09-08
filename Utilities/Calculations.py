from Upini_thesis_project.Utilities import Utils
import numpy as np
from sklearn.metrics import mean_squared_error
from math import sqrt
from Upini_thesis_project.Utilities.ProgressBar import ProgressBar

'''
1.Iterate over all groups
2.Generate combinations based on the number of users
3.Iterate over each combination and check if the item should be given to each user based on the list of available objects
4.Keep valid combinations and their reting in an dictionary for further processing
'''


def combination_test_brute(groups_map, users_map, log, conf_object):
    size_of_recommendation_list = conf_object.number_of_rec_items
    threshold_cov = conf_object.threshold_cov
    fairness_mes = conf_object.fairness_measure
    min_covered_items = conf_object.number_of_min_covered_items
    number_of_all_groups = len(list(groups_map.keys()))
    log.log_static_metric('number_of_all_groups', number_of_all_groups)
    log.log_static_metric('fairness_mes', fairness_mes)

    progress = ProgressBar(number_of_all_groups, fmt=ProgressBar.FULL)

    print('number_of_all_groups:', number_of_all_groups)  #:todo ADD LOGGING OF GENERATED/valid combinations

    for group_id in groups_map:
        users_ids = groups_map[group_id].users
        item_combination_list = Utils.combinations_generator(groups_map[group_id].rlist_of_items,
                                                             size_of_recommendation_list)

        progress.current += 1
        progress()

        total_combinations = 0
        valid_combinations = 0
        best_comb = None
        best_score = -1

        fair_comb = None
        fair_score = -1

        for comb in item_combination_list:
            metric = {}
            total_combinations += 1
            tmp_satisfaction_map = {}
            tmp_usr_coverage_map = {}
            for user_id in users_ids:
                tmp_satisfaction_map[user_id] = 0
                tmp_usr_coverage_map[user_id] = 0

            for item in comb:
                item_avail = 0

                for user_id in users_ids:
                    user_obj = users_map[user_id]

                    if item not in user_obj.map_possible_items_ratings:
                        item_avail += 1

                    elif item in user_obj.map_top_items_ratings:
                        rating = user_obj.map_top_items_ratings[item]
                        tmp_satisfaction_map[user_id] += rating / user_obj.satisfaction_factor
                        tmp_usr_coverage_map[user_id] += 1

                if item_avail / len(users_ids) > threshold_cov:
                    break

            result_list = list(tmp_satisfaction_map.values())
            metric[fairness_mes] = metric_calculation(result_list,fairness_mes)

            if user_coverage_check(tmp_usr_coverage_map, min_covered_items):
                valid_combinations += 1
                if fair_score < metric[fairness_mes]:
                    fair_score = metric[fairness_mes]
                    fair_comb = comb

            if best_score < metric[fairness_mes]:
                best_score = metric[fairness_mes]
                best_comb = comb

        groups_map[group_id].result_obj['best_comb'] = [best_comb, best_score]
        groups_map[group_id].result_obj['fair_comb'] = [fair_comb, fair_score]
        # LOG result
        header = 'group_id,total_combinations,valid_combinations'
        key = str(group_id) + ',' + str(total_combinations)
        log.log_dynamic_metric(header, key, valid_combinations)

    progress.done()


def metric_calculation(satisfaction_list,fairness_mes):
    if fairness_mes == 'least_misery':
        return min(satisfaction_list)
    elif fairness_mes == 'variance':
        return 1 / np.var(satisfaction_list)
    elif fairness_mes == 'min_max_ratio':
        return min(satisfaction_list) / max(satisfaction_list)


def user_coverage_check(coverage_map, min_covered_items):
    for user in coverage_map:
        covered_items = coverage_map[user]
        if covered_items < min_covered_items:
            return False
    return True



def combination_test_greedy(groups_map, users_map, log, conf_object):
    n = conf_object.number_of_rec_items
    ratings_factor = conf_object.greedy_ratings_factor
    coverage_factor = conf_object.greedy_coverage_factor
    fairness_mes = conf_object.fairness_measure
    min_covered_items = conf_object.number_of_min_covered_items
    boost_factor = conf_object.boost_factor
    max_iterations = conf_object.max_iterations

    log.log_static_metric('min_covered_items', min_covered_items)
    log.log_static_metric('ratings_factor', ratings_factor)
    log.log_static_metric('coverage_factor', coverage_factor)


    for group_id in groups_map:
        users_ids = groups_map[group_id].users
        tmp_item_stats = {}
        tmp_item_score = {}

        #GENERATE Initial Combination
        for user_id in users_ids:
            user_obj = users_map[user_id]
            item_ratings = user_obj.map_top_items_ratings

            for item in item_ratings:
                if item not in tmp_item_stats:
                    tmp_item_stats[item] = {'users': 1 / len(users_ids), 'ratings': [item_ratings[item]]}

                else:
                    tmp_item_stats[item]['users'] += 1 / len(users_ids)
                    tmp_item_stats[item]['ratings'].append(item_ratings[item])

        for item in tmp_item_stats:
            tmp_item_score[item] = ratings_factor * tmp_item_stats[item]['users']
            tmp_item_score[item] += coverage_factor * np.mean(tmp_item_stats[item]['ratings'])

        # ITERATE until constrain reached
        score = -1
        iterations=0
        while score < 0 and max_iterations>iterations:
            iterations+=1
            for item in users_map[user_id].map_top_items_ratings:
                tmp_item_score[item] = tmp_item_score[item] * boost_factor
                top = {k: tmp_item_score[k] for k in sorted(tmp_item_score, key=lambda k: -tmp_item_score[k])[:n]}
                comb = list(top.keys())
                score, user_id = calculate_combination_score(comb, users_ids, users_map, min_covered_items,
                                                             fairness_mes)
        groups_map[group_id].result_obj['greedy_comb'] = [comb, score]



def calculate_combination_score(comb,users_ids,users_map,min_covered_items,fairness_mes):
    tmp_satisfaction_map = {}
    tmp_usr_coverage_map = {}
    for user_id in users_ids:
        tmp_satisfaction_map[user_id] = 0
        tmp_usr_coverage_map[user_id] = 0

    for item in comb:
        for user_id in users_ids:
            user_obj = users_map[user_id]

            if item in user_obj.map_top_items_ratings:
                rating = user_obj.map_top_items_ratings[item]
                tmp_satisfaction_map[user_id] += rating / user_obj.satisfaction_factor
                tmp_usr_coverage_map[user_id] += 1

    result_list = list(tmp_satisfaction_map.values())
    # score = 1 / np.var(result_list)
    if user_coverage_check(tmp_usr_coverage_map, min_covered_items):
        score = metric_calculation(result_list, fairness_mes)
        return score,None
    else:
        return -1,min(tmp_usr_coverage_map, key=tmp_usr_coverage_map.get)


def combination_results(groups_map,  log):
    combination_type_list= []
    for comb_type in groups_map[0].result_obj:
        combination_type_list.append(comb_type)
        header = 'Combination Result\ngroup_id'
        header += ',' + comb_type + '_score'

    for group_id in groups_map:
        group_combinations = groups_map[group_id].result_obj
        comb_score = None
        for comb_type in combination_type_list:
            if comb_score == None:
                comb_score = str(group_combinations[comb_type][1])
            else:
                comb_score += ','+str(group_combinations[comb_type][1])

        log.log_dynamic_metric(header, group_id, comb_score)



def top_combination_analysis(groups_map, item_stats, log, users_map):
    for comb_type in groups_map[0].result_obj:

        for group_id in groups_map:
            users_ids = groups_map[group_id].users
            group_combinations = groups_map[group_id].result_obj
            comb = group_combinations[comb_type][0]

            if comb == None:
                break

            for item in comb:
                item_stats[item]['number_of_times_given'] += 1
                satisfied_users = 0
                for user_id in users_ids:
                    user_obj = users_map[user_id]

                    '''
                    if top items +1 satisfied user else just rating score
                    '''
                    if item in user_obj.map_top_items_ratings:
                        item_stats[item]['rating_list'].append(user_obj.map_top_items_ratings[item])
                        satisfied_users += 1
                    elif item in user_obj.map_possible_items_ratings:
                        item_stats[item]['rating_list'].append(user_obj.map_possible_items_ratings[item])

                item_stats[item]['satisfied_users'].append(satisfied_users)

        item_stats_analysis(comb_type,item_stats, log)
        item_stats_reset(item_stats)






def item_stats_analysis(calaulation_type,item_stats, log):
    # LOG result
    header = calaulation_type +'\n'
    header += 'item_id,number_of_times_given,number_of_groups_offered,average_rating,rating_variation,average_covered_users,variation_covered_users'
    for item in item_stats:
        num_of_times = item_stats[item]['number_of_times_given']
        if num_of_times > 0:
            avg_rating = np.mean(item_stats[item]['rating_list'])
            var_rating = np.var(item_stats[item]['rating_list'])
            avg_users_covered = np.mean(item_stats[item]['satisfied_users'])
            var_users_covered = np.var(item_stats[item]['satisfied_users'])
        else:
            avg_rating = 0
            var_rating = 0
            avg_users_covered = 0
            var_users_covered = 0

        key = str(item) + ',' + str(num_of_times)
        key += ',' + str(avg_rating)
        key += ',' + str(var_rating)
        key += ',' + str(avg_users_covered)

        log.log_dynamic_metric(header, key, var_users_covered)


def item_stats_reset(item_stats):
    for item in item_stats:
        item_stats[item]['number_of_times_given'] = 0
        item_stats[item]['rating_list'] = []
        item_stats[item]['satisfied_users'] = []





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
