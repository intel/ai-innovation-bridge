## Healthcare ChatBot Lifecycle Component
The Healthcare ChatBot component "MedBot" is a generative AI question-answering model based on the open-source LLM, gpt4all-j. The performance of this model is augmented by leveraging a similarity search and prompt injection through the Langchain library. 

![image](https://github.com/eduand-alvarez/lifecycle-solution-1/assets/57263404/511e9f64-ab32-4cc9-a62a-bbe015f762e6)


## Technology Stack
 This component is specifically designed to utilize the power of Intel Xeon Scalable Processors on the Intel Developer Cloud. It incorporates convenient scripts that streamline the application launch process on 4th Generation Xeon VMs. Lanchain and Hugging Face libraries are utilized for the management of the LLM lifecycle, including data prep, vector index generation, document loading for similarity search, and prompt engineering. PyTorch 2.0 is our deep learning framework, providing a wealth of oneDNN-based deep learning accelerations optimized for Xeon CPU processors. As a foundation, we utilize an un-released AI Reference Kit to kickstart development. Within the DevOps framework, we employ FastAPI for building API endpoints, Docker for easy application containerization, and chromadb as a vector database for efficient similarity search during prompt engineering in the inference stage.

![image](https://github.com/eduand-alvarez/lifecycle-solution-1/assets/57263404/b0f88ad3-c67c-4b2c-a525-7d3ce0b6b132)


## Deployment Options

#### Deploying Locally with Conda Environment
1. Navigate to the src folder
2. Run `python main.py`

#### Deploying Locally with Docker
1. Inside the component folder run `docker build -t chatbot_image .`
2. Start container `docker run -d -p 5004:5004 chatbot_image`

#### Automated Deployment using Make
1. Inside the component folder run `make full_deployment`

## Additional Resources
