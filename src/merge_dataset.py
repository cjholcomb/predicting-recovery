import pandas as pd

df_political2001 = pd.read_csv('data/state-political-data.csv')
df_political2001 = df_political2001.drop(0)
df_political2001 = df_political2001.set_index('State Code')
df_population2001 = pd.read_csv('data/county-population-data.csv')
df_population2001 = df_population2001.drop(0)
df_population2001 = df_population2001.set_index('State Code')
df = df_political2001.join(df_population2001,how = 'left', lsuffix = 'pop')
df_2001 = df.drop(columns = [ '2008 Gov', '2008 Legis', '2008 Fiscal', '2020 Gov', '2020 Legis', '2020 Fiscal', '2008', '2019'], axis =1)
df_2001 = df_2001.rename(columns = {'2001 Fiscal': 'fiscal','2001 Gov':'gov_party', '2001 Legis': 'legis_party', '2001':'population', 'Code':'area_fips'})
df_2001 = df_2001.set_index('area_fips')
df_2001 = pd.get_dummies(df_2001, columns = ['Region', 'gov_party', 'legis_party'])
df_2001 = df_2001.drop(columns = ['Region_Offshore', 'gov_party_I', 'legis_party_N'], axis =1)
df_industry2001 = pd.read_csv('data/2001emppcg.csv', low_memory = False)
df_industry2001 = df_industry2001.set_index('area_fips')
df_2001 = df_2001.join(df_industry2001, how = 'inner', rsuffix = 'indus' )
df_target2001 = pd.read_csv('data/Recession1_timeline.csv')
df_target2001 = df_target2001.set_index('area_fips')
df_target2001 = df_target2001.drop(columns=['Unnamed: 0','area_title', '2000.25', '2000.5', '2000.75',
       '2001.0', '2001.25', '2001.5', '2001.75', '2002.0', '2002.25', '2002.5',
       '2002.75', '2003.0', '2003.25', '2003.5', '2003.75', '2004.0',
       '2004.25', '2004.5', '2004.75', '2005.0', '2005.25', '2005.5',
       '2005.75', '2006.0', '2006.25', '2006.5', '2006.75', '2007.0',
       '2007.25', '2007.5', '2007.75', '2008.0', 'nadir', 'nadir_qtr',
       'nadir_qtr_ct', 'pre-peak', 'post-peak'])
df_2001 = df_2001.join(df_target2001,how='inner', rsuffix = '_target')
df_2001['year'] = '2001'
df_2001 = df_2001.reset_index()

df_political2008 = pd.read_csv('data/state-political-data.csv')
df_political2008 = df_political2008.drop(0)
df_political2008 = df_political2008.set_index('State Code')
df_population2008 = pd.read_csv('data/county-population-data.csv')
df_population2008 = df_population2008.drop(0)
df_population2008 = df_population2008.set_index('State Code')
df = df_political2008.join(df_population2008,how = 'right', lsuffix = 'pop')
df_2008 = df.drop(columns = ['2001 Gov', '2001 Legis', '2001 Fiscal', '2020 Gov', '2020 Legis', '2020 Fiscal', '2001', '2019'], axis =1)
df_2008 = df_2008.rename(columns = {'2008 Fiscal': 'fiscal','2008 Gov':'gov_party', '2008 Legis': 'legis_party', '2008':'population', 'Code':'area_fips'})
df_2008 = df_2008.set_index('area_fips')
df_2008 = pd.get_dummies(df_2008, columns = ['Region', 'gov_party', 'legis_party'])
df_2008 = df_2008.drop(columns = ['Region_Offshore', 'legis_party_N'], axis =1)
df_industry2008 = pd.read_csv('data/2008emppcg.csv', low_memory = False)
df_industry2008 = df_industry2008.set_index('area_fips')
df_2008 = df_2008.join(df_industry2008, how = 'inner', rsuffix = 'indus' )
df_target2008 = pd.read_csv('data/Recession2_timeline.csv')
df_target2008 = df_target2008.set_index('area_fips')
df_target2008 = df_target2008.drop(columns=['Unnamed: 0', 'area_title', '2007.25', '2007.5', '2007.75', '2008.0',
       '2008.25', '2008.5', '2008.75', '2009.0', '2009.25', '2009.5',
       '2009.75', '2010.0', '2010.25', '2010.5', '2010.75', '2011.0',
       '2011.25', '2011.5', '2011.75', '2012.0', '2012.25', '2012.5',
       '2012.75', '2013.0', '2013.25', '2013.5', '2013.75', '2014.0',
       '2014.25', '2014.5', '2014.75', '2015.0', '2015.25', '2015.5',
       '2015.75', '2016.0', '2016.25', '2016.5', '2016.75', '2017.0',
       '2017.25', '2017.5', '2017.75', '2018.0', '2018.25', '2018.5',
       '2018.75', '2019.0', 'nadir', 'nadir_qtr', 'nadir_qtr_ct', 'pre-peak',
       'post-peak'])
df_2008 = df_2008.join(df_target2008,how='inner', rsuffix = '_target')
df_2008['year'] = '2008'
df_2008 = df_2008.drop(columns = ['fiscal', 'State'])
df_2008 = df_2008.reset_index()

df_merge = df_2001.append(df_2008)
df_merge.shape
df_merge.columns[df_merge.isna().any()]
df_merge = df_merge.fillna(0)
df_merge['delta_percap'] = df_merge['delta'] / df_merge['population']


df_merge.to_csv('data/full_dataset.csv')

df_political2020 = pd.read_csv('data/state-political-data.csv')
df_political2020 = df_political2020.drop(0)
df_political2020.set_index('State Code')
df_population2020 = pd.read_csv('data/county-population-data.csv')
df_population2020 = df_population2020.drop(0)
df_population2020.set_index('State Code')
df = df_political2020.join(df_population2020,how = 'right', lsuffix = 'pop')
df_2020 = df.drop(columns = ['State Codepop', '2001 Gov', '2001 Legis', '2001 Fiscal', '2008 Gov', '2008 Legis', '2008 Fiscal', '2001', '2008'], axis =1)
df_2020 = df_2020.rename(columns = {'2020 Fiscal': 'fiscal','2020 Gov':'gov_party', '2020 Legis': 'legis_party', '2019':'population', 'Code':'area_fips'})
# df_2020.columns
df_2020 = df_2020.set_index('area_fips')
df_2020 = pd.get_dummies(df_2020, columns = ['Region', 'gov_party', 'legis_party'])
df_2008 = df_2020.drop(columns = ['Region_Offshore', 'legis_party_N'], axis =1)
df_industry2020 = pd.read_csv('data/2019emppcg.csv', low_memory = False)
df_industry2020 = df_industry2020.set_index('area_fips')
df_2020 = df_2020.join(df_industry2008, how = 'inner', rsuffix = 'indus' )
df_2020['year'] = '2008'
df_2020 = df_2020.drop(columns = ['fiscal', 'State'])
df_2020 = df_2020.reset_index()

df_2020.to_csv('data/2020_predict.csv')