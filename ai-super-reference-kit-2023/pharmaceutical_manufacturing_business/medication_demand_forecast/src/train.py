# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

# pylint: disable=C0415,E0401,R0914,E0611

"""
Run training with benchmarks.

Code adopted from
https://www.kaggle.com/code/dimitreoliveira/deep-learning-for-time-series-forecasting/notebook
"""
import argparse
import logging
import os
import pathlib
import time
import warnings

import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import tensorflow as tf
print("TensorFlow Version:", tf.__version__)
from utils.load_data import read_data, series_to_supervised, prepare_data
from utils.model import get_cnn_lstm

warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#TODO: MAY NEED TO REMOVE/MODIFY
tf.keras.utils.set_random_seed(5) 


class train_model():
    def __init__(self, filepath: str, window = 129, lag_size = 1, test_size = 0.3, epochs = 10, batch_size = 512):
        self.filepath = filepath
        self.window = window
        self.lag_size = lag_size
        self.test_size = test_size
        self.epochs = epochs
        self.batch_size = batch_size

    def process_data(self):
        # create training and validation datasets
        if not os.path.exists(self.filepath):
            print("Data file ", self.filepath , " not found")
            return

        train = read_data(self.filepath)
        series, labels = series_to_supervised(
            train,
            window=self.window,
            lag=self.lag_size
        )

        self.x_train, self.x_valid, self.y_train, self.y_valid = train_test_split(
            series,
            labels.values,
            test_size=self.test_size,
        )

        self.x_train_sub, self.y_train_sub = prepare_data(
            self.x_train.drop(['date', 'item', 'store'], axis=1), self.y_train, 2
        )
        self.x_valid_sub, self.y_valid_sub = prepare_data(
            self.x_valid.drop(['date', 'item', 'store'], axis=1), self.y_valid, 2
        )


        return self.x_train_sub, self.x_valid_sub, self.y_train_sub, self.y_valid_sub

    def fit_lstm_model(self,
                        save_model_dir: str = None):

        

        # compile the model
        self.model = get_cnn_lstm(self.x_train_sub)
        optimizer = tf.keras.optimizers.Adam(lr=1e-4)
        self.model.compile(loss='mse', optimizer=optimizer)
        self.model.summary()
        logger.info(
            'Starting training on %d samples with batch size %d...',
            self.x_train_sub.shape[0]
        )

        # train the model using keras
        start = time.time()
        _ = self.model.fit(
            x=self.x_train_sub,
            y=self.y_train_sub,
            batch_size= self.batch_size,
            validation_data=(self.x_valid_sub, self.y_valid_sub),
            epochs=self.epochs,
            verbose=2
        )
        end = time.time()

        train_pred = self.model.predict(self.x_train_sub, self.batch_size)
        
        logger.info(
            '======> Train RMSE: %.4f',
            np.sqrt(mean_squared_error(self.y_train_sub, train_pred))
        )

        logger.info(
            '=======> Train time : %d seconds',
            end - start
        )

        if save_model_dir is not None:
            if isinstance(save_model_dir, str) == True:
                path = pathlib.Path(save_model_dir)
                path.mkdir(parents=True, exist_ok=True)
                logger.info("Saving model...")
                self.model.save(save_model_dir)


        return self.model

        

    def validate (self):

        valid_pred = self.model.predict(self.x_valid_sub, self.batch_size)
        
        validation_rmse = np.sqrt(mean_squared_error(self.y_valid_sub, valid_pred))

        logger.info(
            '======> Validation RMSE: %.4f',
            validation_rmse
        )
        
        return validation_rmse