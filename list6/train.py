import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from neural_network import NeuralNetwork

ITERATION_PER_FRAME = 100
FRAMES = 1_000_000


def prepare_train_and_show(neural_network: NeuralNetwork,
                           train_data: np.ndarray,
                           train_labels: np.ndarray,
                           test_data: np.ndarray,
                           test_labels: np.ndarray):
    data_scaler = MinMaxScaler((0, 1))
    labels_scaler = MinMaxScaler((0, 1))

    print("Press Ctrl + C to interrupt, exit button in window may not close the program")
    plt.ion()
    figure, ax = plt.subplots()
    figure.canvas.draw_idle()

    for i in range(1, FRAMES):
        neural_network.train(
            data_scaler.fit_transform(train_data),
            labels_scaler.fit_transform(train_labels),
            ITERATION_PER_FRAME)
        prediction = neural_network.predict(data_scaler.fit_transform(test_data))

        prediction = labels_scaler.inverse_transform(prediction)
        quality = np.sum(np.square(prediction - test_labels)) / test_labels.size
        plt.cla()
        ax.scatter(train_data, train_labels)
        ax.scatter(test_data, prediction)
        plt.title(f"Steps: {i * ITERATION_PER_FRAME:,}".replace(",", " ")
                  + "\n" + f"Error: {quality:.4f}")
        plt.pause(0.00001)
    plt.waitforbuttonpress()
