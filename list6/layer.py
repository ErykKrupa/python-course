from typing import Callable

import numpy as np


class Layer:
    functions = {
        'sigmoid': (
            lambda x: 1.0 / (1.0 + np.exp(np.negative(x))),
            lambda x: x * (1.0 - x)
        ),

        'relu': (
            lambda x: np.maximum(x, 0),
            lambda x: np.where(x > 0.0, 1.0, 0.0)
        ),

        'tanh': (
            lambda x: np.tanh(x),
            lambda x: 1 - np.square(x)
        )
    }

    def __init__(self, size: int, previous_layer_size: int, activation: str):
        activation = Layer.functions[activation]
        self.function: Callable = activation[0]
        self.derivative: Callable = activation[1]
        self.size = size
        self.previous_layer_size = previous_layer_size
        self.weights: np.ndarray = np.array(
            np.random.rand(size, previous_layer_size), np.float64)
