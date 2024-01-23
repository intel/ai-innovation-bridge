import anomalib

from pathlib import Path

from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint

from anomalib.data.utils import read_image, InputNormalizationMethod
from anomalib.deploy import OpenVINOInferencer
from anomalib.data.mvtec import MVTec, MVTecDataset
from anomalib.data.task_type import TaskType
from anomalib.models import Padim
from anomalib.post_processing import NormalizationMethod, ThresholdMethod
from anomalib.utils.callbacks import (
    MetricsConfigurationCallback,
    MinMaxNormalizationCallback,
    PostProcessingConfigurationCallback,
)
from anomalib.utils.callbacks.export import ExportCallback, ExportMode


class AnomalibPills():
    
    def __init__(self):
        self.trainer = []
        self.img_size = []
        self.datamodule = []
        self.model = []
    
    def data_proc(self, data_path: str, img_size: int, batch_size: int = 32, n_threads: int = 4):

        self.img_size = img_size
        
        self.datamodule = MVTec(
            root=data_path,
            category="pill",
            image_size=img_size,
            train_batch_size=batch_size,
            eval_batch_size=batch_size,
            num_workers=n_threads,
            task=TaskType.CLASSIFICATION,
            normalization=InputNormalizationMethod.NONE,  # don't apply normalization, as we want to visualize the images
            )
        
        try: 
            self.datamodule.setup()  # Split the data to train/val/test/prediction sets.
            self.datamodule.prepare_data()  # Create train/val/test/predic dataloaders
        
            i, data = next(enumerate(self.datamodule.val_dataloader()))
            print(data.keys())
            print(data["image"].shape)
        except:
            print('Data prep failed, if you have already run this once, it will just skip this step. \
                  If you ahve not downloaded the dataset, please run the preparation scripts and try again.')
        
    
    def train(self, modeldir: str, model: str = "resnet18", layers: list = ["layer1", "layer2", "layer3"]):
        
        # instatiate model with Padim
        self.model = Padim(
            input_size=(self.img_size, self.img_size),
            backbone=model,
            layers=layers,
            )
        
        # create callbacks
        callbacks = [
            MetricsConfigurationCallback(
                task=TaskType.CLASSIFICATION,
                image_metrics=["AUROC"],
            ),
            ModelCheckpoint(
                mode="max",
                monitor="image_AUROC",
            ),
            PostProcessingConfigurationCallback(
                normalization_method=NormalizationMethod.MIN_MAX,
                threshold_method=ThresholdMethod.ADAPTIVE,
            ),
            MinMaxNormalizationCallback(),
            ExportCallback(
                input_size=(self.img_size, self.img_size),
                dirpath=modeldir,
                filename="model",
                export_mode=ExportMode.OPENVINO,
            ),
            ]
        
        
        # train model
        self.trainer = Trainer(
            callbacks=callbacks,
            accelerator="auto",
            auto_scale_batch_size=False,
            check_val_every_n_epoch=1,
            devices=1,
            gpus=None,
            max_epochs=1,
            num_sanity_val_steps=0,
            val_check_interval=1.0,
        )
        self.trainer.fit(model=self.model, datamodule=self.datamodule)
    
    def validation(self):
        return self.trainer.test(model=self.model, datamodule=self.datamodule)