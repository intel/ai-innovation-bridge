# Stable Diffusion on Intel 4th Gen Xeon CPUs
Simple Stable Diffusion app using Flask

## Prerequisites, assumes running on Ubuntu 22.04

```bash

# Linux packages
sudo apt update
sudo apt-get -y install python3-pip python-is-python3 git

# Git clone repository 
git clone https://github.com/intel/AI-Hackathon.git

# Enter directory
cd AI-Hackathon/genai-rockstar-challenge-2023

# Python requirements.txt
pip3 install -r requirements.txt
```

## Run application locally

```bash 
python3 app.py
```

## Browse to your web UI 

### Open a browser navigate to your **VM's Public IP address** on port 5000. For example:  

```
40.41.42.43:5000
```

### Your Browser should display the following prompt. Enter a prompt and wait for the results.  

<img width="961" alt="image" src="https://github.com/bconsolvo/stable_diffusion_flask/assets/15691316/5f6ad3b7-f6db-4acb-b0f7-825364c54387">

