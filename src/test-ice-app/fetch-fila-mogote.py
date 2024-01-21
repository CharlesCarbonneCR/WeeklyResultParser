import json, os

jsonFolderPath = 'json'
jsonFolderPath = jsonPath = os.path.join(os.path.dirname(__file__), jsonFolderPath)

#### Get files from json folder:
for x in os.listdir(jsonFolderPath):
    if x.endswith(".json"):
        # Prints only text file present in My Folder
        print(x)


##### FETCH FILA DE MOGOTE IN THE JSON FILE
jsonPath = 'json/1-16-2024.json'
jsonPath = os.path.join(os.path.dirname(__file__), jsonPath)
print(jsonPath)

with open(jsonPath) as f:
    d = json.load(f)
    data = d['data']
    for i in data:
        if "Mogote" in i['planta']:
            print(i)