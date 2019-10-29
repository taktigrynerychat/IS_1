import json
import csv
from math import sqrt

def csvRead(path, int_flag = False):
    with open(path) as csv_file:
        reader = csv.reader(csv_file, delimiter=',', skipinitialspace=True)
        next(reader)
        if (int_flag == False):
            return {rows[0]: rows[1:] for rows in reader}
        else:
            return {rows[0]: list(map(int, rows[1:])) for rows in reader}

def getMovieTitles():
    with open('data/data.csv') as data:
        data_csv_reader = csv.reader(data, delimiter=',', skipinitialspace=True)
        return next(data_csv_reader)[1:]

def getAvg(user_ratings):
    rated = list(filter(lambda x: x != -1, user_ratings))
    return round(sum(rated) / len(rated), 3)

def getSim(ratings, input_user):
    sim = {}
    for user_id in ratings:
        if user_id == input_user:
            continue
        user_ratings = ratings[user_id]

        sum_1 = 0
        sum_2 = 0
        sum_3 = 0

        for i in range(len(input_user_ratings)):
            if input_user_ratings[i] == -1 or user_ratings[i] == -1:
                continue
            sum_1 += input_user_ratings[i] * user_ratings[i]
            sum_2 += input_user_ratings[i] ** 2
            sum_3 += user_ratings[i] ** 2

        sim[user_id] = round(sum_1 / sqrt(sum_2) / sqrt(sum_3), 3)
    return sim

def getNearest(sorted_sim, movie_idx, k = 4):
    nearest = []
    counter = 0
    for user in sorted_sim:
        if counter == k:
            break
        if data[user][movie_idx] != -1:
            nearest.append(user)
        counter += 1
    return nearest

def getRui(movie_idx):
    sum_1 = 0
    sum_2 = 0

    for v in getNearest(sorted_sim, movie_idx):
        sum_1 += sim[v] * (data[v][movie_idx] - getAvg(data[v]))
        sum_2 += abs(sim[v])
    return round(getAvg(input_user_ratings) + sum_1 / sum_2, 3)

def getContextCoefficient(movie_idx):
    coefficient = 1

    for v in getNearest(sorted_sim, movie_idx):
        if context_place[v][movie_idx] == 'h':
            coefficient += 0.01
        else:
            coefficient -= 0.01

        if context_day[v][movie_idx] == 'Sat' or context_day[v][movie_idx] == 'Sun':
            coefficient += 0.01
        else:
            coefficient -= 0.01

    return coefficient

def getRecommendations():
    task_1 = {}
    task_2 = {}

    for movie_idx in range(len(input_user_ratings)):
        if input_user_ratings[movie_idx] != -1:
            continue

        task_1[movies[movie_idx]] = getRui(movie_idx)
        task_2[movies[movie_idx]] = round(task_1[movies[movie_idx]] * getContextCoefficient(movie_idx), 3)

    sorted_movies = list(sorted(task_2.items(), key=lambda kv: kv[1], reverse=True))[0]
    # return {'User': input_user, '1': task_1, '2': task_2}
    return {'User': input_user, '1': task_1, '2': {sorted_movies[0]: sorted_movies[1]}}

#########################################################################################################

data = csvRead('data/data.csv', True)
context_day = csvRead('data/context_day.csv')
context_place = csvRead('data/context_place.csv')
movies = getMovieTitles()

input_user_id = input('enter user id > ')
input_user = f'User {input_user_id}'
if input_user not in data:
    print(f'{input_user} not found')
    quit()

input_user_ratings = data[input_user]

sim = getSim(data, input_user)
sorted_sim = list(map(lambda x: x[0], sorted(sim.items(), key=lambda kv: kv[1], reverse=True)))

rec = getRecommendations()

with open(f'result.json', 'w') as outfile:
    json.dump(rec, outfile, indent=4)

print(rec)
