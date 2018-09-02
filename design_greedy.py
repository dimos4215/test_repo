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
cfg = Config()  # init Experiment Configuration
log = Logger(cfg)  # init Experiment Logging process

print('cfg.log_dir', cfg.log_dir)

log.log_task('dataset')

'''Load data:
        1.Load User 
        2.Load Item list
        3.Load Item map that keeps statistics
        4.Load Index-User map'''
dataset = Datasource(os.path.relpath(cfg.dataframe_dir), os.path.relpath(cfg.constrain_dir))

dataset.get_users()
dataset.get_items()
item_stats = dataset.items_stats_map
map_alluser_obj = dataset.index_to_user_obj_map

# load for each user the available items
log.log_task('load_possible_items')
Utils.load_possible_items(map_alluser_obj, dataset.constrains, dataset.dataframe)

'''generate group:
        1.Init
        2.select type of groups'''
log.log_task('GroupGenerator')
group = GroupGenerator(dataset, cfg.group_size)
group.generate_dissimilar_group()

# load for each user the TOP items
log.log_task('select_top_items')
Utils.select_top_items(cfg.number_of_top_items, map_alluser_obj, group.group_map)

# load for each group the list of recommendable items
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
