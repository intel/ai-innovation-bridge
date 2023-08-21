import io

from pathlib import Path

from anomalib.data.utils import read_image, InputNormalizationMethod
from anomalib.deploy import OpenVINOInferencer
from anomalib.data.task_type import TaskType
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint


from anomalib.post_processing import Visualizer, VisualizationMode
from PIL import Image
import matplotlib.pyplot as plt



def inference(openvino_model_path: str, metadata_path: str, image_path: str, device: str = "CPU"):
    
    image = read_image(path=image_path)
    plt.imshow(image)
    
    inferencer = OpenVINOInferencer(
        path=openvino_model_path,  # Path to the OpenVINO IR model.
        metadata=metadata_path,  # Path to the metadata file.
        device=device,  # We would like to run it on an Intel CPU.
    )
    
    predictions = inferencer.predict(image=image)
    
    visualizer = Visualizer(mode=VisualizationMode.FULL, task=TaskType.CLASSIFICATION)
    output_image = visualizer.visualize_image(predictions)
    
    return output_image