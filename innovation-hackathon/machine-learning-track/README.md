<p align="center"><img src="media/ML_AXG-22-11_Software_Dev_Hackathon.png" style="width:800px;border-radius:15px"/></p>

# <p align="center">Welcome to the Machine Learning Track! 🚀</p>

In this track of the hackathon, you will find the sample notebook that was used in Part I of the machine learning track at the Intel<sup>&reg;</sup> Innovation 2022 AI Hackathon. This notebook explores Intel's [Predictive Asset Analytics AI Reference Kit](https://github.com/oneapi-src/predictive-asset-health-analytics) and optimization techniques for model training, hyperparameter tuning, and inference. 

## Getting Started

### Installation

The main libraries used in this notebook include:
- [Intel<sup>&reg;</sup> Distribution of Modin*](https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-of-modin.html#gs.9hqdj4)
- [Intel<sup>&reg;</sup> Extension for Scikit-learn*](https://www.intel.com/content/www/us/en/developer/tools/oneapi/scikit-learn.html#gs.8txte9)
- [XGBoost Optimized for Intel<sup>&reg;</sup> Architecture](https://www.intel.com/content/www/us/en/developer/articles/technical/xgboost-optimized-architecture-getting-started.html)
- [Intel<sup>&reg;</sup> Daal4py](https://intelpython.github.io/daal4py/)

To install all of the Python packages required to run the notebook, use

```
pip3 install -r requirements.txt
```

### Dataset
The dataset used in this demo consists of 100,000 different utility poles with over 30 features on the overall health of the utility. It can be generated following the instructions provided in the Predictive Asset Health Analytics repository [here](https://github.com/oneapi-src/predictive-asset-health-analytics#run-the-code-for-test-dataset-generation-training-the-model-and-prediction). 

### Video Demo
You may also watch a video demo of this notebook [here](https://www.intel.com/content/www/us/en/developer/videos/optimize-utility-maintenance-prediction-ai-kit.html).