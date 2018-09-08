import itertools
import numpy as np
import os

import Upini_thesis_project.entities.GroupOfUsers
from Upini_thesis_project.entities import GroupOfUsers

'''
It takes the index_to_user_obj_map and for each user based on the constrain matrix returns for each user the
available objects
'''


def load_possible_items(users, constrain_matrix, dataframe):
    constrain_flag = 0

    for i in users:
        temp = constrain_matrix.loc[users[i].id, :]

        for item in temp[(temp != constrain_flag)].keys():
            rating = dataframe.loc[users[i].id, item]
            users[i].map_possible_items_ratings[item] = rating
            #users[i].possible_items_list.append(item) :todo remove list


'''
1.Iterate over all groups 
2.Get the available items of each user of each group
3.Get a shorted dict for each user with the top items (to user object)
4.Calculate the factor for the satisfaction of each user (to user object)

'''


def select_top_items(number_of_top_items, all_users_map, groups_map): #:Done

    n = number_of_top_items
    for group_id in groups_map:

        for user_id in groups_map[group_id].users:
            user_obj = all_users_map[user_id]
            tmp_dict = user_obj.map_possible_items_ratings
            user_satisfaction_factor=0

            top = {k: tmp_dict[k] for k in sorted(tmp_dict, key=lambda k: -tmp_dict[k])[:n]}

            for item in top:
                user_satisfaction_factor += top[item]

            user_obj.map_top_items_ratings = dict(top)
            user_obj.satisfaction_factor = user_satisfaction_factor




'''
1.Iterate over all groups 
2.Iterate over all users of each group
3.Get top K items of each user and create a list with the unique recommendation items for the group 

'''


def create_group_recommendation_list_of_available_items(groups_map, all_users_map): #:Done
    for group_id in groups_map:

        tmp_pool_of_recommendable_items = []
        for user_id in groups_map[group_id].users:
            user_top_items_list = all_users_map[user_id].map_top_items_ratings.keys()

            for item in user_top_items_list:
                tmp_pool_of_recommendable_items.append(item)

        groups_map[group_id].rlist_of_items = list(set(tmp_pool_of_recommendable_items))



'''
1.Generate all the permutations of items
2.Add combination only if it does not exist (filter symmetric combinations)
'''


def combinations_generator(list, repeat):
    # https://www.mathplanet.com/education/algebra-2/discrete-mathematics-and-probability/permutations-and-combinations
    item_combination_map = {}

    for item_combination in itertools.combinations(list, repeat): #:todo changed permutation to combination
        item_combination_map[item_combination] = ''

    return item_combination_map


'''
1.Generate all the permutations of items
'''


def combinations_generator_raw(list2, repeat):
    return itertools.permutations(list2, repeat)


'''
back up
----==============(original)==============----
def combinations_generator(list, repeat):
    # https://www.mathplanet.com/education/algebra-2/discrete-mathematics-and-probability/permutations-and-combinations
    item_combination_list = []
    for item_combination in itertools.permutations(list, repeat):
        if item_combination not in item_combination_list:
            item_combination_list.append(item_combination)
    return item_combination_list

'''

'''
gets a list of unique items and returns  a hashmap of item->index
'''


def entity_to_index_map(list):
    map_object = {}
    index = 0
    for i in list:
        map_object[i] = index
        index += 1
    return map_object


'''
gets a list of unique items and returns  a hashmap of index -> item
'''


def index_to_entity_map(list):
    map_object = {}
    index = 0
    for i in list:
        map_object[index] = i
        index += 1
    return map_object


'''
Recommender: Populate utility matrix initially from raw data using the config file
'''


def utility_matrix_populate(matrix, user_index, item_index, data, config_file):
    '''

    :param matrix: an existing matrix with zero values
    :param user_index: dictionary that maps each user_id to an array index
    :param item_index: dictionary that maps each item_id to an array index
    :param data: the dataframe from the raw file(filtered) with user,item,rating format
    :param config_file: contains the info of the entity position in the dataframe (data)
    :return: populated utility matrix
    '''
    for line in data.itertuples():
        user_id = line[config_file.csv_r_ind['user_id']]
        item_id = line[config_file.csv_r_ind['item_id']]
        rating = line[config_file.csv_r_ind['rating']]
        matrix[user_index[user_id], item_index[item_id]] = rating

    return matrix


'''
Recommender: For the export of the of the 2 files required for the constrain process
'''


def export_array_to_csv_dataframe(dir, pred_array, test_array, index_to_item_dict, idex_to_user_dic):
    '''
    :param dir: directory of expoirted files
    :param pred_array: np array that contains the predicted values
    :param test_array: np array that contains the test values
    :param index_to_item_dict: dictionary that gives item_id from the array column index
    :param idex_to_user_dic: dictionary that gives user_id from the array row index
    :return: nothing
    '''
    if os.path.exists(dir):
        os.remove(dir)
        os.remove(dir + "_constrains")

    fp = open(dir, "a")
    fc = open(dir + "_constrains", "a")

    line = 'user'
    for item_index, value in np.ndenumerate(pred_array[0, :]):
        line += ',' + str(index_to_item_dict[item_index[0]])

    fp.write(line)
    fc.write(line)

    for user_index, items_list in enumerate(pred_array):
        line = "\n" + str(idex_to_user_dic[user_index])

        for item_index, value in enumerate(items_list):
            line += ',' + str(value)

        fp.write(line)

    for user_index, items_list in enumerate(test_array):
        line = "\n" + str(idex_to_user_dic[user_index])

        for item_index, value in enumerate(items_list):
            line += ',' + str(value)

        fc.write(line)

    return
