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
    visualize for different groups and settings the results
"""

'''
import modules
'''
from Upini_thesis_project.Config import Config
from Upini_thesis_project.Utilities.Datasource import Datasource
from Upini_thesis_project.entities.GroupGenerator import GroupGenerator
from Upini_thesis_project.Utilities import Calculations, Utils
import time
import os
from time import sleep


init_time = time.clock()

# load data intro memory
settings = Config()
imp_data = Datasource(os.path.relpath(settings.dataframe_dir), os.path.relpath(settings.constrain_dir))

imp_data.get_users()
imp_data.get_items()

user_map = imp_data.user_map


load_complete = time.clock()

print('load time:',load_complete-init_time)

#load for each user the available items
Utils.load_possible_items(user_map, imp_data.constrains, imp_data.dataframe)


#generate group
generategroup_start = time.clock()
group = GroupGenerator(imp_data, settings.group_size)

group.generate_dissimilar_group()

generategroup_end = time.clock()

print('generategroup time:',generategroup_end-generategroup_start)

select_top_items_start = time.clock()
Utils.select_top_items(settings.number_of_top_items, user_map, group.group_map)


select_top_items_end= time.clock()

print('select_top_items time:',select_top_items_end-select_top_items_start)


create_group_recommendation_list_start= time.clock()
Utils.create_group_recommendation_list(group.group_map, settings.rec_repeatability_of_item)
#print(group.group_map[0].rlist_of_items)



create_group_recommendation_list_end= time.clock()

print('create_group_recommendation_list time:',create_group_recommendation_list_end-create_group_recommendation_list_start)
sleep(0.1)
print('==================Calculations======================================')

calcs_start= time.clock()

Calculations.combination_test(group.group_map, user_map)

calc1= time.clock()
sleep(0.1)
print('combination_test time:',calc1-calcs_start)

Calculations.user_satisfaction_prep(group.group_map, user_map)
calc2= time.clock()
print('user_satisfaction_prep time:',calc2-calc1)

Calculations.group_feature_gereration(group.group_map)
calc3= time.clock()
print('group_feature_gereration time:',calc3-calc2)

Calculations.get_top_combination(group.group_map, settings.fairness_measure)
calc4= time.clock()
print('get_top_combination time:',calc4-calc3)

print('Total Time',time.clock()-init_time)