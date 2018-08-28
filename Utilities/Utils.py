import itertools
import numpy as np

'''
It takes the user_map and for each user based on the constrain matrix returns for each user the
available objects
'''


def load_possible_items(users, constrain_matrix, dataframe):
    constrain_flag =0

    for i in users:
        temp = constrain_matrix.loc[users[i].id, :]

        for item in temp[(temp != constrain_flag)].keys():
            rating = dataframe.loc[users[i].id, item]
            users[i].possible_items[item] = rating
            users[i].possible_items_list.append(item)


'''
1.Iterate over all groups 
2.Get the availabke items of each user of each group
3.Create a dictionary for all the users of the group
4.Select top N items from each user of thr group

'''


def select_top_items(number_of_top_items, users, group):
    """
    :type group: group.group_map
    """
    n = number_of_top_items
    for group_id in group:
        all_items_of_users = {}
        for user_id in group[group_id].users:
            user_obj = users[user_id]
            all_items_of_users[user_obj.id] = user_obj.possible_items

        frl = all_items_of_users
        top_list = {}

        for i in frl:
            top_list[i] = {k: frl[i][k] for k in sorted(frl[i], key=lambda k: -frl[i][k])[:n]}

        group[group_id].top_items = top_list


'''
1.Iterate over all groups 
2.Get the top_items of each group
3.Create a list with the unique recommendation items for group
4.expand list based on the number of times an item can be given
'''


def create_group_recommendation_list(group, repeatability_of_item):
    """
    :type group: group.group_map
    """

    for group_id in group:
        user_top_choices = group[group_id].top_items
        temp_rlist_of_items = []
        for user in user_top_choices:
            for item in user_top_choices[user].keys():
                temp_rlist_of_items.append(item)

        group[group_id].rlist_of_items = list(set(temp_rlist_of_items))
        if repeatability_of_item > 1:
            for rep in range(0, repeatability_of_item):
                group[group_id].rlist_of_items += list(set(temp_rlist_of_items))


'''
1.Generate all the permutations of items
2.Add combination only if it does not exist (filter symmetric combinations)
'''


def combinations_generator(list, repeat):
    # https://www.mathplanet.com/education/algebra-2/discrete-mathematics-and-probability/permutations-and-combinations
    item_combination_map = {}
    ct= 0
    for item_combination in itertools.permutations(list, repeat):
        ct+=1
        if item_combination not in item_combination_map:
            item_combination_map[item_combination]=''
    print('number of tota combinations:',ct)
    return item_combination_map
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
