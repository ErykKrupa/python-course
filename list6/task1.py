from collections import namedtuple

import matplotlib.pyplot as plt
import numpy as np

from neural_network import NeuralNetwork

ITERATIONS = 3000
x_axis = [i for i in range(10, ITERATIONS)]

np.random.seed(17)

if __name__ == "__main__":
    eta = 0.01
    neural_networks_names = [[(NeuralNetwork.init_from_scratch(eta, [3, 4, 1], ['sigmoid'] * 2), "sigmoid"),
                              (NeuralNetwork.init_from_scratch(eta, [3, 4, 1], ['relu'] * 2), "relu"),
                              (NeuralNetwork.init_from_scratch(eta, [3, 4, 1], ['sigmoid', 'relu']), "sigmoid-relu"),
                              (NeuralNetwork.init_from_scratch(eta, [3, 4, 1], ['relu', 'sigmoid']), "relu-sigmoid")]
                             for i in range(3)]
    train_data = np.array([[0, 0, 0],
                           [0, 0, 1],
                           [0, 1, 0],
                           [0, 1, 1],
                           [1, 0, 0],
                           [1, 0, 1],
                           [1, 1, 0],
                           [1, 1, 1]])
    TrainLabel_Name = namedtuple('TrainLabel_Name', ['train_label', 'name'])
    train_labels_names = [TrainLabel_Name(train_label=np.array([[0], [1], [1], [1], [1], [1], [1], [0]]), name="xor"),
                          TrainLabel_Name(train_label=np.array([[0], [0], [0], [0], [0], [0], [0], [1]]), name="and"),
                          TrainLabel_Name(train_label=np.array([[0], [1], [1], [1], [1], [1], [1], [1]]), name="or")]
    plt.figure(figsize=(5, 9))
    for i, (neural_network_name, train_label_name) in enumerate(zip(neural_networks_names, train_labels_names), 1):
        plt.subplot(3, 1, i)
        plt.xlabel("iterations")
        plt.ylabel("error")
        plt.title(train_label_name.name)
        for neural_network, name in neural_network_name:
            plt.plot(x_axis, neural_network.train(train_data, train_label_name.train_label, ITERATIONS)[10:ITERATIONS],
                     label=name)
        plt.legend()
    plt.show()
