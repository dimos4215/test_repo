# module
import numpy as np


def sim_group_agr(sim_matrix, all_users, grp_size, used_flag_val):
    group_number = 0
    grp_fnl = {}
    # grp_size = 5
    available_users = list(set(all_users))
    used_users = []
    # used_flag_val= -1

    while len(available_users) > 0:

        # init group creation
        print('group_number:', group_number)
        grp_tmp = []
        # random initialization needed
        user1 = all_users[available_users[0]]
        grp_tmp.append(user1)
        used_users.append(user1)
        available_users = list(set(all_users) - set(used_users))
        temp_l = list(sim_matrix[user1])

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
    return grp_fnl


##############################################################################

def sim_group_sof(sim_matrix, all_users, grp_size, used_flag_val):
    group_number = 0
    grp_fnl = {}

    available_users = list(set(all_users))
    used_users = []
    ct = 0

    while len(available_users) > 0:

        # init group creation
        print('group_number:', group_number)
        # print('len(available_users)', len(available_users))
        grp_tmp = []
        # random initialization needed
        user1 = all_users[available_users[0]]
        grp_tmp.append(user1)
        used_users.append(user1)
        available_users = list(set(all_users) - set(used_users))
        temp_l = sim_matrix[user1]

        for i in used_users:
            temp_l[i] = -abs(used_flag_val)

        for j in range(0, grp_size):
            # print('j', j)

            res = np.argmax(temp_l)
            # print('resus', res)
            print(res, '-->', temp_l)

            grp_tmp.append(res)
            temp_l[res] = -abs(used_flag_val)
            temp_l = np.add(temp_l, sim_matrix[res])
            used_users.append(res)
            available_users = list(set(all_users) - set(used_users))

        print('user1', user1)
        print('resus', res)
        print('available_users', available_users)
        print('grp_tmp', grp_tmp)
        print('group_map', grp_fnl)

        grp_fnl[group_number] = grp_tmp
        group_number += 1

    print('SOFFFFFF!')
    print('group_map')
    print(grp_fnl)
    return grp_fnl


##############################################################################

def dsm_group_sof(sim_matrix, all_users, grp_size, used_flag_val):
    group_number = 0
    grp_fnl = {}

    available_users = list(set(all_users))
    used_users = []
    ct = 0

    while len(available_users) > 0:

        # init group creation
        grp_tmp = []
        # random initialization needed
        user1 = all_users[available_users[0]]
        grp_tmp.append(user1)
        used_users.append(user1)
        available_users = list(set(all_users) - set(used_users))
        temp_l = sim_matrix[user1]

        for i in used_users:
            temp_l[i] = abs(used_flag_val)

        for j in range(0, grp_size):
            res = np.argmin(temp_l)
            grp_tmp.append(res)
            temp_l[res] = abs(used_flag_val)
            temp_l = np.add(temp_l, sim_matrix[res])
            used_users.append(res)
            available_users = list(set(all_users) - set(used_users))

        grp_fnl[group_number] = grp_tmp
        group_number += 1

    return grp_fnl
