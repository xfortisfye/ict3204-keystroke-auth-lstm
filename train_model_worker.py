from PyQt5 import QtCore

import config
from create_model import CreateModel

from os import stat
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from keras.utils.np_utils import to_categorical 
from tensorflow.keras.callbacks import EarlyStopping

# from scikeras.wrappers import KerasClassifier
from keras.wrappers.scikit_learn import KerasClassifier
from keras.models import load_model

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
# from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import OneHotEncoder


class WorkerSignals(QtCore.QObject):
    data = QtCore.pyqtSignal(str)
    acc = QtCore.pyqtSignal(str)

class TrainModelWorker(QtCore.QThread):
    def __init__(self, url, epoch, batch, folds):
        super(TrainModelWorker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.url = url
        self.epoch = epoch
        self.batch = batch
        self.folds = folds
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        # self.kwargs['progress_callback'] = self.signals.progress

    @QtCore.pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        # random seed for reproducibility
        seed = 10
        np.random.seed(seed)

        # loading of dataset
        df = pd.read_csv(self.url)
        
        # # Remove missing values IF AVAILABLE and print head
        df = df.dropna()
        # df.head()
        
        dataset = df.values

        # divide data into features X and target (Classes) Y
        X = dataset[:,3:].astype(float)
        Y = dataset[:,0]

        # # check for class imbalance
        print(df.groupby(Y).size())

        # convert target Y to one hot encoded Y for model
        Y = Y.reshape(-1, 1)
        encoder = OneHotEncoder().fit(Y)

        # get all the encoded class
        self.signals.data.emit("Checking for class imbalance...")
        self.signals.data.emit(str(encoder.get_feature_names_out() + "\n"))

        # print X and Y shape
        self.signals.data.emit("X dataset shape: " + str(X.shape))
        self.signals.data.emit("Y dataset shape: " + str(Y.shape) + "\n")

        # split dataset into train and test of 0.8/0.2 ratio
        X_train, X_test, y_train, y_test = train_test_split(
            X, Y, test_size=0.2, random_state=seed)

        # normalisation to 0 to 1
        scaler = MinMaxScaler(feature_range=(0, 1))
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        # reshaping the dataset to include LSTM
        X_train = np.asarray(X_train, dtype=np.float32)
        X_train = np.reshape(X_train, (X_train.shape[0], config.TIMESTEPS, X_train.shape[1]))
        X_test = np.asarray(X_test, dtype=np.float32)
        X_test = np.reshape(X_test, (X_test.shape[0], config.TIMESTEPS, X_test.shape[1]))

        # converting y data to encoding
        y_train = encoder.transform(y_train).toarray()
        y_test = encoder.transform(y_test).toarray()

        num_classes = y_train.shape[1]

        self.signals.data.emit("X train shape: " + str(X_train.shape))
        self.signals.data.emit("Y train shape: " + str(y_train.shape))
        self.signals.data.emit("X test shape: " + str(X_test.shape))
        self.signals.data.emit("Y test shape: " + str(y_test.shape) + "\n")

        model = KerasClassifier(build_fn=lambda num_classes=num_classes: CreateModel.create_model(num_classes)
        , epochs=self.epoch, batch_size=self.batch)

        kfold = KFold(n_splits=self.folds, shuffle=True, random_state=seed)

        results = cross_val_score(model, X_train, y_train, 
            cv=kfold, error_score="raise", verbose=1)

        self.signals.acc.emit("Validation accuracy of %.2f%% (with standard deviation of %.2f%%)" % 
            (results.mean()*100, results.std()*100))

        # fit the model
        es = EarlyStopping(monitor='loss', mode='min', min_delta=0.001, patience=50,
                        verbose=0)
        history = model.fit(X_train, y_train, callbacks=es)

        print(type(history))
        # view model summary
        model.model.summary()
        
        y_pred = model.predict(X_test)
        y_pred = to_categorical(y_pred)

        # evaluate predictions
        acc = accuracy_score(y_test, y_pred)
        print("Testing accuracy: %.3f%%" % (acc*100))

        # save model
        model.model.save("keys_classifier.h5")

