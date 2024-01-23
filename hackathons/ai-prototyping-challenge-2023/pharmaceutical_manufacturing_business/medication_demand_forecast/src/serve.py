import uvicorn
import logging
import warnings

from fastapi import FastAPI
from model import TrainPayload, PredictionPayload
from train import train_model
from utils import freeze
from predict import inference

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
    This endpoint process raw data and trains an LSTM model

    Parameters
    ----------
    payload : TrainPayload
        Training endpoint payload model

    Returns
    -------
    API response
        Accuracy metrics and other logger feedback on training progress.
    """
    model = train_model(payload.filepath, 
                        payload.window, 
                        payload.lag_size,
                        payload.test_size,
                        payload.epochs,
                        payload.batch_size)

    model.process_data()

    logger.info("Data successfully processed")

    model.fit_lstm_model(save_model_dir = payload.save_model_dir)

    logger.info("Demand forecasting Model successfully trained")

    accuracy_score = model.validate()

    return {"msg": "Model trained succesfully", "validation scores": accuracy_score}
    #pass


@app.post("/predict")
async def predict(payload: PredictionPayload):
    """Prediction Endpoint
    This endpoint freezes a trained model and performs inference

    Parameters
    ----------
    payload : PredictionPayload
        Prediction endpoint payload model

    Returns
    -------
    API response
        Results of inference and other logger feedback
    """
    #may need to pass in frozen_model path
    frozen_model_path = freeze.convert_keras_to_frozen_graph(payload.keras_saved_model_dir, payload.output_saved_dir)
    results = inference(payload.input_file, 
                        frozen_model_path, 
                        payload.results_save_dir,
                        payload.window, 
                        payload.lag_size, 
                        payload.batch_size, 
                        payload.num_iters)
    return {"msg": "Completed Inference", "Result": results}



if __name__ == "__main__":
    uvicorn.run("serve:app", host="0.0.0.0", port=5001, log_level="info")