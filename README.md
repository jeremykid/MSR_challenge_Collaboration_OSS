# An Empirical Study to Investigate Collaboration Among Developers in Open Source Software (OSS)

## Introduction

We present our challenge paper [here](https://msr2023-challenge.hotcrp.com/paper/6?cap=hcav6MHcVLkyejDfgegVtxLKcEkWB)
which aims to investigate how developers collaborate in Open Source Software (OSS).

## Research Question1 (RQ1)

> Generate the datasets for ACE collaboration in RQ1 following the list of steps

- Get the collaborated projects with more than one author, two commits, and includes github in it's url. The script is saved in 001_get_collaborated_projects.py

- Get the 3 level maps from these generated data which includes the project at the first level, commits at second level and authors at third level. Once this is gotten, you simply remove the author alias. The script file is saved in 002_project_commits_with_author.py

- Generate the Authors Cross Entropy using the script 003_generate_ACE.py and results saved in ACE_files_20000.pickle

## Research Question2 (RQ1)

> Generate datasets for Lexical analysis in RQ

- Filter through preprocessed datasets as available in RQ1 in the pickle file py_project_commit_author_files_20000 for only python files with multiple contributors.

- Count the percentage tokens added in commits and compare them against the frequency of the overall tokens