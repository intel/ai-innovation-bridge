# AI Reference Kit Prototyping Framework

Whether you’re a formal enterprise or getting a startup off the ground, the prototype is an essential tool to help us accomplish the following chief aims:

- Verify that the proposed solution solves the identified problem.
- Justify investment into future product development.
- Recruit supporters of your idea. 

The **AI Reference Kit Prototyping Framework** enables developers to focus on the above by ensuring that composing a prototype doesn’t involve writing too much boilerplate ML code and that there’s a clear path from ideation to an attractive demo. 

### What is an AI Reference Kit Prototype? 
An “AI Reference Kit Prototype” comprises distinct product lifecycle components that have been re-imagined — transforming them from legacy implementation to machine learning solutions powered by the Intel hardware and software stack with integrations of popular open-source tools (Figure 1). 

![image](https://github.com/intel/AI-Hackathon/assets/57263404/3a10f14a-0385-4828-8d31-83247ab1b2d3)

Each component of the prototyping framework starts with an AI Reference Kit and/or Edge AI Reference Kit refactored to enable a pseudo-microservice architecture (Figure 2). Refactoring the original kit makes integrating the final product into more complex applications easier.

![image](https://github.com/intel/AI-Hackathon/assets/57263404/15f5b6aa-6c25-4a25-96e5-8cffd82a3dce)

This framework is ideal for simultaneously prototyping multiple parts of a workflow, showcasing how an optimized end-to-end solution could be made with Intel components to address a complex industry challenge. Let’s explore the framework below. 

## The AI Reference Kit Prototyping Framework
The framework is a simple set of steps for developers to follow as they leverage the AI Reference Kits to build prototypes. We will review these steps within the context of the AI Kit Prototype for the Pharmaceutical Manufacturing Business, which serves as the exemplary kit for this framework. The code for this example can be found here. 

### Pharmaceutical Manufacturing Business Prototype
The AI Reference Kit prototype, “Pharmaceuticals Manufacturing Business,” integrates cutting-edge tools to streamline and enhance pharmaceutical production processes. 

- Demand Forecasting Module: employs a time series prediction CNN-LSTM model optimized for Intel® 4th Generation Xeon® Scalable processors using Intel® Extensions for TensorFlow, ensuring accurate demand projections for various products across multiple locales. 
- Predictive Asset Maintenance Module: utilizes an XGBoost classifier with the Intel® Extension for Scikit-Learn to preemptively flag equipment needing service.
- Visual Anomaly Detection Module: Based on VGG-16 or Padim models, visual anomaly detection capabilities are embedded to quickly determine product quality via visual inspection, leveraging technologies such as OpenVINO and Anomalib.
- GenAI Chatbot Module: Complementing these is a generative AI chatbot powered by GPT4all-J LLM and RAG, tailored for interactions related to robotic maintenance situations.
  
All components are adeptly optimized for the Intel® 4th Generation Xeon® Scalable processors, demonstrating the convergence of AI innovation and pharmaceutical manufacturing.

### How we built the Pharmaceutical Manufacturing Business Kit
1. Picking the Kits: After identifying that we wanted to address inefficiencies in the pharmaceutical manufacturing lifecycle, we explored the AI Reference Kits and Edge AI Reference Kits to identify use cases (Figure 3) that closely resembled the challenges we wanted to solve with our prototype.

![image](https://github.com/intel/AI-Hackathon/assets/57263404/6abe23e4-19e2-4cd7-919e-a010e3885420)

2. Cloning the Repos: After identifying the Demand Forecasting, Visual QA/QC, Predictive Maintenance, and Chatbot reference kits, we cloned the appropriate repositories to gain access to the source code. For example, to clone the Predictive Asset Maintenance Kit, run `git clone https://github.com/oneapi-src/predictive-asset-health-analytics.git`

3. Refactoring Kits: The reference kits were structured as command-line Python scripts. Consequently, we refined these scripts into Python modules and libraries, preparing them for seamless integration with the APIs we planned to develop subsequently. 

  For example, we refactored the Predictive Asset Maintenance Kit, originally designed to predict when powerlines need to be maintained. We pivoted the   original use case into a predictive tool for maintaining robotics equipment on the pharma product production line.
  
  This is where you’re expected to spend most of your time as you refactor and pivot the original use case. The time savings come from leveraging the boilerplate code already available in the kits.

4. Creating FastAPI Endpoints: The following steps involve building API endpoints, preferably using FastAPI or another Python API tool, and setting up the frontend using Streamlit. Below is the FastAPI script used to create and deploy the endpoints supporting the machine learning logic on a uvicorn server.

```python
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
```
In the script above, we built three separate endpoints that respond to client requests through a standard REST API: 

**/ping endpoint:** returns “Server is Running” when the server is up. 
**/train endpoint:** receives training parameters and data and returns the location of the trained XGBoost classifier. 
**/predict endpoint:** receives the location of the trained classifier and raw data and returns maintenance classification. 

5. Building and Connecting the Frontend: We leverage the Streamlit low-code frontend developer framework to build a multi-page web application. Each component of the application has its front-end Streamlit script. The script for each pharma manufacturing frontend component can be found here.

![gifapp](https://github.com/intel/AI-Hackathon/assets/57263404/d7beb17e-8196-44cc-ad05-b32b4d38c344)

The frontend and backend are connected using HTTP protocols. The endpoints are hardcoded into the front-end scripts but can be adapted to accommodate various deployment environments. If you intend to make this change, you can adjust the URL value in the Streamlit scripts. 

```python
URL = 'http://robot_maintenance:5003/train'
DATA = {'file':data_file, 'model_name':model_name, 'model_path':model_path, 
                  'test_size': test_size, 'ncpu': 4}
TRAINING_RESPONSE = requests.post(url = URL, json = DATA)
```

To make changes to the UI components, we recommend visiting Streamlit’s API Documentation.

6. Configuring Deployment Tools: As far as deployment goes, the framework leverages docker and docker-compose to manage the containerization and simultaneous deployment of multiple services. For more complex deployments, consider leveraging a container management tool like Kubernetes.

As an example, in the following dockerfile, we configure the predictive maintenance image: 

```yaml
FROM public.ecr.aws/docker/library/python:3.8

# copy assets over to image
COPY /src /robot_maintenance

# set the working directory
WORKDIR /robot_maintenance

# install dependancies
RUN pip3 install --user --no-cache-dir -r requirements.txt

# set PATH
ENV PATH=.local/bin:$PATH

# exposing endpoint port
EXPOSE 5003

ENTRYPOINT ["python", "serve.py"]
```
We use Python 3.8 from the AWS ECR Docker library. The config copies the ‘src’ folder to a ‘robot_maintenance’ directory in the image and sets it as the working directory. Dependencies are installed from ‘requirements.txt’ without caching. The PATH environment variable is adjusted, port 5003 is exposed, and the container runs ‘serve.py’ on startup.

Using docker-compose, in the absence of an object store or database, we bind a local directory to serve as a data layer across the application. This is not typically done in a production setting but works well for prototyping. The following docker-compose config file shows how this tool configures each of the four services and the frontend for deployment.

```yaml
version: '3'
services:

  medication_demand_forecast:
    build:
      context: ../medication_demand_forecast/
      dockerfile: Dockerfile
    ports:
      - 5001:5001
    volumes:
      - <local directory>:<target container directory>
    restart: on-failure

  medication_qaqc:
    build:
      context: ../medication_qaqc/
      dockerfile: Dockerfile
    ports:
      - 5002:5002
    shm_size: '20gb'
    volumes:
      - <local directory>:<target container directory>
    restart: on-failure

  robot_maintenance:
    build:
      context: ../robot_maintenance/
      dockerfile: Dockerfile
    ports:
      - 5003:5003
    volumes:
      - <local directory>:<target container directory>
    restart: on-failure

  supportbot_chatbot:
    build:
      context: ../supportbot_chatbot/
      dockerfile: Dockerfile
    ports:
      - 5004:5004
    volumes:
      - <local directory>:<target container directory>
    restart: on-failure

  app_frontend:
    build:
      context: ../app_frontend/
      dockerfile: Dockerfile
    ports:
      - 5005:5005
    volumes:
      - <local directory>:<target container directory>
    restart: on-failure
```

9. Managing Configurations with Make: An option for efficient setup and deployment from the command line, we leveraged the Linux make utility. You can find the make file for this prototype here. 

## Summary: 
The article discusses the AI Reference Kit Prototyping Framework, powered by Intel’s AI Reference Kits and open-source software, designed to streamline AI prototype development. The framework aids in transforming traditional components into ML solutions optimized for Intel’s hardware and software, incorporating popular open-source tools. This framework allows developers to efficiently prototype various workflows, as illustrated with the AI Reference Kit prototype for the Pharmaceutical Manufacturing Business.

A few exciting things to try would be:

- Join the Intel Developer Cloud, start an instance, clone the repository, and launch the Pharmaceutical Manufacturing prototype. 
- Start exploring the AI Reference Kit Library and Edge AI Reference Kits for opportunities to build meaningful prototypes using this framework. 

