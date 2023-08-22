FROM public.ecr.aws/docker/library/python:3.10.12

# copy assets over to image
COPY /src /medication_qaqc

# set the working directory
WORKDIR /medication_qaqc

# install dependancies
RUN apt-get update && apt-get install -y \
ffmpeg \
libsm6 \
libxext6 

# install dependancies
RUN pip3 install --user --no-cache-dir -r requirements.txt

# set PATH
ENV PATH=/root/.local/bin:$PATH

# exposing endpoint port
EXPOSE 5002

ENTRYPOINT ["python", "serve.py"]