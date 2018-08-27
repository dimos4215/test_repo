from Utilities import Utils
import numpy as np

NUM_CORE = 4  # set to the number of cores you want to use


'''
1.Iterate over all groups
2.Generate combinations based on the number of users
3.Iterate over each combination and check if the item should be given to each user based on the list of available objects
4.Keep valid combinations and their reting in an dictionary for further processing
'''


def combination_test(groups, usersobj):

    for group_id in groups:
        users_group_index = groups[group_id].users
        number_of_users = len(users_group_index)
        item_combination_list = Utils.combinations_generator(groups[group_id].rlist_of_items, number_of_users)

        for comb in item_combination_list:
            metric = 0
            rating_list = []
            pass_flag = True

            for user_combination_index, item in enumerate(comb):
                temp_user_obj = usersobj[users_group_index[user_combination_index]]

                if item in temp_user_obj.possible_items_list:
                    rating = temp_user_obj.possible_items[item]
                    metric += rating
                    rating_list.append(rating)

                else:
                    pass_flag = not pass_flag
                    break

            if pass_flag:
                groups[group_id].result_obj[comb] = {'rating_list': rating_list}




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



def get_top_combination(groups,fairness_measure):

    for group_id in groups:
        group_combinations = groups[group_id].result_obj

        best_comb = None
        best_score = -1111111

        for comb in group_combinations:
            score = group_combinations[comb][fairness_measure]

            if best_score < score:
                best_score = score
                best_comb = comb

        groups[group_id].best_combination[best_comb] = best_score

        print('-->group_id',group_id,'best_comb',best_comb,'best_score',best_score)




