# import json
# with open('cnn.json', encoding="utf8") as json_data:
#     article_dict = json.load(json_data)
#     print(len(article_dict), "Articles loaded succesfully")


# with open('cnn.json', 'w', encoding="utf8") as json_data:
#     json.dump(article_dict, json_data, ensure_ascii=False, indent=2)


import json

with open("metadata2.json", encoding="utf-8") as f:
    meta2 = json.load(f)
meta2_dict = {item["source_url"]: item["title"] for item in meta2 if "source_url" in item and "title" in item}

with open("metadata.json", encoding="utf-8") as f:
    meta = json.load(f)

for item in meta:
    url = item.get("source_url")
    if url in meta2_dict:
        item["title"] = meta2_dict[url]

with open("metadata_merged.json", "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)