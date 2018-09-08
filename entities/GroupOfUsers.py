'''
The User_Group class the holds all the properties per Group
and stat results
'''


class GroupOfUsers:

    def __init__(self, group_id, user_list):
        self.id = group_id
        self.users = user_list
        self.user_map = {}

        self.rlist_of_items = []
        '''
        self.result_obj contains:
        :keys the item combination
        :params 
        '''
        self.result_obj = {}
        self.best_combination = {}

    # def set_users(self, userlist):
    #     self.users = userlist
