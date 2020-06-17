from keras import models, layers, optimizers
import numpy as np
from train import prepare_train_and_show


if __name__ == "__main__":
    train_data = np.array([[i] for i in np.linspace(0, 6, 61)])
    train_labels = np.array(np.sin(train_data * 3 * np.pi / 2))
    test_data = np.array([[i] for i in np.linspace(0, 6, 481)])
    test_labels = np.array(np.sin(test_data * 3 * np.pi / 2))

    model = models.Sequential()
    model.add(layers.Dense(50, activation='tanh', input_shape=(1, )))
    model.add(layers.Dense(75, activation='sigmoid'))
    model.add(layers.Dense(1, activation='sigmoid'))
    model.compile(optimizer=optimizers.RMSprop(lr=0.005),
                  loss="mse",
                  metrics=['accuracy'])
    prepare_train_and_show(model, train_data, train_labels, test_data, test_labels)
