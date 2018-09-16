class Config:

    def __init__(self):

        '''
        Import dataset settings:
            1.dataset dir
            2.Imported csv files have the format user_id,item_id,rating.The rec_csv_read_indexes idfentifies the position of each entity

        '''
        self.dataset_dir = '/home/dimos/PycharmProjects/Py_projects/Upini_thesis_project/files/1_raw_data/movielens/u.data'
        self.csv_r_ind = {'user_id': 1, 'item_id': 2, 'rating': 3}



        '''
        Filtering data settings, Recommender split sets and show visualizations setting
        '''

        self.min_std_of_item_ratings = 0.5
        self.min_num_of_item_ratings = 50
        self.min_std_of_user_ratings = 0.1
        self.min_num_of_user_ratings = 50
        self.test_size = 0.35
        self.show_charts = False


        self.base_dataframe_dir='/home/dimos/PycharmProjects/Py_projects/Upini_thesis_project/files/2_processed/dataframes/'

        '''
        group_type Settings
                   1.similar
                   2.dissimilar
                   3.random
        '''
        self.group_type = 'dissimilar'


        '''
        Combination Test Settings:
            1.group_size : set how many users are contained in a group
            2.number_of_top_items: the number of top K items that would be recommendable to a user 
                                   from all the available items
            3.rec_repeatability_of_item : is the max number of users that can get the same item
            4.the percentage of users who have seen the item
        '''

        self.group_size = 7
        self.number_of_top_items = 3
        self.number_of_rec_items = 4
        self.threshold_cov=0.99
        self.number_of_min_covered_items = 1

        self.greedy_coverage_factor = 0.82
        self.greedy_ratings_factor = 0.09
        self.boost_factor = 1.3
        self.max_iterations = 100

        '''
        Fairness_measure Settings
            1.least_misery
            2.variance
            3.min_max_ratio
        '''
        self.fairness_measure = 'min_max_ratio'


        '''
        Dynamically generated file names
        '''
        self.log_dir = ''
        self.dataframe_fname = ''
        self.dfrm_file_name()
        self.dataframe_dir = self.dataframe_fname
        self.constrain_dir = self.dataframe_fname+'_constrains'
        # self.dataframe_dir = 'files/1_raw_data/dt'
        # self.constrain_dir = 'files/1_raw_data/constrains' #:todo remove test dirs
        self.log_file_name()

    def __str__(self):

        string = '=======================TEST SETTINGS======================='
        for prop in self.__dict__:
            if prop != 'csv_r_ind':
                string += '\n' + prop + ' : ' + str(self.__dict__[prop])

        string += '\n' + '===========================================================' + '\n'
        return string


    def dfrm_file_name(self):

        string = 'df_'
        string += 'itms_' + str(self.min_std_of_item_ratings)
        string += '_itmn_' + str(self.min_num_of_item_ratings)
        string += '_urms_' + str(self.min_std_of_user_ratings)
        string += '_urmn_' + str(self.min_num_of_user_ratings)
        string += '_split_' + str(self.test_size)

        self.dataframe_fname = self.base_dataframe_dir + string

    def log_file_name(self):

        string = '/home/dimos/PycharmProjects/Py_projects/Upini_thesis_project/files/2_processed/'
        string += self.fairness_measure
        string += '_grp_tp_' + self.group_type
        string += '_grp_sz_' + str(self.group_size)
        string += '_top_it_' + str(self.number_of_top_items)
        string += '_item_rec_' + str(self.number_of_rec_items)
        string += '_item_con_' + str(self.number_of_min_covered_items)
        string += '_userfact_' + str(self.greedy_coverage_factor)
        string += '_ratefact_' + str(self.greedy_ratings_factor)
        string += '_boostfact_' + str(self.boost_factor)

        string += '.txt'
        self.log_dir = string

