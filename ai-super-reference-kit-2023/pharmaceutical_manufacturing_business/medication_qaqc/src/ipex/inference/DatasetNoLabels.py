# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2023 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

# pylint: disable=C0415,E0401,R0914

import os
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms



class DatasetNoLabels(Dataset):
    '''
    Dataset class designed for scenarios when you don't have labels
    '''
    def __init__(self, root):
        self.img_transform = transforms.Compose([transforms.Resize((224,224)), transforms.ToTensor()])
        self.img_filenames = self._get_images(root)
        
    @staticmethod
    def _get_images(root):
        image_names = []
        
        folder = "blind"
        folder = os.path.join(root, folder)
        class_images = os.listdir(folder)
        class_images = [os.path.join(folder, image) for image in class_images if image.find(".png") > -1]
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
