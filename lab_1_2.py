import surprise
from collections import defaultdict

k = 4
films_count = 5
id = input('Enter user ID: ')

data = surprise.Dataset.load_builtin('ml-100k')

trainset = data.build_full_trainset()
sim_options = {'name': 'cosine', 'user_based': True, 'min_support': films_count}
algo = surprise.KNNBaseline(k=k, sim_options=sim_options)
algo.fit(trainset)

testset = trainset.build_anti_testset()
testset = filter(lambda x: x[0] == id, testset)

predictions = algo.test(testset)

top_n = defaultdict(list)
for uid, iid, _, est, _ in predictions:
    top_n[uid].append((iid, round(est, 3)))

for uid, user_ratings in top_n.items():
    user_ratings.sort(key=lambda x: x[1], reverse=True)
    top_n[uid] = user_ratings[:5]

file_name = surprise.get_dataset_dir() + '/ml-100k/ml-100k/u.item'
item = {}

with open(file_name, 'r') as f:
    for line in f:
        line = line.split('|')
        item[line[0]] = (line[1], line[2])

print(f'User {id}:')

for movie_id, rating in top_n[id]:
    print(str(movie_id) + "\t" + str(rating) + "\t" + str(item[movie_id]))