The Script in WoC codes:

1st Step: 

001_get_collaborated_projects.py: 

Get collaborated projects with more than 1 authors and more than 2 commits, and 'github' in the url. 

Saved in project_multi_author_url_python.pickle

002_project_commits_with_author.py

From project_multi_author_url_python.pickle, get the 3 level maps
1st level: project
2nd level: commit
3rd level: author

Then remove alias authors

Saved in py_project_commit_author_files_20000

003_generate_ACE.py

From py_project_commit_author_files_20000, to generate author cross entropy and saved in ACE_files_20000.pickle