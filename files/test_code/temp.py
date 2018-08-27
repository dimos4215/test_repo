import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

raw_data_dir = 'files/1_raw_data/'

# column_names = ['user_id', 'item_id', 'rating', 'timestamp']
# df = pd.read_csv(raw_data_dir + 'u.data', sep='\t', names=column_names)

# df.head()

# print(df.head())

# movie_titles = pd.read_csv(raw_data_dir + 'Movie_Id_Titles', )
# movie_titles.head()

# print(movie_titles.head())

# df = pd.merge(df, movie_titles, on='item_id')
# print(df.head())
# moviemat = df.pivot_table(index='user_id',columns='title',values='rating')
# print (moviemat.head())
test_data = pd.read_csv(raw_data_dir + 'dt', index_col='user')
# print(test_data.iloc[1])


result = cosine_similarity(test_data)
all_users = test_data.index.values-1
grp_table = test_data.iloc[1]
# print(list(set(var)-set([1,2,3])))

#print(list(set([40, 2, 3, 4]) - set([30, 2, 3]))[0])
# print( result[ list[set(var)-set([1,2])][0] ])


l = [10, 20, 30, 40, 50]

#print(l.index(max([l[i] for i in [2, 3]])))




#init loop

count = 0
available_users = list(set(all_users))
used_users = []
while (count < 9 and len(available_users)>0):

    print ('The step is:', count)
    user1 = all_users[available_users[0]]
    used_users.append(user1)
    available_users = list(set(all_users) - set(used_users))
    temp_l = list(result[user1])
    for i in used_users:
        temp_l[i] = -1
    res = temp_l.index(max(temp_l))
    used_users.append(res)


    print('user1', user1)
    print('res', res)
    print('available_users', len(available_users))

    count = count + 1




print ("Good bye!")


available_users = list(set(all_users) - set(used_users))

print('all_users',all_users)
print('available_users',len(available_users))

user1 = all_users[available_users[0]]
print('user1',user1)
used_users.append(user1)




print('used_users ', used_users)

available_users = list(set(all_users) - set(used_users))
print('available_users',available_users)

temp_l = list(result[user1])
print('temp_l',temp_l)


for i in used_users:
    temp_l[i]=-1



res= temp_l.index(max(temp_l))

print('res',res)
#################################################################################################
#v2 main

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

raw_data_dir = 'files/1_raw_data/'

test_data = pd.read_csv(raw_data_dir + 'dt', index_col='user')
# print(test_data.iloc[1])


result = cosine_similarity(test_data)
all_users = test_data.index.values - 1
grp_table = test_data.iloc[1]
# print(list(set(var)-set([1,2,3])))

# print(list(set([40, 2, 3, 4]) - set([30, 2, 3]))[0])
# print( result[ list[set(var)-set([1,2])][0] ])


#l = [10, 20, 30, 40, 50]

# print(l.index(max([l[i] for i in [2, 3]])))


# init loop

group_number = 0
# grp_tmp = []
grp_fnl = {}
grp_size = 5
available_users = list(set(all_users))
used_users = []
used_flag_val= -1

while len(available_users) > 0:

    # init group creation
    print('group_number:', group_number)
    grp_tmp = []
    user1 = all_users[available_users[0]]
    grp_tmp.append(user1)
    used_users.append(user1)
    available_users = list(set(all_users) - set(used_users))
    temp_l = list(result[user1])

    for i in used_users:
        temp_l[i] = used_flag_val

    for j in range(0, grp_size):
        print('j', j)
        res = temp_l.index(max(temp_l))
        grp_tmp.append(res)
        temp_l[res] = used_flag_val
        used_users.append(res)
        available_users = list(set(all_users) - set(used_users))

    # print('user1', user1)
    # print('resus', res)
    # print('available_users', available_users)
    print('grp_tmp', grp_tmp)
    print('group_map', grp_fnl)

    grp_fnl[group_number] = grp_tmp
    group_number += 1

print('Good bye!')
print('group_map')
print(grp_fnl)