# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

# pylint: disable=C0415,E0401,R0914,E1129,E0611

"""
Run inference with benchmarks on Tensorflow native models.

Code adopted from
https://www.kaggle.com/code/dimitreoliveira/deep-learning-for-time-series-forecasting/notebook
"""

import logging
import math
import os
import pathlib
import warnings

import numpy as np
import tensorflow as tf
print("TensorFlow Version:", tf.__version__)

from utils.load_data import read_data, series_to_supervised, prepare_data

warnings.filterwarnings("ignore")
tf.keras.utils.set_random_seed(42)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def load_pb(in_model: str) -> tf.compat.v1.Graph:
    """Load a frozen graph from a .pb file

    Args:
        in_model (str): .pb file

    Returns:
        tf.compat.v1.Graph: tensorflow graph version
    """
    detection_graph = tf.compat.v1.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.compat.v1.GraphDef()
        with tf.compat.v1.gfile.GFile(in_model, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.compat.v1.import_graph_def(od_graph_def, name='')
    return detection_graph


def get_concrete_function(graph_def: tf.compat.v1.Graph):
    """Get a concrete function from a TF graph to
    make a callable

    Args:
        graph_def (tf.compat.v1.Graph): Graph to turn into a callable
    """

    def imports_graph_def():
        tf.compat.v1.import_graph_def(graph_def, name="")

    wrap_function = tf.compat.v1.wrap_function(imports_graph_def, [])
    graph = wrap_function.graph

    return wrap_function.prune(
        tf.nest.map_structure(graph.as_graph_element, ["x:0"]),
        tf.nest.map_structure(graph.as_graph_element, ["Identity:0"]))


def inference(input_file: str,
                saved_frozen_model: str,
                results_save_dir: str,
                window = 129, 
                lag_size = 1,  
                batch_size = 512, 
                num_iters = 100):
    """Run inference with benchmarking for the CNN-LSTM model.

    Args:
        flags : run flags
    """
    # prepare data for prediction
 

    # read in data files
    if not os.path.exists(input_file):
        print(f"Data file {input_file} not found")
        return

    test = read_data(input_file)
    series, labels = series_to_supervised(
        test,
        window=window,
        lag=lag_size
    )

    # load model which is saved as a frozen graph
    model = load_pb(saved_frozen_model)

    
    
    concrete_function = get_concrete_function(
        graph_def=model.as_graph_def()
    )

    
    # series = series[labels == -1]
    # labels = labels[labels == -1]

    x_test, x_labels = series, labels.values
    x_test_sub, _ = prepare_data(
        x_test.drop(['date', 'item', 'store'], axis=1), x_labels, 2
    )
    predictions = []

    for i in range(math.ceil(len(x_test_sub)/batch_size)):
        #print(x_test_sub.shape)
        btch = tf.constant(
            x_test_sub[batch_size * i: batch_size * (i+1)],
            dtype=tf.float32)
        res = concrete_function(x=btch)[0]
        predictions.append(res.numpy())
        

    out_df = x_test[['date', 'item', 'store']]
    
    out_df['prediction'] = np.vstack(predictions)

    path = pathlib.Path(results_save_dir)
    path.mkdir(parents=True, exist_ok=True)
    
    out_df.to_json(path_or_buf = os.path.join(results_save_dir, "results.json"), orient="records")
    
    return os.path.join(results_save_dir, "results.json")
    