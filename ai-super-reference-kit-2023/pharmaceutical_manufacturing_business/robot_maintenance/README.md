## Robotics Predictive Maintenance Lifecycle Solution Component
Introducing our cutting-edge predictive maintenance tool that harnesses the power of the Intel oneDAL library on Xeon CPUs to accelerate XGBoost inference. By leveraging advanced acceleration techniques, our tool enables accurate prediction of maintenance needs, helping you proactively address issues before breakdowns occur and ensuring uninterrupted operations and optimized maintenance schedules.

![image](https://github.com/eduand-alvarez/lifecycle-solution-1/assets/57263404/7bdaf074-1cb2-4483-98d5-fef6e16bcfc3)

## Technology Stack

This component is a comprehensive solution that utilizes the power of Intel Xeon Scalable Processors on the Intel Developer Cloud. It includes a set of convenient scripts to facilitate the seamless deployment of the application on 4th Generation Xeon VMs. To enhance the efficiency of data processing and inference in the machine learning pipeline, we leverage the daal4py library and Intel scikit-learn extensions from the AI analytics toolkit. To kickstart the development process, we incorporate the "Predictive Asset Health Analytics" AI Reference Kit. For streamlined deployment, we employ FastAPI to build API endpoints and Docker to containerize our applications, ensuring ease of deployment and management within the DevOps framework.

![image](https://github.com/eduand-alvarez/lifecycle-solution-1/assets/57263404/79971032-1b5f-433d-b103-5c51291e8231)

## Deployment Options

#### Deploying Locally with Conda Environment
1. Navigate to the src folder
2. Run `python main.py`

#### Deploying Locally with Docker
1. Inside the component folder run `docker build -t robotics_image .`
2. Start container `docker run -d -p 5000:5000 robotics_image`

#### Automated Deployment using Make
1. Inside the component folder run `make full_deployment`

## Additional Resources

[Original AI Reference Kit for Predictive Asset Health Analytics](https://github.com/oneapi-src/predictive-asset-health-analytics)
