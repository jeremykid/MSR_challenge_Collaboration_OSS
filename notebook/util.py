import pickle
import pandas as pd
import numpy as np
from tqdm import tqdm

def remove_alias_authors(project_output_dict):
    '''
    remove alias
    Input: project_output_dict with project_url -> commit -> author
    Output: project_output_dict's commits with remove alias authors.
    '''
    with tqdm(total=len(list(project_output_dict.keys()))) as pbar:
        for project_url, test_project_commit in project_output_dict.items():
            remove_alias_dict = {}
            for commit, value in test_project_commit.items():
                [author_name, author_email] = project_output_dict[project_url][commit]['author'].split('<')
                # Get Author name, email and email prefix
                project_output_dict[project_url][commit]['author_name'] = author_name
                project_output_dict[project_url][commit]['author_email'] = author_email
                project_output_dict[project_url][commit]['author_prefix'] = author_email.split('@')[0]

                if author_email in remove_alias_dict:
                    remove_alias_dict[author_email].append(author_name)
                else:
                    remove_alias_dict[author_email] = []

            # Find if there is any duplicates in merge author name and email prefix
            for commit, value in test_project_commit.items():
                [author_name, author_email] = project_output_dict[project_url][commit]['author'].split('<')
                author_prefix = author_email.split('@')[0]
                if author_name in remove_alias_dict[author_email] or author_prefix in in remove_alias_dict[author_email]:
                    project_output_dict[project_url][commit]['author_name'] = remove_alias_dict[author_email][0]

            # Find if there is any duplicates in author names but with different email
            remove_alias_dict = {}
            for commit, value in test_project_commit.items():
                [author_name, author_email] = project_output_dict[project_url][commit]['author'].split('<')
                if author_name in remove_alias_dict:
                    remove_alias_dict[author_name].append(author_email)
                else:
                    remove_alias_dict[author_name] = []

            # Merge alias with the same author_email
            for commit, value in test_project_commit.items():
                [author_name, author_email] = project_output_dict[project_url][commit]['author'].split('<')
                if project_output_dict[project_url][commit]['author_name'] in remove_alias_dict[author_name]:
                project_output_dict[project_url][commit]['author_email'] = remove_alias_dict[author_name][0]
        pbar.update(1)
    return project_output_dict

def assign_classification(df):
    
    '''
    Input: Dataframe with change_file column
    Return: Dataframe with new file_type
        S: Source Code
        D: Documentation
        T: Tests
        B: Build Files
        O: Other
    '''
    
    df = df[~df['change_file'].isna()]
    df['file_type'] = 'O'

    source_file_extensions = ["\.c", "\.cc", ".sh", ".cpp", '.ts', '.css', '.html', '\.m',
                              # ".C",  ".CPP",  ".C++",  
                              # ".c++",
                              ".java",  ".pl",  ".rb",  ".php",  ".pm",  ".py",  ".sql",
                              ".js", ]
    regex_string = [extension+'$' for extension in source_file_extensions]
    regex_string = '|'.join(regex_string)
    # df[df['change_file'].str.contains(regex_string)].shape
    df.loc[df['change_file'].str.contains(regex_string, case=False), 'file_type'] = 'S'

    df.loc[df['change_file'].str.contains('doxygen$|.tex$|.txt$|^INSTALL$|^README.*$|^FILES$|^TODO$|^AUTHORS$', regex=True), 'file_type'] = 'D'
    df.loc[df['change_file'].str.contains('^.*test.*$|^.*\\.t$'), 'file_type'] = 'T'

    build_file_extensions = ["Makefile" , "makefile", "build.xml" ,
    "Makefile.global", "Makefile.inc" , "configure" , "configure.in" ,
    "aclocal.m4" ,"config.guess" ,"config.sub" ,"config.h", '.conf'
    ,"install-sh" ,"bootstrap.sh" ,"configure.ac" ,"config.status"
    ,"config.sub" ,"Makefile.am","Makefile.in"]
    regex_string = [extension+'$' for extension in build_file_extensions]
    regex_string = '|'.join(regex_string)
    df.loc[df['change_file'].str.contains(regex_string), 'file_type'] = 'B'
    return df