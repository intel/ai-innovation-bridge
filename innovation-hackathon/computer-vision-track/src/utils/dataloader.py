# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

"""System module."""
# pylint: disable=E1101,E1102,E0401
import os
import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader, SubsetRandomSampler
from torchvision import transforms
from sklearn.model_selection import train_test_split, StratifiedKFold

from utils.constants import (
    GOOD_CLASS_FOLDER,
    DATASET_SETS,
    BLIND_DATA,
    INPUT_IMG_SIZE,
    IMG_FORMAT,
    NEG_CLASS,
)


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

class MvtecAdDatasetNoLabels(Dataset):
    '''
    Dataset class designed for scenarios when you don't have labels
    '''
    def __init__(self, root):
        self.img_transform = transforms.Compose([transforms.Resize(INPUT_IMG_SIZE), transforms.ToTensor()])
        self.img_filenames = self._get_images(root)
        
    @staticmethod
    def _get_images(root):
        image_names = []
        
        folder = BLIND_DATA
        folder = os.path.join(root, folder)
        class_images = os.listdir(folder)
        class_images = [os.path.join(folder, image) for image in class_images if image.find(IMG_FORMAT) > -1]
        image_names.extend(class_images)
        return image_names
        
    def __len__(self):
        return len(self.img_filenames)

    def __getitem__(self, idx):
        img_path = self.img_filenames[idx]
        img_name = os.path.basename(img_path)
        img = Image.open(img_path)
        img = self.img_transform(img)
        return img, img_name


def get_train_test_loaders(root, batch_size, test_size=0.2, random_state=42, split=True):
    """
    Returns train and test dataloaders.
    Splits dataset in stratified manner, considering various defect types.
    """
    
    if split:
        
        dataset = MvtecAdDataset(root=root)

        train_idx, test_idx = train_test_split(
            np.arange(dataset.__len__()),
            test_size=test_size,
            shuffle=True,
            stratify=dataset.img_labels_detailed,
            random_state=random_state,
        )
        train_sampler = SubsetRandomSampler(train_idx)
        test_sampler = SubsetRandomSampler(test_idx)
    
        train_loader = DataLoader(
            dataset, batch_size=batch_size, sampler=train_sampler, drop_last=True
        )
        test_loader = DataLoader(
            dataset, batch_size=batch_size, sampler=test_sampler, drop_last=False
        )
        return train_loader, test_loader
    
    else:
        
        dataset = MvtecAdDatasetNoLabels(root=root)
        no_label_loader = DataLoader(dataset, batch_size=batch_size, drop_last=False)
        
        return no_label_loader
    