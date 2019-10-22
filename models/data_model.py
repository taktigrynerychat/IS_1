import csv

class Data:

    def __init__(self):
        self.data = []
        for i in self.csvRead('./data/data.csv'):
            self.data.append(list(map(int, i)))
        self.context_day = self.csvRead('./data/context_day.csv')
        self.context_place = self.csvRead('./data/context_place.csv')

    def csvRead(self, path):
        with open(path) as csv_file:
            data = []
            reader = csv.reader(csv_file)
            for row in reader:
                data.append(row)

        result = []
        for row in data[1:]:
            result.append(row[1:])
        return result
