import numpy as np

from neural_network import NeuralNetwork
from train import prepare_train_and_show

if __name__ == "__main__":
    train_data = np.array([[i] for i in np.linspace(0, 2, 21)])
    train_labels = np.array(np.sin(train_data * 3 * np.pi / 2))
    test_data = np.array([[i] for i in np.linspace(0, 2, 161)])
    test_labels = np.array(np.sin(test_data * 3 * np.pi / 2))
    neural_network = NeuralNetwork.init_from_scratch(
        0.20, [1, 10, 15, 20, 1], ['tanh', 'tanh', 'sigmoid', 'sigmoid'])
    prepare_train_and_show(neural_network, train_data, train_labels, test_data, test_labels)
