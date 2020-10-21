
import matplotlib.pyplot as plt
import keras
import pandas as pd


def flatten_shape(shape):
    s = 1
    for v in shape[1:]:
        s *= v
    return (shape[0], s)


def flatten(X):
    shape = X.shape
    s = 1
    for v in shape[1:]:
        s *= v
    Xt = X.copy()
    Xt.resize(shape[0], s)
    return Xt


class NeuralNet(object):

    def create(self, shape, layers=[10, 10], out=1, activation='relu'):
        if len(shape) > 2 : shape = flatten_shape(shape)
        model = keras.Sequential()
        for i, l in enumerate(layers):
            if i==0:
                model.add(keras.layers.Dense(l, activation=activation, input_shape=(shape[1:])))
            else:
                model.add(keras.layers.Dense(l, activation=activation))
        model.add(keras.layers.Dense(out))
        model.compile(optimizer='rmsprop', loss='mse')
        self.model = model

    def train(self, X, y, epochs=50, batch_size=256, verbose=0):
        if len(X.shape) > 2 : X = flatten(X)
        self.history = self.model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=verbose)

    def predict(self, X):
        if len(X.shape) > 2 : X = flatten(X)
        return self.model.predict([X])[:,0]

    def review_history(self):
        history_dict = self.history.history
        print(history_dict.keys())
        train_loss_values = history_dict['loss']
        test_loss_values = history_dict['val_loss']
        epochs = range(1, len(train_loss_values) + 1)
        plt.plot(epochs, train_loss_values, 'bo', label='Training loss')
        plt.plot(epochs, test_loss_values, 'b', label='Test loss')
        plt.title('Training and test loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()

    def review_prediction(model, X_train, y_train, X_test, y_test):
        predictions = model.predict(X_test)
        df = pd.DataFrame({'x':predictions[:,0], 'y':y_test})
        df.plot.scatter(x=0, y=1)
        print(df.corr())
        return df