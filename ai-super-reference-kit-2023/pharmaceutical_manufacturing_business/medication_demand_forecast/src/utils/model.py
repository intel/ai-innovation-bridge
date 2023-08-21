# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

# pylint: disable=C0415,E0401,R0914,E0611

"""
Tensorflow models and utilities.

Model adopted from https://www.kaggle.com/code/dimitreoliveira/deep-learning-for-time-series-forecasting/notebook
"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D
from tensorflow.keras.layers import Dense, LSTM, TimeDistributed, Flatten


def get_cnn_lstm(X, n_hidden: int = 150) -> Sequential:
    """Get a CNN-LSTM Model

    Args:
        n_cells (int, optional): dim of hidden state in LSTM . Defaults to 100.

    Returns:
        Sequential: untrained and uncompiled CNN-LSTM model
    """
    model_cnn_lstm = Sequential()
    model_cnn_lstm.add(
        TimeDistributed(
            Conv1D(filters=128, kernel_size=3, activation='relu',
                   input_shape=(X.shape[2], X.shape[3])),
            input_shape=(X.shape[1], X.shape[2], X.shape[3])
        )
    )
    model_cnn_lstm.add(TimeDistributed(MaxPooling1D(pool_size=2)))
    model_cnn_lstm.add(
        TimeDistributed(
            Conv1D(filters=64, kernel_size=3, strides=2, activation='relu')
        )
    )
    model_cnn_lstm.add(TimeDistributed(MaxPooling1D(pool_size=2)))
    model_cnn_lstm.add(
        TimeDistributed(
            Conv1D(filters=32, kernel_size=3, strides=2, activation='relu')
        )
    )
    model_cnn_lstm.add(TimeDistributed(MaxPooling1D(pool_size=2)))
    model_cnn_lstm.add(TimeDistributed(Flatten()))
    model_cnn_lstm.add(LSTM(n_hidden, activation='relu'))
    model_cnn_lstm.add(Dense(1))
    return model_cnn_lstm
