## Healthcare ChatBot Lifecycle Component
The generative AI chatbot component uses a Falcon LLM and Retrieval Augmented Generation (RAG) to respond to queries associated with fictitious robotic maintenance scenarios.  It leverages the PyTorch 2.0, LangChain, and Hugging Face Transformers on Intel® 4th Generation Xeon® Scalable processors. 

![image](https://github.com/intel/AI-Hackathon/assets/57263404/b414f62b-e5ec-42cf-a273-29ba25f7a8aa)

## Technology Stack
This component is specifically designed to utilize the power of Intel Xeon Scalable Processors on the Intel Developer Cloud. It incorporates convenient scripts that streamline the application launch process on 4th Generation Xeon VMs. Lanchain and Hugging Face libraries are utilized for the management of the LLM lifecycle, including data prep, vector index generation, document loading for similarity search, and prompt engineering. PyTorch 2.0 is our deep learning framework, providing a wealth of oneDNN-based deep learning accelerations optimized for Xeon CPU processors. As a foundation, we utilize an un-released AI Reference Kit to kickstart development. Within the DevOps framework, we employ FastAPI for building API endpoints, Docker for easy application containerization, and chromadb as a vector database for efficient similarity search during prompt engineering in the inference stage.
