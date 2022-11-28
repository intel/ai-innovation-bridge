# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

"""System module."""
import os
import shutil
import argparse

if __name__ == "__main__":
    # This code will help to match the bad samples data distribution with good samples
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-d',
                        '--datapath',
                        type=str,
                        required=False,
                        default='dataset/',
                        help='dataset path which consists of train and test folders')
    FLAGS = PARSER.parse_args()
    DATA_FOLDER = FLAGS.datapath
    TARGET_DIRS = ['train', 'test']
    N_CLASSES = ["good", "bad"]
    CNT1, CNT2 = 0, 0
    CLONE_TIMES = 20

    # Clonning only the bad samples as the distribution is low for bad samples
    DATA = os.listdir(DATA_FOLDER)
    for dir_name in DATA:
        if dir_name in TARGET_DIRS:
            for class_folder in N_CLASSES:
                full_files = os.listdir(os.path.join(DATA_FOLDER, dir_name, class_folder))
                for img_path in full_files:
                    full_path = os.path.join(DATA_FOLDER, dir_name, class_folder, img_path)
                    if class_folder == "bad":
                        for i in range(CLONE_TIMES):
                            new_path = os.path.join(DATA_FOLDER, dir_name,
                                                    class_folder, img_path.split(".")[0]+"_" +
                                                    str(i) + "." + img_path.split(".")[1])
                            shutil.copy(full_path, new_path)
                            CNT1 += 1
                    CNT2 += 1
    print("total count", CNT1+CNT2)
