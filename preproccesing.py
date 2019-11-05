import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import warnings

#ignore warnings
warnings.filterwarnings("ignore")

#load data
df = pd.read_csv("raw_data.csv", low_memory=False)

#drop unwanted columns
df = df.drop(columns = ['belongs_to_collection', 'homepage', 'imdb_id', 'overview', 'poster_path', 'spoken_languages', 'tagline', 'title', 'video', 'production_companies', 'id', 'original_title'])
print(df.columns)

#set dtype to numeric
df.budget = pd.to_numeric(df.budget, errors='coerce')
df.popularity = pd.to_numeric(df.popularity, errors='coerce')
df.revenue = pd.to_numeric(df.revenue, errors='coerce')
df.runtime = pd.to_numeric(df.runtime, errors='coerce')
df.vote_average = pd.to_numeric(df.vote_average, errors='coerce')
df.vote_count = pd.to_numeric(df.vote_count, errors='coerce')

#replace single quotes to double quotes to make a valid json
df.production_countries = df.production_countries.str.replace('\'', '\"')

##convert production_countries json entries to dict
for i in range(0, len(df)):
    try:
        df.production_countries[i] = json.loads(df.production_countries[i])
        df.production_countries[i] = df.production_countries[i][0]['iso_3166_1']
    except Exception as e:
        df.production_countries[i] = np.NaN

# Set string columns as dummies variables
original_languages_dummies = pd.get_dummies(data=df['original_language'], prefix='lan', drop_first=True)
original_languages_dummies = original_languages_dummies.drop(columns = ['lan_68.0', 'lan_82.0'])
df = df.drop(columns = 'original_language')
df = pd.concat([df, original_languages_dummies], axis = 1)

status_dummies = pd.get_dummies(data=df['status'], drop_first=True)
df = df.drop(columns = 'status')
df = pd.concat([df, status_dummies], axis = 1)

production_countries_dummies = pd.get_dummies(data=df['production_countries'], prefix='prod_coun', drop_first=True)
df = df.drop(columns = 'production_countries')
df = pd.concat([df, production_countries_dummies], axis = 1)

# save proccesed data to csv
df.to_csv('preprocessed_data.csv')


