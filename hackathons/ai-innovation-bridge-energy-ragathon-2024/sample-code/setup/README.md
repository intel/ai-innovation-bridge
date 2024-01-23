# Deployment Instructions
These are the docker-compose-based deployment instructions for this sample:
- Slim Deployment: Prepares data and launches services for 1/4 (Robotic Maintenance) components. This deployment is designed for quick demos and infrastructure with less than 30Gbs of storage. 
  1. Navigate to the **/setup** directory
  2. Run `make install-dockertools` to setup docker dependencies
  3. Run `make setup-store-full` to setup data and model store
  3. Run `make launch-rag` to launch the application
  4. Front-end is hard-coded to run on port 5005 - open http://localhost:5005 on your local browser to access the frontend.
  5. To shutdown app, run **make shutdown-rag** - this will shutdown and remove docker containers but leaves images.