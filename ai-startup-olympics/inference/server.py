# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2023 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

# pylint: disable=C0415,E0401,R0914

import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel

from utils.logger import log

from predict import cv_evaluator



app = FastAPI()

# payload models
class PredictionPayload(BaseModel):
    trained_model_path: str=None
    data_folder: str=None
    batch_size: int=5

@app.get("/ping")
async def ping():
    """Ping server to determine status

    Returns
    -------
    API response
        response from server on health status
    """
    return {"message":"Server is Running"}


@app.post("/predict")
async def predict(payload:PredictionPayload):

    y_pred_blind, file_list = cv_evaluator(trained_model=payload.trained_model_path, data_folder=payload.data_folder, batch_size=payload.batch_size)
    log.info(f'Prediction labels: {y_pred_blind} and associated files: {file_list}')
    return {"msg": "Model Inference Complete", "Prediction Output": list(zip(y_pred_blind,file_list))} 

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=5001, log_level="info")