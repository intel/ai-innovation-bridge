# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2023 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

# pylint: disable=C0415,E0401,R0914

import torch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import confusion_matrix
from torchvision import transforms
from torchvision import transforms

GOOD_CLASS_FOLDER = "good"
DATASET_SETS = ["train", "test"]
BLIND_DATA = "blind"
IMG_FORMAT = ".png"
INPUT_IMG_SIZE = (224, 224)
NEG_CLASS = 1

def plot_confusion_matrix(y_true, y_pred, class_names="auto"):
    """
    Visualization
    """
    confusion = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=[5, 5])
    sns.heatmap(
        confusion,
        annot=True,
        cbar=False,
        xticklabels=class_names,
        yticklabels=class_names,
    )

    plt.ylabel("True labels")
    plt.xlabel("Predicted labels")
    plt.title("Confusion Matrix")
    plt.show()


def get_bbox_from_heatmap(heatmap, thres=0.8):
    """
    Returns bounding box around the defected area:
    Upper left and lower right corner.
    Threshold affects size of the bounding box.
    The higher the threshold, the wider the bounding box.
    """
    binary_map = heatmap > thres

    x_dim = np.max(binary_map, axis=0) * np.arange(0, binary_map.shape[1])
    x_0 = int(x_dim[x_dim > 0].min())
    x_1 = int(x_dim.max())

    y_dim = np.max(binary_map, axis=1) * np.arange(0, binary_map.shape[0])
    y_0 = int(y_dim[y_dim > 0].min())
    y_1 = int(y_dim.max())

    return x_0, y_0, x_1, y_1

def data_augmentation(inputs, labels):

    img_p = transforms.ToPILImage()
    img_filp_transform = transforms.Compose(
            [transforms.Resize(INPUT_IMG_SIZE),
             transforms.RandomHorizontalFlip(), transforms.ToTensor()])
    img_crop_transform = transforms.Compose(
            [transforms.Resize(INPUT_IMG_SIZE),
             transforms.CenterCrop(224), transforms.ToTensor()])
    img_rotation_transform = transforms.Compose(
            [transforms.Resize(INPUT_IMG_SIZE),
             transforms.RandomRotation(25), transforms.ToTensor()])
    img_enhance_transform = transforms.Compose(
            [transforms.Resize(INPUT_IMG_SIZE), transforms.ColorJitter(
                brightness=0.3, contrast=0.3,
                saturation=0.3, hue=0.2), transforms.ToTensor()])
    n_inputs = []
    n_labels = []
    for i, _ in enumerate(inputs):
        n_inputs.append(inputs[i])
        n_labels.append(labels[i])
        img_filp = img_filp_transform(img_p(inputs[i]))
        n_inputs.append(img_filp)
        n_labels.append(labels[i])
        img_crop = img_crop_transform(img_p(inputs[i]))
        n_inputs.append(img_crop)
        n_labels.append(labels[i])
        img_rotation = img_rotation_transform(img_p(inputs[i]))
        n_inputs.append(img_rotation)
        n_labels.append(labels[i])
        img_enhance = img_enhance_transform(img_p(inputs[i]))
        n_inputs.append(img_enhance)
        n_labels.append(labels[i])
    return torch.stack(n_inputs, 0), torch.stack(n_labels, 0)