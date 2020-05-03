import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

m1 = [10, 100, 1000, 10_000]
m2 = [10, 100, 200, 500, 1000, 10_000]
main_movie_id = 1


def _prepare_data(data: pd.DataFrame, max_movie_id: int, movie_id: int) -> (pd.DataFrame, np.array):
    users_id = data[data.movieId == movie_id]['userId'].to_numpy()
    ratings = data[data.userId.isin(users_id)][data.movieId <= max_movie_id]
    movies_id = np.unique(ratings.movieId.to_numpy())
    matrix = pd.DataFrame(0.0, index=[user_id for user_id in range(users_id.size)], columns=movies_id)

    for i, user in enumerate(users_id):
        ratings_for_user = ratings[ratings.userId == user]
        for _, row in ratings_for_user.iterrows():
            matrix.at[i, row.movieId] = row.rating

    vector = matrix[movie_id].to_numpy()
    matrix = matrix.drop(columns=[movie_id])
    return matrix, vector


def _prepare_plot_with_error(matrix: pd.DataFrame, vector: np.array, result: np.array,
                             position: tuple, max_movie_id: int) -> None:
    plt.subplot(position[0], position[1], position[2])
    plt.plot(np.linspace(1, vector.size, vector.size),
             np.abs(matrix.to_numpy().dot(result) - vector),
             label='Absolute error')
    plt.title(f"Max movie id: {max_movie_id}")
    plt.xlabel("users")
    plt.ylabel("ratings")
    plt.legend()


def _prepare_plot(matrix: pd.DataFrame, vector: np.array, result: np.array,
                  position: tuple, max_movie_id: int) -> None:
    linear_space = np.linspace(1, vector.size, vector.size)
    plt.subplot(position[0], position[1], position[2])
    plt.plot(linear_space, matrix.to_numpy().dot(result), label='regression')
    plt.plot(linear_space, vector, label='real')
    plt.title(f"Max movie id: {max_movie_id}")
    plt.xlabel("users")
    plt.ylabel("ratings")
    plt.legend()


if __name__ == '__main__':
    raw_data = pd.read_csv("data\\ratings.csv")[['userId', 'movieId', 'rating']]
    for i, movie_amount in enumerate(m1, 1):
        X, y = _prepare_data(raw_data, movie_amount, main_movie_id)
        regression = np.linalg.lstsq(X, y)[0]
        print(regression.score())
        _prepare_plot_with_error(X, y, regression, (2, 2, i), movie_amount)
    plt.gcf().set_size_inches([10, 8])
    plt.show()

    for i, movie_amount in enumerate(m2, 1):
        X, y = _prepare_data(raw_data, movie_amount, main_movie_id)
        regression = np.linalg.lstsq(X[:201], y[:201])[0]
        _prepare_plot(X[201:], y[201:], regression, (3, 2, i), movie_amount)
    plt.gcf().set_size_inches([10, 12])
    plt.show()
