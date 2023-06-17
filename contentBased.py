import numpy as np
import pandas as pd
import re

def content_recommend():
    try:
        df_content = pd.read_csv('./output_AFMT_ID.csv')
        df_content = df_content.drop('no_of_reviews', axis=1)
        df_copy_content = df_content.copy()

        for index, row in df_copy_content.iterrows():
            cat = row['category']
            df_content.at[index, cat] = 1

        df_copy_content = df_content.fillna(0)

        userInput = [
            {'name': 'M.N. VIideo Game Parlour', 'rating': 5.0},
            {'name': 'Wonde Narayan Temple', 'rating': 4.0},
            {'name': 'Gaming Zone', 'rating': 5.0},
            {'name': "Shree Narayan Temple", 'rating': 4.5},
            {'name': "National Art Museum", 'rating': 4.7},
            {'name': "Suryamukhi Park", 'rating': 4.6},
        ]
        input_df = pd.DataFrame(userInput)
        # input_df['rating'] = input_df['rating'].astype(int)

        inputId = df_copy_content[df_copy_content['name'].isin(input_df['name'].tolist())]
        input_df = input_df.drop('rating', axis=1)
        input_df = pd.merge(inputId, input_df, on='name')

        user_df = df_copy_content[df_copy_content['name'].isin(input_df['name'].tolist())]
        user_df_gen = user_df.drop(['name', 'latitude', 'longitude', 'type', 'category', 'ratings', 'id', 'small_photo'], axis=1)

        userProfile = user_df_gen.transpose().dot(input_df['ratings'].values)

        
        genre_table = df_copy_content.set_index(df_copy_content['id'])
        genre_table = genre_table.drop(['ratings', 'latitude', 'longitude', 'type', 'category', 'name', 'id'], axis=1)

        recommendationTable_df = ((genre_table * userProfile).sum(axis=1)) / userProfile.sum()
        recommendationTable_df = recommendationTable_df.sort_values(ascending=False)
        top_recommend = df_copy_content.loc[df_copy_content['id'].isin(recommendationTable_df.head(5).keys())]

        # print(top_recommend)
        return top_recommend

    except Exception as e:
        print("An error occurred:", str(e))
content_recommend()
