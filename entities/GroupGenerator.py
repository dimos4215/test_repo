from entities.GroupOfUsers import GroupOfUsers
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class GroupGenerator:

    def __init__(self, data_obj, group_size=1):
        self.grp_size = group_size
        self.all_users = list(data_obj.user_map.keys())
        self.available_users = self.all_users
        self.group_map = {}
        self.used_users = []
        self.sim_matrix = cosine_similarity(data_obj.dataframe)
        self.group_number = 0
        self.used_flag_val = -1000

    def generate_similar_group(self):

        while len(self.available_users) > 0:
            '''
            Initialize the creation of each group by creating a temp group_list that holds the user
            indexes and by selecting an initial user(seed) from a list of available users
            '''
            grp_tmp = []
            # initial_user = self.available_users[rd.randint(0,len(self.available_users))] random initial user
            initial_user = self.available_users[0]
            '''
            1.Add user to temp group
            2.Remove user from available users
            3.Add user to used users list
            '''
            grp_tmp.append(initial_user)
            self.available_users.remove(initial_user)
            self.used_users.append(initial_user)
            '''
            4.Get the row from the similarity matrix for the seed user
            5.Put the used_flag_val in the indexes of used users
            '''
            user_similarity_row = list(self.sim_matrix[initial_user])
            for i in self.used_users:
                user_similarity_row[i] = self.used_flag_val
            '''
            Get the rest users of the group by selecting the index of the max/min val
            of the seed user's similarity matrix row
            '''

            for j in range(0, self.grp_size - 1):
                next_user = user_similarity_row.index(max(user_similarity_row))
                grp_tmp.append(next_user)

                user_similarity_row[next_user] = self.used_flag_val
                self.used_users.append(next_user)
                if len(self.available_users) > 0:
                    self.available_users.remove(next_user)
                else:
                    break

            self.group_map[self.group_number] = GroupOfUsers(self.group_number, grp_tmp)
            self.group_number += 1

        print('sim_groups finished')


    def generate_dissimilar_group(self):

        self.used_flag_val = abs(self.used_flag_val)

        while len(self.available_users) > 0:
            '''
            Initialize the creation of each group by creating a temp group_list that holds the user
            indexes and by selecting an initial user(seed) from a list of available users
            '''
            grp_tmp = []
            # initial_user = self.available_users[rd.randint(0,len(self.available_users))] random initial user
            initial_user = self.available_users[0]
            '''
            1.Add user to temp group
            2.Remove user from available users
            3.Add user to used users list
            '''
            grp_tmp.append(initial_user)
            self.available_users.remove(initial_user)
            self.used_users.append(initial_user)
            '''
            4.Get the row from the similarity matrix for the seed user
            5.Put the used_flag_val in the indexes of used users
            '''
            user_similarity_row = list(self.sim_matrix[initial_user])
            for i in self.used_users:
                user_similarity_row[i] = self.used_flag_val
            '''
            Get the rest users of the group: 
                1.by selecting the index of the min val of the seed user's similarity matrix row
                2.by adding the next_users similarity matrix row to the existing
                3.resetting user index values with self.used_flag_val
            '''

            for j in range(0, self.grp_size - 1):
                next_user = user_similarity_row.index(min(user_similarity_row))
                grp_tmp.append(next_user)

                user_similarity_row = list(np.add(user_similarity_row, self.sim_matrix[next_user]))
                user_similarity_row[next_user] = self.used_flag_val
                self.used_users.append(next_user)
                if len(self.available_users) > 0:
                    self.available_users.remove(next_user)
                else:
                    break

            self.group_map[self.group_number] = GroupOfUsers(self.group_number, grp_tmp)
            self.group_number += 1

        print('dis_groups finished')

