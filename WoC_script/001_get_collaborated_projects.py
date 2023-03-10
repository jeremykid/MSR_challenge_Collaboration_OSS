
import oscar
import csv
import pickle
'''

1st step: get 5000 projects from WoC maps P2c

zcat /da?_data/basemaps/gz/P2cFullU*.s | cut -d\; -f 1 | uniq | /home/hindle1/public/bin/choosen.py 5000 > commits_P2c_5000.txt 
zcat /da?_data/basemaps/gz/P2cFullU*.s | cut -d\; -f 1 | uniq > commits_P2c_all.txt
zcat /da?_data/basemaps/gz/P2cFullU*.s | cut -d\; -f 1 | uniq | wc -l

2nd step: run filter get project with github url > project_url.csv

python3 list_all_project_url.py

3rd step: 

Use github API to get issues but most of them does not have issues. 

Total  107737122 projects

'''


import pymongo
client = pymongo.MongoClient("mongodb://da1.eecs.utk.edu/")

db = client["WoC"]                                                    
coll = db["P_metadata.U"]

data_list = {}

dataset = coll.find({"NumAuthors" : { "$gt" : 1 }, "NumCommits": {"$gt":2} }, no_cursor_timeout=True)
# print (len(dataset))
for data in dataset:
    project_name = data['ProjectID']
    project_obj = oscar.Project(project_name)
    # print (project_obj.author_names)
    # if project_obj.url
    try:
        url = project_obj.url.decode('utf-8', 'ignore').strip('\n')
    except:
        continue
    if 'github' in url:
        if 'FileInfo' in data and 'Python' in data['FileInfo'''].keys():
            data_list[project_name] = {
                'NumAuthors': data['NumAuthors'],
                'url': url,
                'EarliestCommitDate': data['EarliestCommitDate'],
                'LatestCommitDate': data['LatestCommitDate']
            }

with open('./project_multi_author_url_python.pickle',"wb") as f:
    pickle.dump(data_list ,f)    