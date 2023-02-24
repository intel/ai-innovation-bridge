<h1>AI Startup Olympics Hackathon</h1>

# What's this Hackathon About?
The AI Startup Olympics is a 3-day event dedicated to accelerating the implementation of Intel’s accelerated software and hardware in industry-leading solution architectures. The Hackathon challenge consists of building an ML application according to specifications defined in the “Solution Blueprint.” This blueprint outlines the architectural components that your team must build to support your solution. The blueprint provides enough flexibility for teams to build to choose the data and AI problem they want to solve – which means you can bring your data and code to the hackathon. Teams will be judged on their ability to build according to these specs, solution innovation, and workload optimization. 

![Hack Title Image](assets/Title_Image.png)

# What if you don’t have code or data to bring? 
For teams that don’t have their own code and data to bring to the event, Intel will provide a set of alternative sample solutions with data and code that participants can use as an alternative starting point.  

# Alternative Sample Solutions and Datasets
- [Drone Landing Areas (Computer Vision)](https://github.com/oneapi-src/drone-navigation-inspection)
- [Medical Imaging Diagnostics (Computer Vision)](https://github.com/oneapi-src/medical-imaging-diagnostics)
- [Customer Chatbot (Natural Language Processing)](https://github.com/oneapi-src/customer-chatbot)
- [Disease Prediction (Natural Language Processing)](https://github.com/oneapi-src/disease-prediction)

# Blueprint Description
Build an ML application based on the provided microservice architecture pattern. The design pattern splits data, training, and inference components into individual microservices. 

![Image](assets/Pseduo_Microservice_Architecture.png)

## Blueprint Requirements:
- Application must be split into separate processes containing one or more modules. You must have at least two of the following microservices: data wrangling/processing, training and validation, and inference. 
- Each microservice must be deployed as a containerized application using docker or other popular container management tools. 
- At least one of your two microservices must leverage an intel deep learning accelerated extension. 
- Each microservice must contain an API end-point that can receive HTTP requests in JSON format. 
- The only compute resources and storage for your solution are the 4th Generation Intel Xeon Bare Metal IDC Instance.

## Optional Side Quests: Optional side quests can be awarded additional points. Awarding these points will be at the discretion of judges/mentors.
- Incorporate a working database layer (10pts)
- Add Synchronous or Async. event messaging (10pts)
- Demonstrate the use of OpenMP Topology Optimizations (5pts)
- Leverage an Intel Accelerated Extension in both of your main microservices (7pts)
- Build a model observability or performance tracking microservice. (10pts)
- Include a performance benchmark report in your final presentation (5pts)

*Keep in mind that All components of blueprint specs and side quests are open to interpretation by intel staff supporting the judging process.*









