# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2023 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

# pylint: disable=C0415,E0401,R0914

import uvicorn
import io

from fastapi import FastAPI, Response
from ipex.utils.CustomVGG import CustomVGG
from ipex.training.TrainModel import TrainModel
from ipex.utils.logger import log
from ipex.inference.predict import cv_evaluator
from vino.train import AnomalibPills
from vino.predict import inference
from PIL import Image

from model import PredictionPayload_ANOMALIB, PredictionPayload_IPEX, TrainPayload_ANOMALIB, TrainPayload_IPEX

app = FastAPI()

@app.get("/ping")
async def ping():
    """Ping server to determine status

    Returns
    -------
    API response
        response from server on health status
    """
    return {"message":"Server is Running"}

@app.post("/train-openvino")
async def train(payload:TrainPayload_ANOMALIB):

    anomalib_pills = AnomalibPills()
    anomalib_pills.data_proc(data_path = payload.data_path, img_size = payload.img_size, 
                             batch_size = payload.batch_size, n_threads = payload.n_threads)
    anomalib_pills.train(modeldir = payload.modeldir, model = payload.model, layers = payload.layers)
    results = anomalib_pills.validation()
    return {"msg": "Model trained succesfully", "Validation Results": results}

@app.post("/predict-openvino")
async def predict(payload:PredictionPayload_ANOMALIB):
    
    output_image = inference(openvino_model_path = payload.openvino_model_path, metadata_path = payload.metadata_path, 
                             image_path = payload.image_path, device = payload.device)
    
    # Convert the NumPy array to a PIL Image
    pill_image = Image.fromarray(output_image)
    
     # Create an in-memory buffer to store the image
    img_buffer = io.BytesIO()
    
    # Save the PIL Image to the buffer in PNG format (you can use other formats like JPEG, BMP, etc.)
    pill_image.save(img_buffer, format="PNG")
    
    # Get the image data from the buffer
    img_bytes = img_buffer.getvalue()
    
    # Close the buffer
    img_buffer.close()
    
    headers = {
        "Content-Disposition": "attachment; filename=pill_image.png",
        "Content-Type": "image/png",
    }
    
    return Response(content=img_bytes, headers=headers)

@app.post("/train-ipex")
async def train(payload:TrainPayload_IPEX):

    vgg = CustomVGG()
    clf = TrainModel(vgg, payload.data_folder, payload.neg_class)
    clf.get_train_test_loaders(batch_size=5)
    log.info(f"Built train test loaders")
    epoch_loss, epoch_acc = clf.train(epochs=payload.epochs, learning_rate= payload.learning_rate, data_aug=payload.data_aug)
    log.info(f"Successfully Trained Model - Last Epoch Accuracy {epoch_acc} and Last Epoch Loss {epoch_loss}")
    accuracy, balanced_accuracy = clf.evaluate()
    log.info(f"Reporting Evaluation Models - Accuracy {accuracy} and Balanced Accuracy {balanced_accuracy}")
    clf.save_model(model_path=payload.modeldir)
    log.info(f"Successfully saved model to {payload.modeldir}")
    return {"msg": "Model trained succesfully", "Model Location": payload.modeldir}

@app.post("/predict-ipex")
async def predict(payload:PredictionPayload_IPEX):

    y_pred_blind, file_list = cv_evaluator(trained_model=payload.trained_model_path, data_folder=payload.data_folder, batch_size=payload.batch_size)
    log.info(f'Prediction labels: {y_pred_blind} and associated files: {file_list}')
    return {"msg": "Model Inference Complete", "Prediction Output": list(zip(y_pred_blind,file_list))} 

if __name__ == "__main__":
    uvicorn.run("serve:app", host="0.0.0.0", port=5002, log_level="info")