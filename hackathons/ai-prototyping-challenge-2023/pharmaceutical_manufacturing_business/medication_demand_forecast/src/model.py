from pydantic import BaseModel

class TrainPayload(BaseModel):
    filepath: str
    window: int = 129
    lag_size: int = 1
    test_size: float = 0.3
    epochs: int = 10
    batch_size: int = 512
    save_model_dir: str = None
# class PredictionPayload(BaseModel):

class PredictionPayload(BaseModel):
    keras_saved_model_dir: str
    output_saved_dir: str
    input_file: str
    results_save_dir: str
    window: int = 129
    lag_size: int = 1 
    batch_size: int = 512
    num_iters: int = 100