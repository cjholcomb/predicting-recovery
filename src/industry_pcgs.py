from src.dictionaries import *
import pandas as pd
import numpy as np

def third_quarter(index):
    if index == 0:
        return False
    elif (index - 3) % 4 == 0:
        return False
    else:
        return True

def make_pcgs_files(years):
    for year in years:
        filepath = 'data/really-big-files/' + str(year) + '.q1-q4.singlefile.csv'
        df = pd.read_csv(filepath, skiprows = lambda x: third_quarter(x), low_memory = False, usecols = [0,1,2,3,4,5,6,7,8,11,12,15])
        indus_maxes = df.groupby(['area_fips', 'industry_code']).month3_emplvl.transform(max)
        df = df.loc[df.month3_emplvl == indus_maxes]
        df = df.pivot_table('month3_emplvl', 'area_fips', 'industry_code').fillna(0)
        for column in df:
            if column == '10':
                continue
            else:
                df[column] = df[column] / df['10']
        savepath = 'data/' + str(year) + 'emppcg.csv'
        df.to_csv(savepath)