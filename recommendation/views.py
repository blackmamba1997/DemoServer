from django.shortcuts import render
from django.http import JsonResponse as res
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

# Create your views here.
def home(request,text):

    df = pd.read_csv("./dataset/movie_dataset.csv")

    def combine_features(row):
        return row['keywords'] + " " + row['genres']

    features = ['keywords', 'genres']

    for feature in features:
        df[feature] = df[feature].fillna('')  # filling all NaNs with blank string

    df['combined_features'] = df.apply(combine_features, axis=1)

    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df['combined_features'])
    cosine_sim = cosine_similarity(count_matrix)

    def get_id_from_index(index):
        return df[df.index == index]['id'].values[0]

    def get_index_from_id(id):
        return df[df.id == id]['index'].values[0]

    movie_user_likes = text
    movie_index = get_index_from_id(movie_user_likes)
    similar_movies = list(enumerate(cosine_sim[movie_index]))
    # accessing the row corresponding to given movie to find all the similarity scores for that movie and then enumerating over it

    similar_sorted = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:]
    similar_movies = similar_sorted[0:10]

    list_names = []
    for names in similar_movies:
        #list_names.append(df[df.id==get_id_from_index(names[0])]['title'].values[0])
        temp={}
        temp['id']=str(get_id_from_index(names[0]))
        temp['movie']=df[df.id==get_id_from_index(names[0])]['title'].values[0]
        list_names.append(temp)

    result = {'result': list_names}

    #list.append(text)
    #print(list)
    return res(result)

def about(request):

    return res("<h2>About</h2")
