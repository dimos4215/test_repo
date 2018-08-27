class Config:

    def __init__(self):



        self.dataframe_dir = 'files/1_raw_data/dt'
        self.constrain_dir = 'files/1_raw_data/constrains'
        '''
        ->group_size : set how many users are contained in a group
        ->number_of_top_items: the number of top K items that would be recommendable to a user 
        from all the available items
        -> rec_repeatability_of_item : is the max number of users that can get the same item
        '''
        self.group_size = 3
        self.number_of_top_items = 3
        self.rec_repeatability_of_item = 2
        '''
        options for fairness_measure
        1.least_misery
        2.variance
        3.min_max_ratio
        '''
        self.fairness_measure = 'least_misery'
