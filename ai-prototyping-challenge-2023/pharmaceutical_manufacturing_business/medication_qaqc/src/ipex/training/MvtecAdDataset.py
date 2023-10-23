# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2023 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

# pylint: disable=C0415,E0401,R0914

import os
import torch
import numpy as np


from torchvision import transforms
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms

GOOD_CLASS_FOLDER = "good"
DATASET_SETS = ["train", "test"]
BLIND_DATA = "blind"
IMG_FORMAT = ".png"
INPUT_IMG_SIZE = (224, 224)
NEG_CLASS = 1

class MvtecAdDataset(Dataset):
    """
    Class to load subsets of MVTEC ANOMALY DETECTION DATASET
    Dataset Link: https://www.mvtec.com/company/research/datasets/mvtec-ad
    Root is path to the subset, for instance, `mvtec_anomaly_detection/leather`
    """

    def __init__(self, root):
        self.classes = ["Good", "Anomaly"] if NEG_CLASS == 1 else ["Anomaly", "Good"]
        self.img_transform = transforms.Compose(
            [transforms.Resize(INPUT_IMG_SIZE), transforms.ToTensor()]
        )

        (
            self.img_filenames,
            self.img_labels,
            self.img_labels_detailed,
        ) = self._get_images_and_labels(root)

    @staticmethod
    def _get_images_and_labels(root):
        image_names = []
        labels = []
        labels_detailed = []

        for folder in DATASET_SETS:
            folder = os.path.join(root, folder)

            for class_folder in os.listdir(folder):
                label = (
                    1 - NEG_CLASS if class_folder == GOOD_CLASS_FOLDER else NEG_CLASS
                )
                label_detailed = class_folder

                class_folder = os.path.join(folder, class_folder)
                class_images = os.listdir(class_folder)
                class_images = [
                    os.path.join(class_folder, image)
                    for image in class_images
                    if image.find(IMG_FORMAT) > -1
                ]

                image_names.extend(class_images)
                labels.extend([label] * len(class_images))
                labels_detailed.extend([label_detailed] * len(class_images))

        print(f"Dataset {root}: N Images = {len(labels)}, "
              f"Share of anomalies = {np.sum(labels) / len(labels):.3f}")
        return image_names, labels, labels_detailed

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_fn = self.img_filenames[idx]
        label = self.img_labels[idx]
        img = Image.open(img_fn)
        img = self.img_transform(img)
        label = torch.as_tensor(label, dtype=torch.long)
        return img, label