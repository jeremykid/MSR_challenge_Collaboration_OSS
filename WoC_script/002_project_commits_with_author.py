
import oscar
import csv
import pickle

def extract_commit_message(commits_data):
    author_timestamp, commit_timestamp = 0, 0
    author, commiter = '', ''
    commit_temp_list = commits_data.split('\n')
    for temp in commit_temp_list:
        # print (temp)
        if temp.split(' ')[0] == 'author':
            author = ' '.join(temp.split(' ')[1:-2])
            author_timestamp = temp.split(' ')[-2]
        elif temp.split(' ')[0] == 'committer':
            commiter = ' '.join(temp.split(' ')[1:-2])
            commit_timestamp = temp.split(' ')[-2]
    commit_message = ' '.join(commit_temp_list[3:])
    return author, author_timestamp, commiter, commit_timestamp, commit_message

# project_name = 'nvaccess_scons'

# project_name = 'EricWang12_garbage-classifier'

with open('./project_multi_author_url_python.pickle',"rb") as f:
    project_dict = pickle.load(f)    

project_output_dict = {}
count = 0
project_names = list(project_dict.keys())[:20000]

# for project_name, value in project_dict.items():
for project_name in project_names:
    project_obj = oscar.Project(project_name)
    # project_obj = oscar.Project(project_name)
    url = project_obj.url.decode('utf-8', 'ignore').strip('\n')
    data_dict = {}
    if count %100 == 0:
        print (count)
    count+=1
    for commit in project_obj.commits:
        commits_data = commit.data.decode('utf-8', 'ignore')
        try:
            author, author_timestamp, commiter, commit_timestamp, commit_message = extract_commit_message(commits_data)
            result = {
                'author': commit.author.decode('utf-8', 'ignore'),
                'commit_timestamp': commit_timestamp,
                'changed_file_names': []
            }
            changed_file_names = []
            for changed_file_name in commit.changed_file_names:
                changed_file_name = changed_file_name.decode('utf-8', 'ignore')
                # if changed_file_name[-2:] == 'py':
                changed_file_names.append(changed_file_name)
            result['changed_file_names'] = changed_file_names
            data_dict[str(commit)] = result
        except:
            continue
    project_output_dict[url] = data_dict

for project_url, test_project_commit in project_output_dict.items():
    remove_alias_dict = {}
    for commit, value in test_project_commit.items():
        [author_name, author_email] = project_output_dict[project_url][commit]['author'].split('<', 1)
        project_output_dict[project_url][commit]['author_name'] = author_name
        project_output_dict[project_url][commit]['author_email'] = author_email
        project_output_dict[project_url][commit]['author_prefix'] = author_email.split('@')[0]

        if author_email in remove_alias_dict:
            remove_alias_dict[author_email].append(author_name)
        else:
            remove_alias_dict[author_email] = []
    
    for commit, value in test_project_commit.items():
        [author_name, author_email] = project_output_dict[project_url][commit]['author'].split('<', 1)
        author_prefix = author_email.split('@')[0]
        if author_name in remove_alias_dict[author_email] or author_prefix in in remove_alias_dict[author_email]:
            project_output_dict[project_url][commit]['author_name'] = remove_alias_dict[author_email][0]

    remove_alias_dict = {}
    for commit, value in test_project_commit.items():
        [author_name, author_email] = project_output_dict[project_url][commit]['author'].split('<', 1)
        if author_name in remove_alias_dict:
            remove_alias_dict[author_name].append(author_email)
        else:
            remove_alias_dict[author_name] = []
            
    for commit, value in test_project_commit.items():
        [author_name, author_email] = project_output_dict[project_url][commit]['author'].split('<', 1)
        if project_output_dict[project_url][commit]['author_name'] in remove_alias_dict[author_name]:
            project_output_dict[project_url][commit]['author_email'] = remove_alias_dict[author_name][0]

data_list = []
for url, value in project_output_dict.items():
    project_set = set()
    for commit, commit_information in value.items():
        author = commit_information['author_email']
        for file_name in commit_information['changed_file_names']:
            project_set.add((url, author, file_name, commit))
    data_list.extend(list(project_set))

all_author_names = set()
# with tqdm(total=1000) as pbar:
for url, value in project_output_dict.items():
    for commit, commit_information in value.items():
        all_author_names.add((url, commit_information['author']))
#         pbar.update(1)
print ('before alias:', len(all_author_names))

all_author_names = set()
# with tqdm(total=1000) as pbar:
for url, value in project_output_dict.items():
    for commit, commit_information in value.items():
        all_author_names.add((url, commit_information['author_email']))
        # pbar.update(1)
print ('after alias:', len(all_author_names))

with open('./py_project_commit_author_files_20000.pickle',"wb") as f:
    pickle.dump(data_list ,f)