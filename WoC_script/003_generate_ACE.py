import numpy as np
import pandas as pd

data_list = pd.read_pickle('py_project_commit_author_files_20000.pickle')

def agg_ACE(x):
    temp_numpy = x.to_numpy()
    total = sum(x)
    temp_probability = temp_numpy/total
    cross_entropy = -np.sum(temp_probability * np.log(temp_probability))
    return cross_entropy

def assign_classification(df):
    df = df[~df['file_name'].isna()]
    df['file_type'] = 'O'

    source_file_extensions = ["\.c", "\.cc", ".sh", ".cpp", '.ts', '.css', '.html', '\.m', '\.swift', '.ipynb',
                              # ".C",  ".CPP",  ".C++",  
                              # ".c++",
                              ".java",  ".pl",  ".rb",  ".php",  ".pm",  ".py",  ".sql",
                              ".js", ]
    regex_string = [extension+'$' for extension in source_file_extensions]
    regex_string = '|'.join(regex_string)
    df.loc[df['file_name'].str.contains(regex_string, case=False), 'file_type'] = 'S'

    df.loc[df['file_name'].str.contains('doxygen$|.tex$|.txt$|.md$|^INSTALL$|^README.*$|^FILES$|^TODO$|^AUTHORS$|^LICENSE$', regex=True), 'file_type'] = 'D'
    df.loc[df['file_name'].str.contains('^.*test.*$|^.*\\.t$'), 'file_type'] = 'T'

    build_file_extensions = ["Makefile" , "makefile", "build.xml" ,
    "Makefile.global", "Makefile.inc" , "configure" , "configure.in" ,
    "aclocal.m4" ,"config.guess" ,"config.sub" ,"config.h", '.conf'
    ,"install-sh" ,"bootstrap.sh" ,"configure.ac" ,"config.status"
    ,"config.sub" ,"Makefile.am","Makefile.in"]
    regex_string = [extension+'$' for extension in build_file_extensions]
    regex_string = '|'.join(regex_string)
    df.loc[df['file_name'].str.contains(regex_string), 'file_type'] = 'B'
    return df

temp_df = pd.DataFrame.from_records(data_list, columns=['project_url', 'author', 'file_name', 'commit'])

temp_df = temp_df.groupby(['project_url', 'file_name', 'author']).agg({'commit': 'count'})
temp_df = temp_df.reset_index()

temp_ace =temp_df.groupby(['project_url', 'file_name']).agg({'commit':agg_ACE, 'author':'count'})
temp_ace = temp_ace.reset_index()

temp_ace = assign_classification(temp_ace)

for file_type in ['S', 'T', 'D', 'B']:
    file_temp_df = temp_ace[temp_ace['file_type'] == file_type]
    print (file_type, ':',file_temp_df[file_temp_df['author'] > 1].shape[0], '/', file_temp_df.shape[0])
    
temp_ace[temp_ace['author'] > 1].to_pickle('ACE_files_20000.pickle')