import pandas as pd
import numpy as np
from pandas import DataFrame, Series
from typing import List

_user_id = 1


def _fetch_data() -> pd.DataFrame:
    result = pd.read_csv('data\\ratings.csv')[['userId', 'movieId', 'rating']]
    return result[result.movieId < 10_000]


def _fetch_movies() -> pd.Series:
    result_df = pd.read_csv('data\\movies.csv')[['movieId', 'title']]
    result = pd.Series(0.0, result_df.movieId)
    for _, row in result_df.iterrows():
        result[row.movieId] = row.title
    return result


def _get_movies_id_and_ratings(data: pd.DataFrame) -> (pd.Series, np.array):
    users_id: np.array = np.unique(data['userId'].to_numpy())
    movies_id_result: np.array = np.unique(data['movieId'].to_numpy())
    ratings_result: DataFrame = pd.DataFrame(0.0, [user_id for user_id in users_id], columns=movies_id_result)
    for _, row in data.iterrows():
        ratings_result.at[row.userId, row.movieId] = row.rating
    return movies_id_result, ratings_result.to_numpy()


def _get_user_ratings(data: pd.DataFrame, user_id: int) -> np.array:
    result: Series = pd.Series(0.0, np.unique(data['movieId'].to_numpy()))
    for _, row in data[data.userId == user_id].iterrows():
        result.at[row.movieId] = row.rating
    return result.to_numpy().reshape(result.size, 1)


def _normalize(matrix: np.array) -> np.array:
    return matrix / np.linalg.norm(matrix, axis=0)


def _get_sorted_user_recommendations(data: pd.DataFrame, movies: pd.Series, user_id: int) -> List[tuple]:
    user_ratings = _get_user_ratings(data, user_id)
    normalized_ratings = _normalize(ratings)
    normalized_user_ratings = _normalize(user_ratings)
    movie_profile = _normalize(np.dot(normalized_ratings, normalized_user_ratings))
    normalized_ratings = _normalize(ratings)
    normalized_movie_profile = _normalize(movie_profile)
    user_recommendations = np.dot(normalized_ratings.T, normalized_movie_profile)
    user_recommendations = pd.Series(user_recommendations.reshape(user_recommendations.size), movies_id)
    return [(index, movies.at[index], recommendation)
            for index, recommendation in user_recommendations.sort_values(ascending=False).iteritems()]


if __name__ == '__main__':
    print("May take a while...")
    raw_data = _fetch_data()
    movies_id, ratings = _get_movies_id_and_ratings(raw_data)
    sorted_user_recommendations = _get_sorted_user_recommendations(raw_data, _fetch_movies(), _user_id)
    for movie_index, movie_name, recommendation_points in sorted_user_recommendations:
        print(movie_index, movie_name, recommendation_points)

