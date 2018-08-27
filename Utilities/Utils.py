import itertools

'''
It takes the user_map and for each user based on the constrain matrix returns for each user the
available objects
'''


def load_possible_items(users, constrain_matrix, dataframe):
    constrain_flag = 1

    for i in users:
        temp = constrain_matrix.loc[users[i].id, :]

        for item in temp[(temp == constrain_flag)].keys():
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
    item_combination_list = []
    for item_combination in itertools.permutations(list, repeat):
        if item_combination not in item_combination_list:
            item_combination_list.append(item_combination)
    return item_combination_list

'''
gets a list of unique items and returns  a hashmap of item->index
'''
def list_map(list):
    map_object= {}
    index = 0
    for i in list:
        map_object[i]=index
        index+=1
    return map_object