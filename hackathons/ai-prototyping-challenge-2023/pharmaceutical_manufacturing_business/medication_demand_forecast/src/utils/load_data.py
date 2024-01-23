# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

# pylint: disable=C0415,E0401,R0914

"""
Code to load and prepare data for training.

Adopted from https://www.kaggle.com/code/dimitreoliveira/deep-learning-for-time-series-forecasting/notebook
"""
from typing import Union

import numpy as np
import pandas as pd


def read_data(fname: str) -> pd.DataFrame:
    """read in the data frame and create relevant columns

    Args:
        fname (str): path to data file
    Returns:
        pd.DataFrame: data file as dataframe
    """
    data = pd.read_csv(fname, parse_dates=['date'])
    data = data.sort_values('date').groupby(
        ['item', 'store', 'date'], as_index=False)
    data = data.agg({'sales': ['mean']})
    data.columns = ['item', 'store', 'date', 'sales']
    return data


def series_to_supervised(
    data: pd.DataFrame,
    window: int = 1,
    lag: int = 1,
    dropnan: bool = True
) -> Union[pd.DataFrame, pd.DataFrame]:
    """creates a dataframe with lags

    Args:
        data (pd.DataFrame): dataframe
        window (int, optional): window size to lookback. Defaults to 1.
        lag (int, optional): target timestep. Defaults to 1.
        dropnan (bool, optional): whether to drop nans. Defaults to True.

    Returns:
        Union[pd.DataFrame, pd.DataFrame]: dataframe with lagged values and
        dataframe labels
    """
    cols, names = [], []
    dates = data['date']
    data = data.drop('date', axis=1)
    # Input sequence (t-n, ... t-1)
    for i in range(window, 0, -1):
        cols.append(data.shift(i))
        names += [(f'{col}(t-{i})') for col in data.columns]
    # Current timestep (t=0)
    cols.append(data)
    names += [(f'{col}(t)') for col in data.columns]
    # Target timestep (t=lag)
    cols.append(data.shift(-lag))
    names += [(f'{col}(t+{lag})') for col in data.columns]
    # Put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    agg['date'] = dates
    # Drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)

    columns_to_drop = [(f'{col}(t+{lag})') for col in ['item', 'store']]
    for i in range(window, 0, -1):
        columns_to_drop += [(f'{col}(t-{i})') for col in ['item', 'store']]
    agg['item'] = agg['item(t)']
    agg['store'] = agg['store(t)']
    agg.drop(columns_to_drop, axis=1, inplace=True)
    agg.drop(['item(t)', 'store(t)'], axis=1, inplace=True)

    labels_col = f'sales(t+{lag})'
    labels = agg[labels_col]
    agg = agg.drop(labels_col, axis=1)
    return agg, labels


def prepare_data(
        data: pd.DataFrame,
        labels: pd.Series,
        sub_size: int = 1
) -> Union[np.ndarray, np.ndarray]:
    """Reshape the data to fit the CNN-LSTM model

    Args:
        data (pd.DataFrame): time series features
        labels (pd.Series): forecasting labels
        sub_size (int, optional): number of subsequences to make. Defaults to 1.

    Returns:
        Union[np.ndarray, np.ndarray]: prepared data for CNN-LSTM.
    """
    series = data.values.reshape((data.shape[0], data.shape[1], 1))
    if sub_size > 1:
        timesteps = data.shape[1]//sub_size
        series_sub = series.reshape(
            (series.shape[0], sub_size, timesteps, 1)
        )
        return series_sub, labels
    return series, labels
