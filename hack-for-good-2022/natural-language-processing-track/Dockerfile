FROM vault.habana.ai/gaudi-docker/1.7.0/ubuntu20.04/habanalabs/pytorch-installer-1.12.0:latest as habanahack

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y --no-install-recommends &&\
    apt-get install htop=2.2.0-2build1 -y  --no-install-recommends &&\
    apt-get install sudo=1.8.31-1ubuntu1.2 -y  --no-install-recommends &&\
    apt-get install wget=1.20.3-1ubuntu2 -y  --no-install-recommends &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash ubuntu &&\
    usermod -aG sudo ubuntu &&\
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER ubuntu
RUN python3 -m pip install --upgrade --no-cache-dir pip==22.3.1 

#installing conda - not currently used
#ENV PATH=/opt/conda/bin:$PATH
#RUN sudo wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
#    sudo /bin/bash ~/miniconda.sh -b -p /opt/conda &&\
#    conda create --name nlphackathon python=3.8 && \
#    source activate nlphackathon

WORKDIR /home/ubuntu/nlp-hackathon

COPY . /home/ubuntu/nlp-hackathon/

RUN echo "export OS=ubuntu20.04" >> ~/.bashrc && \
    echo "export PT_VERSION=1.12.0" >> ~/.bashrc && \
    echo "export PATH=/home/ubuntu/.local/bin:/home/ubuntu/nlp-hackathon/start_jupyter_scripts:$PATH" >> ~/.bashrc && \
    source ~/.bashrc && \
    pip3 install -r /home/ubuntu/nlp-hackathon/requirements.txt --no-cache-dir

FROM habanahack as habanahack8080
USER ubuntu
ENV HABANA_VISIBLE_DEVICES 0
ENV OMPI_MCA_btl_vader_single_copy_mechanism none
CMD ["bash","/home/ubuntu/nlp-hackathon/start_jupyter_scripts/start-jupyter8080.sh"]

FROM habanahack as habanahack8081
USER ubuntu
ENV HABANA_VISIBLE_DEVICES 1
ENV OMPI_MCA_btl_vader_single_copy_mechanism none
CMD ["bash","/home/ubuntu/nlp-hackathon/start_jupyter_scripts/start-jupyter8081.sh"]

FROM habanahack as habanahack8082
USER ubuntu
ENV HABANA_VISIBLE_DEVICES 2
ENV OMPI_MCA_btl_vader_single_copy_mechanism none
CMD ["bash","/home/ubuntu/nlp-hackathon/start_jupyter_scripts/start-jupyter8082.sh"]

FROM habanahack as habanahack8083
USER ubuntu
ENV HABANA_VISIBLE_DEVICES 3
ENV OMPI_MCA_btl_vader_single_copy_mechanism none
CMD ["bash","/home/ubuntu/nlp-hackathon/start_jupyter_scripts/start-jupyter8083.sh"]

FROM habanahack as habanahack8084
USER ubuntu
ENV HABANA_VISIBLE_DEVICES 4
ENV OMPI_MCA_btl_vader_single_copy_mechanism none
CMD ["bash","/home/ubuntu/nlp-hackathon/start_jupyter_scripts/start-jupyter8084.sh"]

FROM habanahack as habanahack8085
USER ubuntu
ENV HABANA_VISIBLE_DEVICES 5
ENV OMPI_MCA_btl_vader_single_copy_mechanism none
CMD ["bash","/home/ubuntu/nlp-hackathon/start_jupyter_scripts/start-jupyter8085.sh"]

FROM habanahack as habanahack8086
USER ubuntu
ENV HABANA_VISIBLE_DEVICES 6
ENV OMPI_MCA_btl_vader_single_copy_mechanism none
CMD ["bash","/home/ubuntu/nlp-hackathon/start_jupyter_scripts/start-jupyter8086.sh"]

FROM habanahack as habanahack8087
USER ubuntu
ENV HABANA_VISIBLE_DEVICES 7
ENV OMPI_MCA_btl_vader_single_copy_mechanism none
CMD ["bash","/home/ubuntu/nlp-hackathon/start_jupyter_scripts/start-jupyter8087.sh"]

