from Upini_thesis_project.Utilities.Calculations import  greedy_algorith_score_function,metric_calculation
import os


def optimize_greedy(groups_map, users_map, log, conf_object):
    ratings_factor = conf_object.greedy_ratings_factor
    coverage_factor = conf_object.greedy_coverage_factor
    fairness_mes = conf_object.fairness_measure
    boost_factor = conf_object.boost_factor

    dir = '/home/dimos/PycharmProjects/Py_projects/Upini_thesis_project/files/2_processed/opt_'
    dir += fairness_mes + '_cf_'+str(coverage_factor)+'_rf_'+str(ratings_factor)+'_bf_'+str(boost_factor)
    dir += '.csv'
    if os.path.exists(dir):
        os.remove(dir)

    fp = open(dir, "a")

    line = 'item,users,ratimgs,flag'
    fp.write(line)
    for group_id in groups_map:
        users_ids = groups_map[group_id].users

        comb = groups_map[group_id].result_obj['fair_comb'][0]

        # tmp_item_stats = {}
        # tmp_item_score = {}
        # evl_item_stats = {}
        # evl_item_score = {}
        # iterations_list = []

        if comb != None:
            tmp_item_stats, tmp_item_score = greedy_item_scoring(users_ids, users_map, ratings_factor, coverage_factor)
            evl_item_stats, evl_item_score = reference_item_scoring(users_ids, comb, users_map, ratings_factor, coverage_factor)

            for item in tmp_item_stats:
                top_choices_flag = 0
                if item in evl_item_stats:
                    top_choices_flag = 1

                line = '\n' + str(item) + ',' + str(tmp_item_stats[item]['users'])
                line += ',' + str(metric_calculation(tmp_item_stats[item]['ratings'], fairness_mes))
                line += ',' + str(top_choices_flag)

                fp.write(line)




def greedy_item_scoring(users_ids, users_map, ratings_factor, coverage_factor):
    tmp_grd_item_stats = {}
    tmp_item_score = {}

    for user_id in users_ids:
        user_obj = users_map[user_id]
        item_ratings = user_obj.map_top_items_ratings
        item_iteration(users_ids, item_ratings, tmp_grd_item_stats)

    for item in tmp_grd_item_stats:
        tmp_item_score[item] = greedy_algorith_score_function(ratings_factor, coverage_factor,
                                                              tmp_grd_item_stats[item]['users'],
                                                              tmp_grd_item_stats[item]['ratings'])

    return tmp_grd_item_stats, tmp_item_score


def item_iteration(users_ids, item_ratings, tmp_item_stats):  # done
    for item in item_ratings:
        if item not in tmp_item_stats:
            tmp_item_stats[item] = {'users': 1 / len(users_ids), 'ratings': [item_ratings[item]]}
        else:
            tmp_item_stats[item]['users'] += 1 / len(users_ids)
            tmp_item_stats[item]['ratings'].append(item_ratings[item])


def reference_item_scoring(users_ids, comb, users_map, ratings_factor, coverage_factor):
    tmp_item_score = {}
    tmp_item_stats = {}
    for item in comb:
        for user_id in users_ids:
            user_obj = users_map[user_id]
            item_ratings = user_obj.map_top_items_ratings

            if item in item_ratings:
                if item not in tmp_item_stats:
                    tmp_item_stats[item] = {'users': 1 / len(users_ids), 'ratings': [item_ratings[item]]}
                else:
                    tmp_item_stats[item]['users'] += 1 / len(users_ids)
                    tmp_item_stats[item]['ratings'].append(item_ratings[item])


    for item in tmp_item_stats:
        tmp_item_score[item] = greedy_algorith_score_function(ratings_factor, coverage_factor,
                                                              tmp_item_stats[item]['users'],
                                                              tmp_item_stats[item]['ratings'])

    return tmp_item_stats, tmp_item_score

