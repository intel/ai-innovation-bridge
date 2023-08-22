# Deployment Instructions
These are the docker-compose-based deployment instructions for this Super Kit. There are two different types of deployment, slim and full: 
- Slim Deployment: Prepares data and launches services for 1/4 (Robotic Maintenance) components. This deployment is designed for quick demos and infrastructure with less than 30Gbs of storage. 
  1. Navigate to the **/setup** directory
  2. Run `make install-tools` to setup dependencies
  3. Run `make launch-slim` to launch the application
  4. Front-end is hard-coded to run on port 5005 - open http://localhost:5005 on your local browser to access the frontend.
  5. To shutdown app, run **make shutdown-slim** - this will shutdown and remove docker containers but leaves images.

- Full Deployment: Prepares data and launches services for 4/4 components. This deployment is designed for full prototype utilization. 
  1. Navigate to the **/setup** directory
  2. Run `make install-tools` to setup dependencies
  3. Run `make launch-full` to launch the application
  4. Front-end is hard-coded to run on port 5005 - open http://localhost:5005 on your local browser to access the frontend.
  5. To shutdown app, run **make shutdown-full** - this will shutdown and remove docker containers but leaves images.
