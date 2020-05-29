from typing import List, Tuple

import numpy as np

from layer import Layer


class NeuralNetwork:
    def __init__(self, eta: float, *layers: Layer) -> None:
        self._eta: float = eta
        self._layers: Tuple[Layer] = layers

    @classmethod
    def init_from_scratch(cls, eta: float, sizes: List[int], activations: List[str]):
        layers = []
        for i, (size, activation) in enumerate(zip(sizes[1:], activations)):
            layers.append(Layer(size, sizes[i], activation))
        return cls(eta, *layers)

    def train(self, train_data: np.ndarray, train_labels: np.ndarray, iterations: int):
        evaluations = []
        for i in range(iterations):
            neurons_activation = self._feed_forward(train_data)
            self._backward_propagation(train_data, train_labels, neurons_activation)
            evaluations.append(np.sum(np.power(neurons_activation[-1] - train_labels, 2))
                               / neurons_activation[-1].size)
        return evaluations

    def predict(self, data: np.ndarray):
        return self._feed_forward(data)[-1]

    def _feed_forward(self, x) -> List[np.ndarray]:
        neurons_activation = [self._layers[0].function(np.dot(x, self._layers[0].weights.T))]
        for i, layer in enumerate(self._layers[1:]):
            neurons_activation.append(layer.function(np.dot(neurons_activation[i], layer.weights.T)))
        return neurons_activation

    def _backward_propagation(self, x, y, neurons_activation) -> None:
        delta_weights = []

        delta = self._layers[-1].derivative(neurons_activation[-1]) * (y - neurons_activation[-1])
        for i in range(len(self._layers) - 2, -1, -1):
            delta_weights.append(self._eta * np.dot(delta.T, neurons_activation[i]))
            delta = self._layers[i].derivative(neurons_activation[i]) * np.dot(delta, self._layers[i + 1].weights)
        delta_weights.append(self._eta * np.dot(delta.T, x))
        delta_weights.reverse()

        for layer, delta_weight in zip(self._layers, delta_weights):
            layer.weights += delta_weight
