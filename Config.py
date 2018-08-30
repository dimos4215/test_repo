class Config:

    def __init__(self):

        '''
        dataset directory
        log result file directory - dynamically generated based on test settings
        '''
        self.dataset_dir = '/home/dimos/PycharmProjects/Py_projects/Upini_thesis_project/files/1_raw_data/movielens/u.data'



        self.log_dir=''

        self.min_number_of_rated_items = 21
        self.test_size = 0.25
        '''
        Imported csv files have the format user_id,item_id,rating.
        The rec_csv_read_indexes idfentifies the position of each entity
        '''
        self.csv_r_ind = {'user_id': 1, 'item_id': 2, 'rating': 3}

        self.dataframe_dir = '/home/dimos/PycharmProjects/Py_projects/Upini_thesis_project/Utilities/test'
        self.constrain_dir = '/home/dimos/PycharmProjects/Py_projects/Upini_thesis_project/Utilities/test_constrains'
        # self.dataframe_dir = 'files/1_raw_data/dt'
        # self.constrain_dir = 'files/1_raw_data/constrains'
        '''
        ->group_size : set how many users are contained in a group
        ->number_of_top_items: the number of top K items that would be recommendable to a user 
        from all the available items
        -> rec_repeatability_of_item : is the max number of users that can get the same item
        '''
        self.group_size = 2
        self.number_of_top_items = 3
        self.rec_repeatability_of_item = 1
        '''
        options for fairness_measure
        1.least_misery
        2.variance
        3.min_max_ratio
        '''
        self.fairness_measure = 'least_misery'

        self.log_file_name()

    def __str__(self):

        string = '=======================TEST SETTINGS======================='
        for prop in self.__dict__:
            if prop != 'csv_r_ind':
                string += '\n' + prop + ' : ' + str(self.__dict__[prop])

        string += '\n' + '===========================================================' + '\n'
        return string

    def log_file_name(self):

        string = '/home/dimos/PycharmProjects/Py_projects/Upini_thesis_project/files/2_processed/log_'

        string += 'grp_sz_' + str(self.group_size)
        string += '_top_it_' + str(self.number_of_top_items)
        string += '_item_rep_' + str(self.rec_repeatability_of_item)

        string += '.txt'
        self.log_dir = string

