FROM vault.habana.ai/gaudi-docker/1.11.0/ubuntu22.04/habanalabs/pytorch-installer-2.0.1:latest
SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND noninteractive\
    OMPI_MCA_btl_vader_single_copy_mechanism none

RUN apt-get update -y --no-install-recommends &&\
    apt-get install htop -y --no-install-recommends &&\
    apt-get install sudo -y  --no-install-recommends &&\
    apt-get install wget -y  --no-install-recommends &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install jupyter

RUN useradd -ms /bin/bash ubuntu &&\
    usermod -aG sudo ubuntu &&\
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER ubuntu

WORKDIR /home/ubuntu

RUN pip install optimum-habana\
    pip install git+https://github.com/HabanaAI/DeepSpeed.git@1.11.0

RUN git clone https://github.com/HabanaAI/Model-References
RUN git clone https://github.com/HabanaAI/Gaudi-tutorials
