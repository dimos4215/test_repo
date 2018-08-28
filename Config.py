class Config:

    def __init__(self):

        '''
        dataset directory
        '''
        self.dataset_dir = '/home/dimos/PycharmProjects/Py_projects/Upini_thesis_project/files/1_raw_data/movielens/u.data'
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
        self.group_size = 4
        self.number_of_top_items = 3
        self.rec_repeatability_of_item = 2
        '''
        options for fairness_measure
        1.least_misery
        2.variance
        3.min_max_ratio
        '''
        self.fairness_measure = 'least_misery'

    def __str__(self):

        string = '=======================TEST SETTINGS======================='
        for prop in self.__dict__:
            if prop != 'csv_r_ind':
                string += '\n' + prop + ' : ' + str(self.__dict__[prop])

        string += '\n' + '===========================================================' + '\n'
        return string

    def __call__(self):

        string = ''
        for prop in self.__dict__:
            if prop != 'csv_r_ind':
                string += '\n' + prop + ' : ' + str(self.__dict__[prop])

        string += '\n'
        return string
