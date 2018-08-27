
'''
The User class the holds all the properties per user
and stat results
'''


class User(object):

    def __init__(self, user_id):
        self.id = user_id
        self.constrain_flag = 1
        self.possible_items = {}
        self.possible_items_list = []
        self.recommended_item = None
        self.sum_of_top_ratings = None

