import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def similarity(df) :
# TF-IDF 벡터화
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['title'])

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    threshold = 0.8

    unique_indices_set = set()
    for i in range(cosine_sim.shape[0]):
        if i not in unique_indices_set:
            similar_indices = [j for j in range(cosine_sim.shape[1]) if cosine_sim[i, j] >= threshold and j != i]
            unique_indices_set.update(similar_indices)

    unique_indices = list(unique_indices_set)

    unique_df = df.drop(unique_indices).reset_index(drop=True)

    return unique_df
