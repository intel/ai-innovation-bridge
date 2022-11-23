
<p align="center"><img src="pngs/20220926_hackathon_nlp_track.png" width="600" /></p>

# Welcome to the Natural Language Processing Track! 🚀

Author: Benjamin Consolvo, AI Solutions Engineer Manager at Intel

In this track of the hackathon, you will find two sample notebooks that were used in the NLP track of the AI Hackathon at Intel Innovation 2022. This notebook explores a binary classification humor dataset and optimization techniques for model training, hyperparameter tuning, and inference. 

## Getting Started

### Installation
There is a [requirements.txt](requirements.txt) file with all of the required Python packages. You can use the usual `pip3 install -r requirements.txt` from the command line to install the necessary packages. I have purposefully commented out PyTorch in the last line of the requirements.txt file (`#torch==1.12.0`) because for the Habana Gaudi training portion, you need to use the SynapseAI fork of PyTorch ([see installation guide here](https://docs.habana.ai/en/latest/Installation_Guide/index.html#gaudi-installation-guide)). However, I also have provided a Docker solution below to simplify the process on a Habana Gaudi instance.

### Video Demo
Please visit [this link](https://www.intel.com/content/www/us/en/developer/videos/ai-for-social-good-hackathon.html) to find the video series associated to the Hackathon.

### Dataset
I do not provide the data in this repository. The data can be downloaded from [Kaggle here](https://www.kaggle.com/datasets/deepcontractor/200k-short-texts-for-humor-detection).

### Notebooks
I have provided two demo notebooks:
1. [01_TrainingHumorDetection_HabanaGaudi_Demo.ipynb](01_TrainingHumorDetection_HabanaGaudi_Demo.ipynb) - This notebook goes over training an NLP DistilBERT model for determining if a statement would be considered as humorous or not, on a Habana® Gaudi® HPU accelerator.
2. [02_Quantization_FP32toINT8_NLP_Demo.ipynb](02_Quantization_FP32toINT8_NLP_Demo.ipynb) - This notebook goes over quantizing an NLP model from FP32 to INT8 to greatly increase inference speed!

### Docker
I have provided a [docker-compose.yml](docker-compose.yml) file and a [Dockerfile](Dockerfile) here for the Habana Gaudi instance so that you can run the following command to build 8 individual Docker containers that each only look at 1 of the 8 HPU devices present on the Habana Gaudi instance and start up a Jupyter Labs server:
```
docker compose up -d
```




