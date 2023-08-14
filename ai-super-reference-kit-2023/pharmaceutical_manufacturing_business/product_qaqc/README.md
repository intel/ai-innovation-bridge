## Robotics Predictive Maintenance Lifecycle Solution Component
Presenting our advanced visual quality control tool that leverages Intel Extension for PyTorch to fine-tune a model for detecting faulty pills in the production line. With the added power of Xeon CPUs and collaboration with OpenVINO, our tool ensures efficient inference at the edge, enabling real-time identification of defective pills for enhanced quality control in manufacturing processes.

![image](https://github.com/eduand-alvarez/lifecycle-solution-1/assets/57263404/81c4b2b0-de8c-4a37-9ee0-8a467a1d88ae)

## Technology Stack
This prototype component is designed to leverage the powerful Intel Xeon Scalable Processors for training on the Intel Developer Cloud. The solution provides convenient scripts for application deployment on 4th Generation Xeon VMs. For inference, we utilize the accelerated capabilities of OpenVINO on Xeon VMs or Intel ARC GPUs. To enhance the training and inference stages of the machine learning pipeline, we leverage the Intel Extension for PyTorch from the AI analytics toolkit. Additionally, we employ Intel Scikit-Learn Extension for efficient data processing, Torchvision for data augmentation, the Hugging Face transformers library for foundational model access, and ONNX for model interoperability. The "Visual Quality Inspection" AI Reference Kit is the starting point for development. Within the DevOps framework, we utilize FastAPI for building API endpoints, Docker for easy application containerization, and the OpenVINO Model Server (OVMS) specifically for efficient model serving during the inference phase.

![image](https://github.com/eduand-alvarez/lifecycle-solution-1/assets/57263404/f8529f25-3b43-4277-8e20-02216f120247)


## Deployment Options

#### Deploying Locally with Conda Environment
1. Navigate to the src folder
2. Run `python main.py`

#### Deploying Locally with Docker
1. Inside the component folder run `docker build -t qa_image .`
2. Start container `docker run -d -p 5001:5001 qa_image`

#### Automated Deployment using Make
1. Inside the component folder run `make full_deployment`

## Additional Resources

[Original AI Reference Kit for Visual Quality Inspection](https://github.com/oneapi-src/visual-quality-inspection)
