import pandas as pd
from Upini_thesis_project.entities.User import User

'''
this class handles the loading of the raw files
into objects
'''


class Datasource:

    def __init__(self, utility_matrix_dir, constrain_matrix_dir):
        '''

        :param utility_matrix_dir:
        :param constrain_matrix_dir:
        '''
        self.dir = utility_matrix_dir
        self.con_dir = constrain_matrix_dir
        self.dataframe = 'empty'
        self.constrains = 'empty'
        self.load_df()
        self.load_constrains()
        self.userslist = []
        self.item_to_index_map = {}  # maps items to indexes of arrays
        self.index_to_user_obj_map = {}  # maps user arrays indexes to user objects
        self.items_stats_map = {}  # maps object stats

    def load_df(self):
        '''
        Loads the utility matrix
        '''
        # self.df = pd.read_csv(self.dir)
        print('self.dir', self.dir)
        self.dataframe = pd.read_csv(self.dir, index_col='user')
        print("data imported!")

    def load_constrains(self):
        '''
        Loads the constrain matrix
        '''
        # self.constrains = pd.read_csv(self.con_dir)
        self.constrains = pd.read_csv(self.con_dir, index_col='user')
        print("constrains imported!")

    def get_users(self):
        '''
        Loads the users from the utility matrix
        '''
        ind = 0
        for u in self.dataframe.index:
            self.userslist.append(u)
            self.index_to_user_obj_map[ind] = User(u)
            ind += 1
        print('all users:', len(self.userslist))

    def get_items(self):
        '''
        Loads the items from the utility matrix
        indexed based on columns
        '''
        ind = 0
        for u in self.dataframe:
            if u != 'user':
                self.item_to_index_map[u] = ind
                self.items_stats_map[u] = {'number_of_groups': 0, 'number_of_times': 0}
                ind += 1
        print('all items:', len(list(self.item_to_index_map.keys())))

        # keep item stats only for items that can be given to users
        for item in self.dataframe:
            if item != 'user':
                item_availability = self.dataframe[self.dataframe[item] > 0][item].count()
                # if item_availability > 0:
                self.items_stats_map[item] = dict(availability=item_availability, number_of_times_given=0,
                                                  rating_list=[], satisfied_users=[])


'''
Test Area
'''
if __name__ == '__main__':

    raw_data_dir = 'files/1_raw_data/dt'
    con_data_dir = 'files/1_raw_data/constrains'

    imported_data = Datasource(raw_data_dir, con_data_dir)

    # imported_data.get_users()
    # imported_data.get_items()
    imported_data.load_constrains()
    print('imported_data.constrains')

    print(imported_data.constrains)

    print(imported_data.constrains.loc[[18]])

    for i in imported_data.constrains.loc[[18]]:
        print(imported_data.constrains.loc[[18]][i][18])
