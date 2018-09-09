from Upini_thesis_project.Config import Config
from Upini_thesis_project.Utilities.Datasource import Datasource
from Upini_thesis_project.entities.GroupGenerator import GroupGenerator
from Upini_thesis_project.Utilities import Calculations, Utils
from Upini_thesis_project.Utilities.GreedyTrain import optimize_greedy
from time import sleep
from Upini_thesis_project.Utilities.Logger import Logger
import numpy as np

Export_data_for_optimization_analysis = False
Multirun = True

boost_factor_min = 1.0
boost_factor_max = 1.35
boost_factor_stp = 0.05
coverage_factor_min = 0.0
coverage_factor_max = 2.1
coverage_factor_stp = 0.4
ratings_factor_min = 0.0
ratings_factor_max = 1.1
ratings_factor_stp = 3.0

# Load Settings and Start Logging process
cfg = Config()
log = Logger(cfg)


log.log_task('Loading data from recommender system')
dataset = Datasource(cfg.dataframe_dir,cfg.constrain_dir)
dataset.get_users()
dataset.get_items()
item_stats = dataset.items_stats_map
all_users_map = dataset.index_to_user_obj_map


log.log_task('Load for each user the available')
Utils.load_possible_items(all_users_map, dataset.constrains, dataset.dataframe)


log.log_task('Generate groups of users')
group = GroupGenerator(dataset, cfg.group_size)

if cfg.group_type == 'similar':
    group.generate_similar_group()
elif cfg.group_type == 'dissimilar':
    group.generate_dissimilar_group()
elif cfg.group_type == 'random':
    group.generate_random_group()


log.log_task('Load for each user the top items')
Utils.select_top_items(cfg.number_of_top_items, all_users_map, group.group_map)


log.log_task('Generate for its group the list of recommendable items')
Utils.create_group_recommendation_list_of_available_items(group.group_map, all_users_map)
sleep(0.3)

print('==================Calculations======================================')


log.log_task('combination_test_brute')
Calculations.combination_test_brute(group.group_map, all_users_map, log, cfg) #:todo change
sleep(0.1)



if Multirun:
    log.log_task('Multirun_test_greedy')
    for boost_factor in np.arange(boost_factor_min, boost_factor_max, boost_factor_stp):
        for coverage_factor in np.arange(coverage_factor_min, coverage_factor_max, coverage_factor_stp):
            for ratings_factor in np.arange(ratings_factor_min, ratings_factor_max, ratings_factor_stp):
                print('boost_factor:',boost_factor,'coverage_factor:',coverage_factor,'ratings_factor:',ratings_factor)
                cfg.boost_factor = boost_factor
                cfg.greedy_coverage_factor = coverage_factor
                cfg.greedy_ratings_factor = ratings_factor


                Calculations.combination_test_greedy(group.group_map, all_users_map, log, cfg)
                Calculations.greedy_algorith_deviation(group.group_map, log, cfg)
                sleep(0.1)

else:
    log.log_task('combination_test_greedy')
    Calculations.combination_test_greedy(group.group_map, all_users_map, log, cfg) #:todo change
    Calculations.greedy_algorith_deviation(group.group_map, log)

if Export_data_for_optimization_analysis:
    log.log_task('optimize_greedy')
    optimize_greedy(group.group_map, all_users_map, log, cfg) #:todo change
    sleep(0.1)



log.log_task('top_combination_analysis')
Calculations.top_combination_analysis(group.group_map, item_stats, log,all_users_map) #:todo change

log.end()
