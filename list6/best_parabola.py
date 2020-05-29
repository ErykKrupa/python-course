import numpy as np

from neural_network import NeuralNetwork
from train import prepare_train_and_show

if __name__ == "__main__":
    train_data = np.array([[i] for i in np.linspace(-50, 50, 26)])
    train_labels = np.array(np.square(train_data))
    test_data = np.array([[i] for i in np.linspace(-50, 50, 101)])
    test_labels = np.array(np.square(test_data))
    neural_network = NeuralNetwork.init_from_scratch(
        0.25, [1, 10, 15, 15, 15, 1], ['tanh', 'sigmoid', 'sigmoid', 'sigmoid', 'sigmoid'])
    print("Better approximation in longer period of time")
    prepare_train_and_show(neural_network, train_data, train_labels, test_data, test_labels)
