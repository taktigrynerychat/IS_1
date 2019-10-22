import math
import operator
import models.data_model as dm


class Recommendations:

    def __init__(self):
        self.allData = dm.Data()
        self.k = 4

    def getSim(self, user_1: int, user_2: int):
        sum_1 = 0
        sum_2 = 0
        sum_3 = 0
        for i in range(len(self.allData.data[0])):
            if self.allData.data[user_1][i] != -1 and self.allData.data[user_2][i] != -1:
                sum_1 += self.allData.data[user_1][i] * self.allData.data[user_2][i]
                sum_2 += self.allData.data[user_1][i] ** 2
                sum_3 += self.allData.data[user_2][i] ** 2
        return sum_1 / (math.sqrt(sum_2) * math.sqrt(sum_3))

    def getSimilar(self, user_idx):
        result = []
        for i in range(0, len(self.allData.data)):
            if user_idx != i:
                result.append((i, self.getSim(user_idx, i)))
        result = sorted(result, key=operator.itemgetter(1), reverse=True)
        return result

    def getAvg(self, user_idx):
        sum = 0
        count = 0
        for score in self.allData.data[user_idx]:
            if score != -1:
                sum += score
                count += 1
        return sum / count

    def getRui(self, user_idx, film_idx, k):
        sum_1 = 0
        sum_2 = 0
        r_u = self.getAvg(user_idx)
        similar = self.getSimilar(user_idx)

        counter = 0
        for user in similar:
            if counter == k:
                break
            if self.allData.data[user[0]][film_idx] != -1:
                r_v = self.getAvg(user[0])
                sum_1 += user[1] * ((self.allData.data[user[0]][film_idx]) - r_v)
                sum_2 += math.fabs(user[1])
                counter += 1

        return r_u + sum_1 / sum_2

    def getRecommendations(self):
        best = {}
        scores = {}
        result = []
        for user_idx in range(len(self.allData.data)):
            task_1 = {}
            for film_idx in range(len(self.allData.data[user_idx])):
                if self.allData.data[user_idx][film_idx] == -1:
                    task_1["movie " + str(film_idx + 1)] = round(self.getRui(user_idx, film_idx, self.k), 3)
                    if not (user_idx + 1 in scores):
                        scores[user_idx + 1] = {}
                    scores[user_idx + 1]["movie " + str(film_idx + 1)] = round(self.getRui(user_idx, film_idx, self.k),
                                                                               3)
            task_2 = {}
            for user_s in self.getSimilar(user_idx):
                if user_idx + 1 in best:
                    break
                for film_idx in range(len(self.allData.data[user_idx])):
                    if self.allData.data[user_idx][film_idx] == -1 and self.allData.context_place[user_s[0]][
                        film_idx] == " h" and \
                            (self.allData.context_day[user_s[0]][film_idx] == " Sat" or
                             self.allData.context_day[user_s[0]][film_idx] == " Sun") and \
                            self.allData.data[user_s[0]][film_idx] > self.getAvg(user_s[0]):
                        best[user_idx + 1] = "movie: " + str(film_idx + 1)
                        task_2["movie " + str(film_idx + 1)] = float(scores[user_idx + 1]['movie ' + str(film_idx + 1)])
                        break
            result.append({'user': user_idx + 1, 1: task_1, 2: task_2})
        return result
