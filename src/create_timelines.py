from src.dictionaries import *
import pandas as pd

def add_qtrid(df):
    df['qtrid'] = df['year'] + (df['qtr']/4)
    return df

#import one year of data to explore
def import_one(year):
    filepath = 'data/by_county' + str(year) + '.csv'
    df = pd.read_csv(filepath, dtype = schema_dict)
    df = df.drop(drop_columns, axis = 1)
    return df

#import all data into a single file
def import_all(years):
    df = import_one(years[0])
    for year in years[1:]:
        df = df.append(import_one(year))
    df = add_qtrid(df)
    return df