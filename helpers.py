import json


bind_map = json.load(open('binds.json'))
lang_data = json.load(open('lang.json'))

lang_to_code = {}

for i in lang_data["text"]:
    lang_to_code[i["language"]] = i["code"]

