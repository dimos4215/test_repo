import pandas as pd
from entities.User import User

'''
this class handles the loading of the raw files
into objects
'''


class Datasource:

    def __init__(self, utility_matrix_dir, constrain_matrix_dir):
        self.dir = utility_matrix_dir
        self.con_dir = constrain_matrix_dir
        self.dataframe = 'empty'
        self.constrains = 'empty'
        self.load_df()
        self.load_constrains()
        self.userslist = []
        self.item_map = {}
        self.user_map = {}

    def load_df(self):
        '''
        Loads the utility matrix
        '''
        # self.df = pd.read_csv(self.dir)
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
            self.user_map[ind] = User(u)
            ind += 1
        print('all users')
        print(self.userslist)

    def get_items(self):
        '''
        Loads the items from the utility matrix
        indexed based on columns
        '''
        ind = 0
        for u in self.dataframe:
            if u != 'user':
                self.item_map[u] = ind
                ind += 1
        print('all items')
        print(self.item_map)


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
