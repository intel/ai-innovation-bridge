import streamlit as st
from PIL import Image
import requests
import matplotlib.pyplot as plt
import os
import io

st.title('Pill Visual Quality Control')

vino_tab, ipex_tab, help_tab = st.tabs(["OpenVINO Anomalib", "Intel Extension for PyTorch", "Help"])

with vino_tab:

    col11, col22= st.columns(2)

    with col11:
        image = Image.open('./assets/qaqc.png')
        st.image(image)
    with col22:
        st.markdown("##### The visual anomaly detection component uses a binary classification computer vision model based on VGG-16 or Padim to produce a flag if the product passes or fails visual inspection.  It leverages the OpenVINO, Anomalib, Intel® Extension for PyTorch*, and  Hugging Face Transformers on Intel® 4th Generation Xeon® Scalable processors OR Intel ARC GPUs. ")

    st.divider()
    
    st.markdown('#### Anomalib Model Training with PyTorch Lightning')

    data_path = st.text_input('Path to Pill Data Folder', value='./store/datasets/medication_qaqc/')
    modeldir = st.text_input('Path to Save Model', value='./store/models/medication_qaqc/')
    model = st.text_input('Foundation Model Options', value = "resnet18", help = "Use resnet18 to get started, review Anomalib docs more.")
    batch_size = st.number_input('Batch Size', value= 32, min_value=8,max_value=512)
    n_threads = st.number_input('Threads', value = 4, min_value=1,max_value=96)
    img_size = st.number_input('Image Size', value=256, min_value=16)
    layers = st.multiselect('Neural Network Layers', options = ["layer1", "layer2", "layer3"])
    
    if st.button('Train Model', key='vino training'):
        # build request

        URL = 'http://medication_qaqc:5002/train-openvino'
        DATA = {"data_path":data_path,"modeldir":modeldir,"model":model, 
                "batch_size": batch_size, "n_threads": n_threads, "img_size":img_size, "layers":layers}
        TRAINING_RESPONSE = requests.post(url = URL, json = DATA)

        if len(TRAINING_RESPONSE.text) < 40:       
            st.error("Model Training Failed")
            st.info(TRAINING_RESPONSE.text)
        else:
            st.success('Training was Succesful')
            st.info('Validation AUROC Score: ' + str(TRAINING_RESPONSE.json().get('Validation Results')))
               
    st.divider()
    
    st.markdown('#### Anomalib Inference with OpenVINO')
    
    openvino_model_path: str=None
    metadata_path: str=None
    image_path: str=None
    device: str = "CPU"
    
    openvino_model_path = st.text_input('OpenVINO model path', value='./store/models/medication_qaqc/weights/openvino/model.bin')
    metadata_path = st.text_input('OpenVINO metadata', value='./store/models/medication_qaqc/weights/openvino/metadata.json')
    image_path = st.text_input('Path to Target Image', value='./store/datasets/medication_qaqc/data/test/bad/012.png')
    device = st.text_input('Target Device', value= 'CPU')
    
    if st.button('Start Inference', key='openvino inference'):
        
        # build request
        URL = 'http://medication_qaqc:5002/predict-openvino'
        DATA = {"openvino_model_path":openvino_model_path,"metadata_path":metadata_path,
                "image_path":image_path, "device":device}
        INFERENCE_RESPONSE = requests.post(url = URL, json = DATA)

        if len(INFERENCE_RESPONSE.text) < 40:       
            st.error("Inference Failed")
            st.info(INFERENCE_RESPONSE.text)
        else:
            st.success('Inference was Succesful')
            classified_pills = INFERENCE_RESPONSE.content
            st.image(classified_pills, width=800)  
           
# Start of Intel Extension for PyTorch Implementation

with ipex_tab:

    col11, col22= st.columns(2)

    with col11:
        image = Image.open('./assets/qaqc.png')
        st.image(image)
    with col22:
        st.markdown("##### The visual anomaly detection component uses a binary classification computer vision model based on VGG-16 or Padim to produce a flag if the product passes or fails visual inspection.  It leverages the OpenVINO, Anomalib, Intel® Extension for PyTorch*, and  Hugging Face Transformers on Intel® 4th Generation Xeon® Scalable processors OR Intel ARC GPUs. ")


    st.divider()
    
    st.markdown('#### Visual QA/QC Model Training')

    data_folder = st.text_input('Root Training Data Folder', value='./store/datasets/medication_qaqc/data/')
    model_path = st.text_input('Save Model Path', value='./store/models/medication_qaqc/model_ipex.h5')
    neg_class = st.number_input('Passing Quality Label',min_value=0,max_value=100)
    learning_rate = st.slider('Learning Rate',min_value=0.0001, max_value=0.05, step=.0001, value=.025, format='%f')
    epochs = st.number_input('Epochs',min_value=1, max_value=100, step=1, value=5 )
    data_aug = st.checkbox('Augment Training Data')
    
    if st.button('Train Model', key='ipex training'):
        # build request

        URL = 'http://medication_qaqc:5002/train-ipex'
        DATA = {"data_folder":data_folder,"neg_class":neg_class,"modeldir":model_path, 
                "learning_rate": learning_rate, "epochs": epochs, "data_aug":data_aug}
        TRAINING_RESPONSE = requests.post(url = URL, json = DATA)

        if len(TRAINING_RESPONSE.text) < 40:       
            st.error("Model Training Failed")
            st.info(TRAINING_RESPONSE.text)
        else:
            st.success('Training was Succesful')
            st.info('Trained Model Location: ' + str(TRAINING_RESPONSE.json().get('Model Location')))
            
    st.divider()
    
    st.markdown('#### Intel Extension for PyTorch Inference')
    
    data_folder = st.text_input('Root Store', value='./store/datasets/medication_qaqc/data/')
    trained_model_path = st.text_input('Trained Model Path', value='./store/models/medication_qaqc/model_ipex.h5')
    batch_size = st.number_input('Inference Batch Size',min_value=5,max_value=100)
    
    if st.button('Start Batch Evaluation', key='ipex inference'):
        
        # build request
        URL = 'http://medication_qaqc:5002/predict-ipex'
        DATA = {"trained_model_path":trained_model_path,"data_folder":data_folder,"batch_size":batch_size}
        INFERENCE_RESPONSE = requests.post(url = URL, json = DATA)

        if len(INFERENCE_RESPONSE.text) < 40:       
            st.error("Inference Failed")
            st.info(INFERENCE_RESPONSE.text)
        else:
            st.success('Inference was Succesful')
            classified_pills = INFERENCE_RESPONSE.json().get('Prediction Output')
            
            with st.expander("Pill Classifications"):
                for label, file in classified_pills:
                    if label == 1.0:
                        st.markdown('### Faulty Pill')
                        st.text(os.path.join(data_folder,'blind/',file))
                        image = Image.open(os.path.join(data_folder,'blind/',file))
                        st.image(image, width=800)
                    else:
                        st.markdown('### Valid Pill')
                        st.text(os.path.join(data_folder,'blind/',file))
                        image = Image.open(os.path.join(data_folder,'blind/',file))
                        st.image(image, width=800)
                    
            
            
    
with help_tab:
    st.markdown("#### Coming Soon!")