# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

# pylint: disable=C0415,E0401,R0914,E0611,W0108

"""
Convert a keras saved model to a frozen graph.
"""
import argparse
import os
import pathlib
import warnings



import tensorflow as tf




from tensorflow.python.framework.convert_to_constants import \
    convert_variables_to_constants_v2


warnings.filterwarnings("ignore")


def convert_keras_to_frozen_graph(keras_saved_model_dir: str, 
                                    output_saved_dir: str):


    """Convert a keras saved model to a frozen graph.

    """
    
    model = tf.keras.models.load_model(keras_saved_model_dir)

    full_model = tf.function(lambda x: model(x))
    concrete_function = full_model.get_concrete_function(
        x=tf.TensorSpec(model.inputs[0].shape, model.inputs[0].dtype))
    frozen_model = convert_variables_to_constants_v2(concrete_function)

    path = pathlib.Path(output_saved_dir)
    path.mkdir(parents=True, exist_ok=True)

    tf.io.write_graph(
        graph_or_graph_def=frozen_model.graph,
        logdir='.',
        name=os.path.join(output_saved_dir, "saved_frozen_model.pb"),
        as_text=False
    )

    return os.path.join(output_saved_dir, "saved_frozen_model.pb")




