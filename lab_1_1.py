import json
import models.recommendations_model as rm

rec = rm.Recommendations()
user = rec.getRecommendations()

id = int(input("enter user id > ")) - 1
result_json = json.dumps(user[id])

json_file = open("result.json",'w')
json_file.write(result_json)
json_file.close()
