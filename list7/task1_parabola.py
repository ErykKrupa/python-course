from keras import models, layers, optimizers
import numpy as np
from train import prepare_train_and_show


if __name__ == "__main__":
    train_data = np.array([[i] for i in np.linspace(-50, 50, 26)])
    train_labels = np.array(np.square(train_data))
    test_data = np.array([[i] for i in np.linspace(-50, 50, 101)])
    test_labels = np.array(np.square(test_data))

    model = models.Sequential()
    model.add(layers.Dense(10, activation='tanh', input_shape=(1, )))
    model.add(layers.Dense(15, activation='sigmoid'))
    model.add(layers.Dense(1, activation='sigmoid'))
    model.compile(optimizer=optimizers.RMSprop(lr=0.01),
                  loss="mse",
                  metrics=['accuracy'])
    prepare_train_and_show(model, train_data, train_labels, test_data, test_labels)
