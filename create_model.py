from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization,\
Flatten, LSTM
import config

class CreateModel():

    def __init__(self) -> None:
        pass
    
    @staticmethod
    def create_model(num_classes):
        # define model
        model = Sequential()
        model.add(LSTM(units=128, return_sequences=True, 
                    input_shape=(config.TIMESTEPS, config.NUM_FEATURES)))
        model.add(Dropout(0.2))
        model.add(BatchNormalization())
        model.add(LSTM(units=128, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(BatchNormalization())
        model.add(LSTM(units=64, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(BatchNormalization())
        # Softmax for multi-class classification
        model.add(Flatten())
        model.add(Dense(num_classes, activation='softmax'))

        model.compile(loss='categorical_crossentropy', optimizer='adam',
                    metrics=['accuracy'])
        return model






