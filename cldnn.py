from network import Network
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras import Sequential
from keras.layers import LSTM, Dense, Conv2D, MaxPooling2D
import numpy as np


class CLDNN(Network):
    def train_model(self):
        es = EarlyStopping(patience=4)
        lr_reduce = ReduceLROnPlateau(factor=0.2, verbose=1)

        self.x_train = np.expand_dims(self.x_train, 3)
        self.x_val = np.expand_dims(self.x_val, 3)
        self.x_test = np.expand_dims(self.x_test, 3)

        model = Sequential()
        # conv, conv, dense, lstm, lstm, dnn, dnn, out
        model.add(Conv2D(256, kernel_size=(9, 9), strides=(1, 1),
                         activation='relu',
                         input_shape=(self.x_val.shape[1:])))

        model.add(Conv2D(256, kernel_size=(4, 3), strides=(1, 1), activation='relu'))

        model.add(MaxPooling2D())

        model.add(Dense(256))

        model.add(LSTM(512))
        model.add(LSTM(512))

        model.add(Dense(1024))
        model.add(Dense(1024))
        model.add(Dense(self.y_train.shape[1], activation='softmax'))

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        history_callback = model.fit(self.x_train, self.y_train,
                                     validation_data=(self.x_val, self.y_val),
                                     epochs=self.epochs,
                                     batch_size=2048, callbacks=[es, lr_reduce])
        self.train_loss_history = history_callback.history["loss"]
        self.train_acc_history = history_callback.history["acc"]
        return model