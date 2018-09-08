
'''
The User class the holds all the properties per user
and stat results
'''


class User(object):

    def __init__(self, user_id):
        self.id = user_id
        #self.constrain_flag = 1
        '''
        for the possible items get:
        1 the map item-rating
        2 the map of top_item-rating
        2 the satisfaction_factor that s = SUM(Ratings of top Items)
        '''
        self.map_possible_items_ratings = {}
        self.map_top_items_ratings = {}  #:todo where this is used
        self.satisfaction_factor = -1  #:todo


        # self.possible_items_list = []
        # self.recommended_item = None
        # selfelf.sum_of_top_ratings = None

