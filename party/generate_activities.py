import json

activities = [[".*习近平在正定.*", "习近平在正定"], [".+", "学习强国APP学习"]]
json.dump(activities, open('重要活动.json', 'w'), ensure_ascii=False)
print(json.load(open('重要活动.json')))
