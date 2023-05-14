import os
import pandas as pd

def get_data_year(path, year):
    file_name = [file for file in os.listdir(path) if file[0:4] == str(year)][0]
    df = pd.read_csv(path + file_name)
    return df

def prepare_data_leesin(major_regions, drop_irrelevant, drop_large_nulls):
    dfs = []
    for year in range(2015, 2024):
        df_year = get_data_year('../data/', year)
    
        df_lee = (
        df_year[
            (df_year['position'] == 'jng') 
            & (df_year['champion'] == 'Lee Sin') 
            & (df_year['league'].isin(major_regions))
        ]
        .drop(columns=drop_irrelevant)
        .drop(columns=drop_large_nulls)
    )
        dfs.append(df_lee.copy())

    dfs = pd.concat(dfs, axis=0).reset_index(drop=True)
    return dfs