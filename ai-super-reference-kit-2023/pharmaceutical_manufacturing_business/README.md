# AI Super Reference Kits: Higlighting How to Innovate Legacy with the Intel AI Stack.

AI Super Reference Kits comprise distinct product lifecycle components that have been re-imagined – transforming them from legacy to machine learning solutions powered by the Intel hardware and software AI stack. The enabling technology stack includes components across Intel’s software and hardware portfolio. Each lifecycle component starts with an AI Reference Kit that has been refactored to enable a pseudo-microservice architecture, making them easier to integrate into more complex applications. The integration of multiple kits, showcases how an integrated optimized solution could be made with intel components to address a particular industry challenge. 

![image](https://github.com/intel-innersource/frameworks.ai.ai-hackathon/assets/57263404/cc38d230-e93a-414e-b765-9c8a7f281096)

A few benefits of the super kits include: 
- Quickly prototype unified AI solutions with multiple reference kits
- Leverage sample architecture to plan for scale with essential DevOps tools
- Build with pre-baked Intel AI optimizations

### Available Super AI Reference Kits

- Pharmaceutical Manufacturing Business
- More coming in 2024...

## Pharmaceutical Manufacturing Business "Super Kit": 

The AI Super Reference Kit titled "Pharmaceuticals Manufacturing Business" integrates cutting-edge tools to streamline and enhance pharmaceutical production processes. Firstly, its demand forecasting module employs a time series prediction CNN-LSTM model optimized for Intel® 4th Generation Xeon® Scalable processors using Intel® Extensions for TensorFlow, ensuring accurate demand projections for various products across multiple locales. In tandem, a predictive asset maintenance system utilizes an XGBoost classifier with the Intel® Extension for Scikit-Learn to preemptively flag equipment in need of service. Visual anomaly detection capabilities, based on VGG-16 or Padim models, are embedded to quickly determine product quality via visual inspection, leveraging technologies such as OpenVINO and Anomalib. Complementing these is a generative AI chatbot, powered by GPT4all-J LLM and RAG, tailored for interactions related to fictitious robotic maintenance situations. All components are adeptly optimized for the Intel® 4th Generation Xeon® Scalable processors, demonstrating the convergence of AI innovation and pharmaceutical manufacturing.

![image](https://github.com/intel-innersource/frameworks.ai.ai-hackathon/assets/57263404/93ae98e1-df30-4db6-b56a-8928748957ff)

### Adaptation Flow of Super Kit
The Pharmaceutical Manufacturing Business "Super Kit" was adapted from four different AI reference kits. The process involved an architectural refactoring and new data. With the AI Reference Kit code as the starting point, very little work went into AI/ML components, which allowed us to focus on the architectural and deployment elements of the application. 

![image](https://github.com/intel-innersource/frameworks.ai.ai-hackathon/assets/57263404/70fea86d-087a-4cbb-92f9-d00ec6a0ac7f)

### Package Diagram of Super Kit
The Pharmaceutical Manufacturing Business "Super Kit" contains 5 unique components. Each component contains: 
- /src folder: contains all of the AI/ML code and FastAPI script
- Dockerfile: container instructions - used by docker compose
- README: Basic documentation for the component

  ![image](https://github.com/intel-innersource/frameworks.ai.ai-hackathon/assets/57263404/df6fc5f3-06a8-4ea2-89e3-7fb4ec03cb31)

## What comes with a AI Super Reference Kit?
- AI/ML Source Code
- Documentation
- Docker Container & Docker Compose Config Files
- FastAPI Endpoint Scripts
- Synthetic Data Generation Scripts
- Streamlit WebApp Frontend
- Makefile for easy deployment 

## How to Contribute
If you want to contribute to this project and make it better, your help is very welcome. Contributing is also a great way to learn more about social coding on Github, new technologies and and their ecosystems and how to make constructive, helpful bug reports, feature requests and the noblest of all contributions: a good, clean pull request.

### Contributing your own Lifecycle Solution
If you want to contribute a new solution, please open an issue and we will follow up with you ASAP!

### Implementing Patches and Bug Fixes

- Create a personal fork of the project on Github.
- Clone the fork on your local machine. Your remote repo on Github is called origin.
- Add the original repository as a remote called upstream.
- If you created your fork a while ago be sure to pull upstream changes into your local repository.
- Create a new branch to work on! Branch from develop if it exists, else from master.
- Implement/fix your feature, comment your code.
- Follow the code style of the project, including indentation.
- If the component has tests run them!
- Write or adapt tests as needed.
- Add or change the documentation as needed.
- Squash your commits into a single commit with git's interactive rebase. Create a new branch if necessary.
- Push your branch to your fork on Github, the remote origin.
- From your fork open a pull request in the correct branch. Target the project's develop branch if there is one, else go for master!

If the maintainer requests further changes just push them to your branch. The PR will be updated automatically.
Once the pull request is approved and merged you can pull the changes from upstream to your local repo and delete your extra branch(es).
And last but not least: Always write your commit messages in the present tense. Your commit message should describe what the commit, when applied, does to the code – not what you did to the code.

## Additional Resources
- [AI Reference Kits](https://www.intel.com/content/www/us/en/developer/topic-technology/artificial-intelligence/reference-kit.html)

