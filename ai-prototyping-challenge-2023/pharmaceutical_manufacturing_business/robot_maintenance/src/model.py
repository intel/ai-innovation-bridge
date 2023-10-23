from pydantic import BaseModel

class PredictionPayload(BaseModel):
    sample: list
    model: str
    num_class: int = 3
    
class TrainPayload(BaseModel):
    file: str
    model_name: str
    model_path: str
    test_size: int = 25  
    ncpu: int = 4 
    