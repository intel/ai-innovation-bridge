# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

# pylint: disable=C0415,E0401,R0914,W0102

"""
Generate a time series dataset with store and item level effects
"""

import pathlib
import numpy as np
import pandas as pd
import argparse

np.random.seed(0)


def simulate_seasonal_term_frequency_domain(
        period,
        num_simulations,
        harmonics_sin=[1],
        harmonics_cos=[1],
        noise_std=5,
        ar=0.8,
        ma=0.5,
        trend=0.005,
        offset=10):
    """Generate data for testing.

    Use the formulation of a seasonal time series as an ARMA(1,1)
    process with 1 fourier seasonal components.

    Args:
        period (int): period of seasonality
        num_simulations (int): number of points to simulate
        harmonics_sin (list, optional): sin coefs. Defaults to [1].
        harmonics_cos (list, optional): cos coefs. Defaults to [1].
        noise_std (int, optional): noise level. Defaults to 5.
        ar (float, optional): ar(1) coeff. Defaults to 0.8.
        ma (float, optional): ma(1) coeff. Defaults to 0.5.
        trend (float, optional): linear trend coeff. Defaults to 0.005.
        offset (int, optional): constant base offset. Defaults to 10.

    Returns:
        np.array: Array of values following above process.
    """

    innovations = np.random.normal(0, noise_std, size=num_simulations)
    series = offset + np.zeros(num_simulations)
    for t in range(1, len(series)):
        y = 0
        for k in range(1, len(harmonics_sin) + 1):
            y += harmonics_sin[k - 1] * \
                np.sin((2 * np.pi * k * t / period) + np.pi/2)
            y += harmonics_cos[k - 1] * \
                np.cos((2 * np.pi * k * t / period) + np.pi/2)
        series[t] = ar * series[t - 1] + ma * \
            innovations[t-1] + y + innovations[t]

    # yt = c + at + ARMA(1,1) + fourier
    series = offset + trend * np.arange(0, len(series)) + series
    return np.ceil(series)


def main(FLAGS):

    # Model
    # Seasonality is fixed for all items
    # Store level:
    #   Store level variance, Store level baseline sales
    # Item level:
    #   Item level base sales, trend
    store_level_variance = [np.random.normal(4, 0.5) for _ in range(10)]
    store_level_baseline_offset = [
        np.round(np.random.normal(0, 8)) for _ in range(10)]
    item_level_baseline = [np.random.poisson(30) for _ in range(50)]
    item_level_trend = [np.random.normal(0.005, 0.003) for _ in range(50)]
    start_date = "2013-01-01"
    end_date = "2017-12-31"
    pred_start_date = "2018-01-01"
    pred_date = "2018-03-31"
    dates = pd.date_range(start=start_date, end=end_date)
    pred_dates = pd.date_range(start=pred_start_date, end=pred_date)

    new_data = []
    pred_data = []
    for store_idx in range(1, 10 + 1):
        for item_idx in range(1, 50 + 1):
            res = simulate_seasonal_term_frequency_domain(
                period=375,
                num_simulations=len(dates) + 180,
                harmonics_sin=list([1.2]),
                harmonics_cos=list([1.2]),
                noise_std=store_level_variance[store_idx - 1],
                ar=0.7,
                ma=0.1,
                trend=item_level_trend[item_idx - 1],
                offset=item_level_baseline[item_idx - 1] +
                store_level_baseline_offset[store_idx - 1]
            )
            new_data.append(pd.DataFrame({
                'date': dates,
                'store': [store_idx for _ in range(len(res[180:]))],
                'item': [item_idx for _ in range(len(res[180:]))],
                'sales': np.ceil(res[180:]).clip(min=0).astype(int)
            })
            )
            pred_data.append(pd.DataFrame({
                'date': pred_dates,
                'store': [store_idx for _ in range(len(pred_dates))],
                'item': [item_idx for _ in range(len(pred_dates))],
                'sales': [-1 for _ in range(len(pred_dates))]
            }))

    final_df = pd.concat(new_data)
    pred_df = pd.concat(pred_data)

    final_df.to_csv(FLAGS.save_path + 'train.csv', index=False)
    pred_df.to_csv(FLAGS.save_path + 'test.csv', index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p',
                    '--save_path',
                    type=str,
                    required=True,
                    default=None,
                    help='used to define the path where synthetic data should be saved.')
    FLAGS = parser.parse_args()
    main(FLAGS)
