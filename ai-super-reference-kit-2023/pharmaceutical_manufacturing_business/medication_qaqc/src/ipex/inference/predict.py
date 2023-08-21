# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2023 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

# pylint: disable=C0415,E0401,R0914

import numpy as np
import torch
from torch.utils.data import DataLoader
from ipex.inference.DatasetNoLabels import DatasetNoLabels
from ipex.utils.CustomVGG import CustomVGG
import itertools

def blind_dataloader(root, batch_size=5):
    """
    Create blind data loader
    """
    dataset = DatasetNoLabels(root=root)
    print(dataset)
    no_label_loader = DataLoader(dataset, batch_size=batch_size, drop_last=False)
    
    return no_label_loader

def evaluate(model, dataloader, device):
    """
    yields predicted label array
    """
    
    model.to(device)
    model.eval()
        
    y_pred = np.empty(shape=(0,))
    input_files = []
    
    
    for inputs, fn in dataloader:
        inputs = inputs.to(device)
        preds_probs = model(inputs)[0]
        preds_class = torch.argmax(preds_probs, dim=-1)
        preds_class = preds_class.detach().to("cpu").numpy()
        y_pred = np.concatenate((y_pred, preds_class))
        input_files.append(list(fn))
    
    
    file_list = list(itertools.chain.from_iterable(input_files))
    
        
    return y_pred, file_list
    
    
def cv_evaluator(trained_model, data_folder, batch_size):
    """
    main evaluator function that yields prediction array for scoring
    """
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = torch.load(trained_model)
    
    no_label_loader = blind_dataloader(root=data_folder, batch_size=batch_size)
    y_pred_blind, file_list = evaluate(model=model, dataloader=no_label_loader, device=device)
    
    return y_pred_blind, file_list