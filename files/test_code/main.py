from files.test_code import slfunc as sl
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

raw_data_dir = 'files/1_raw_data/'

data_inp = pd.read_csv(raw_data_dir + 'dt', index_col='user')
# print(test_data.iloc[1])


sim_mtrx = cosine_similarity(data_inp)
all_users = data_inp.index.values - 1

#groups = grpgen.sim_group_sof(sim_mtrx, all_users, 5, -10)

r1 = {1: {'m1': 5, 'm2': 4, 'm3': 3, 'm4': 2},
      2: {'m1': 2, 'm2': 3, 'm7': 5, 'm4': 5},  
      3: {'m1': 1, 'm2': 2, 'm3': 3, 'm6': 4}
      }

r2=sl.select_top_items(1,r1)

print('sim_mtrx')
print(type(sim_mtrx[0][0]))
print('r2')
print(r2)


#stuff = [1,1,1,2,2,2,3,3, 3]
#for subset in itertools.combinations(stuff, 3):
#    print(subset)

#stuff = ['10','1','2']
#for subset in itertools.product(stuff, repeat=3):
#    print(subset)
#combinations_with_replacement()