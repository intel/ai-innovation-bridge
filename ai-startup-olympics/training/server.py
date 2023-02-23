# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2023 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

# pylint: disable=C0415,E0401,R0914

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from CustomVGG import CustomVGG
from TrainModel import TrainModel

from utils.logger import log


app = FastAPI()

# payload models
class TrainPayload(BaseModel):
    data_folder: str=None
    neg_class: int
    model_path: str=None

@app.get("/ping")
async def ping():
    """Ping server to determine status

    Returns
    -------
    API response
        response from server on health status
    """
    return {"message":"Server is Running"}

@app.post("/train")
async def train(payload:TrainPayload):

    vgg = CustomVGG()
    clf = TrainModel(vgg, payload.data_folder, payload.neg_class)
    clf.get_train_test_loaders(batch_size=5)
    log.info(f"Built train test loaders")
    epoch_loss, epoch_acc = clf.train()
    log.info(f"Successfully Trained Model - Last Epoch Accuracy {epoch_acc} and Last Epoch Loss {epoch_loss}")
    accuracy, balanced_accuracy = clf.evaluate()
    log.info(f"Reporting Evaluation Models - Accuracy {accuracy} and Balanced Accuracy {balanced_accuracy}")
    clf.save_model(model_path=payload.model_path)
    log.info(f"Successfully saved model to {payload.model_path}")
      
    return {"msg": "Model trained succesfully", "validation accuracy": balanced_accuracy}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=5000, log_level="info")