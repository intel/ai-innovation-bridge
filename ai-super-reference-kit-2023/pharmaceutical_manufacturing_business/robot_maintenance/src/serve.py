import uvicorn
from fastapi import FastAPI
import logging
import warnings
from predict import inference
import pandas as pd

from fastapi import FastAPI
from model import TrainPayload, PredictionPayload
from train import RoboMaintenance

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")


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
    """Training Endpoint
    This endpoint process raw data and trains an XGBoost Classifier and converts it to daal4py format.

    Parameters
    ----------
    payload : TrainPayload
        Training endpoint payload model

    Returns
    -------
    API response
        Accuracy metrics and other logger feedback on training progress.
    """
    model = RoboMaintenance(payload.model_name)
    model.process_data(payload.file, payload.test_size)
    logger.info("Data has been successfully processed")
    model.train(payload.ncpu)
    logger.info("Robotic Maintenance Model Successfully Trained")
    model.save(payload.model_path)
    logger.info("Saved Robotic Maintenance Model")
    accuracy_score = model.validate()
    return {"msg": "Model trained succesfully", "validation scores": accuracy_score}

@app.post("/predict")
async def predict(payload:PredictionPayload):
    
    sample = pd.json_normalize(payload.sample)
    results = inference(data = sample, model = payload.model, num_class = payload.num_class)
    return {"msg": "Completed Analysis", "Maintenance Recommendation": results}

if __name__ == "__main__":
    uvicorn.run("serve:app", host="0.0.0.0", port=5003, log_level="info")