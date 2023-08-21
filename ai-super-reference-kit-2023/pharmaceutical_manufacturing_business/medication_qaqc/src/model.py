from pydantic import BaseModel

class PredictionPayload_IPEX(BaseModel):
    trained_model_path: str=None
    data_folder: str=None
    batch_size: int=5

class TrainPayload_IPEX(BaseModel):
    data_folder: str=None
    neg_class: int
    modeldir: str=None
    learning_rate: int
    epochs: int
    data_aug: int
    
class PredictionPayload_ANOMALIB(BaseModel):
    openvino_model_path: str=None
    metadata_path: str=None
    image_path: str=None
    device: str = "CPU"

class TrainPayload_ANOMALIB(BaseModel):
    data_path: str = None
    img_size: int = None
    batch_size: int = 32
    n_threads: int = 4
    modeldir: str = None
    model: str = "resnet18", 
    layers: list = ["layer1", "layer2", "layer3"]