"""
below are described the steps of the design process:

1.Set up data input:
    1.1 for data input there must be a completed utility matrix from a traditional reccomender system.(User - user colab filtering)
    1.2 for each user we have a list of the available movies that can be reccomended

2.Set up the interface for parameter input (possibly GUI):
    2.1 Set type of group creation (simmilar,dissimilar,random)
    2.2 Set size of group
    2.3 Set contrains (how many times an item can be given)
    2.4 Set Cost function

3.Calculations per group:
    3.1 Generate user-item combinations
    3.2 filter Constrained combinations :\
        3.2.1 Users that have seen a movie should not re-see iter
        3.2.2 Combinations where an item appears more than the numeric constrain of 2.3 section should be filtered
    3.3 after trying combinations get best user-item combinations
    3.4(1) Calculate user satisfaction!!!

4.Total Calculations:
    4.1 for all groups have the cost result
    4.2 for all users have the cost for the itam that they got vs the one they liked the most
    4.3 prediction accuracy of recommender vs current for each user

5. Extras:
    5.1 add a neural network for the user ordering selection
    visualize for different groups and cfg the results
"""
from typing import Dict, Any

'''
import modules
'''
from Upini_thesis_project.Config import Config
from Upini_thesis_project.Utilities.Datasource import Datasource
from Upini_thesis_project.entities.GroupGenerator import GroupGenerator
from Upini_thesis_project.Utilities import Calculations, Utils
import os
from time import sleep
from Upini_thesis_project.Utilities.Logger import Logger




# load data intro memory
cfg = Config()

log = Logger(cfg)

print('cfg.log_dir',cfg.log_dir)
log.log_task('dataset')

#dataset = Datasource(os.path.relpath(cfg.dataframe_dir), os.path.relpath(cfg.constrain_dir))
dataset = Datasource(cfg.dataframe_dir,cfg.constrain_dir)

dataset.get_users()
dataset.get_items()

item_stats = dataset.items_stats_map

map_alluser_obj = dataset.index_to_user_obj_map



#load for each user the available items
log.log_task('load_possible_items')
Utils.load_possible_items(map_alluser_obj, dataset.constrains, dataset.dataframe)


#generate group

log.log_task('GroupGenerator')
group = GroupGenerator(dataset, cfg.group_size)
group.generate_dissimilar_group()

log.log_task('select_top_items')
Utils.select_top_items(cfg.number_of_top_items, map_alluser_obj, group.group_map)





log.log_task('create_group_recommendation_list')
Utils.create_group_recommendation_list(group.group_map, cfg.rec_repeatability_of_item)


sleep(0.1)
print('==================Calculations======================================')


log.log_task('combination_test2')
Calculations.combination_test(group.group_map, map_alluser_obj, log)
sleep(0.1)




log.log_task('user_satisfaction_prep')
Calculations.user_satisfaction_prep(group.group_map, map_alluser_obj)


log.log_task('group_feature_gereration')
Calculations.group_feature_gereration(group.group_map)


log.log_task('get_top_combination')
Calculations.get_top_combination(group.group_map, cfg.fairness_measure, item_stats, log)


log.end()

#:todo remove design temp code

'''
backup 

import time

#init_time = time.clock()

# load data intro memory
cfg = Config()

log = Logger(cfg)

print('cfg.log_dir',cfg.log_dir)
log.log_task('dataset')

dataset = Datasource(os.path.relpath(cfg.dataframe_dir), os.path.relpath(cfg.constrain_dir))

dataset.get_users()
dataset.get_items()

index_to_user_obj_map = dataset.index_to_user_obj_map


#load_complete = time.clock()

#print('load time:',load_complete-init_time)

#load for each user the available items
log.log_task('load_possible_items')
Utils.load_possible_items(index_to_user_obj_map, dataset.constrains, dataset.dataframe)


#generate group
#generategroup_start = time.clock()
log.log_task('GroupGenerator')
group = GroupGenerator(dataset, cfg.group_size)

group.generate_dissimilar_group()

#generategroup_end = time.clock()

#print('generategroup time:',generategroup_end-generategroup_start)

#select_top_items_start = time.clock()

log.log_task('select_top_items')
Utils.select_top_items(cfg.number_of_top_items, index_to_user_obj_map, group.group_map)


#select_top_items_end= time.clock()

#print('select_top_items time:',select_top_items_end-select_top_items_start)


#create_group_recommendation_list_start= time.clock()
log.log_task('create_group_recommendation_list')
Utils.create_group_recommendation_list(group.group_map, cfg.rec_repeatability_of_item)
#print(group.group_map[0].rlist_of_items)



#create_group_recommendation_list_end= time.clock()

#print('create_group_recommendation_list time:',create_group_recommendation_list_end-create_group_recommendation_list_start)
sleep(0.1)
print('==================Calculations======================================')

#calcs_start= time.clock()
log.log_task('combination_test')
Calculations.combination_test(group.group_map, index_to_user_obj_map)

#calc1= time.clock()
sleep(0.1)
#print('combination_test time:',calc1-calcs_start)



log.log_task('user_satisfaction_prep')
Calculations.user_satisfaction_prep(group.group_map, index_to_user_obj_map)
#calc2= time.clock()
#print('user_satisfaction_prep time:',calc2-calc1)

log.log_task('group_feature_gereration')
Calculations.group_feature_gereration(group.group_map)
#calc3= time.clock()
#print('group_feature_gereration time:',calc3-calc2)

log.log_task('get_top_combination')
Calculations.get_top_combination(group.group_map, cfg.fairness_measure)
#calc4= time.clock()
#print('get_top_combination time:',calc4-calc3)

#print('Total Time',time.clock()-init_time)

log.end()
'''