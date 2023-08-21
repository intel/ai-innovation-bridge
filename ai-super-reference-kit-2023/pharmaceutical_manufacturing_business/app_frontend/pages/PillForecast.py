import streamlit as st
from PIL import Image
import requests

st.title('Medication Demand Forecasting')

app_tab, help_tab = st.tabs(["Application", "Help"])

with app_tab:

    col11, col22= st.columns(2)

    with col11:
        image = Image.open('./assets/forecasting.png')
        st.image(image)
    with col22:
        st.markdown("##### The demand forecasting component uses a time series prediction CNN-LSTM model to predict the demand for multiple products across multiple locations. It leverages the Intel® Extensions for TensorFlow on Intel® 4th Generation Xeon® Scalable processors.")

    st.divider()
    
    st.markdown('#### Demand Forecasting Model Training')
    
    data_file = st.text_input('Training Data File Path',key='data')
    window_size = st.number_input('Window', min_value=50, max_value=200, value=125,step=5)
    lag_size = st.slider('Lagging Window',min_value=5, max_value=50, value=25, step=5)
    epochs = st.number_input('Epochs',min_value=1, max_value=100, step=1, value=5 )
    batch_size = st.number_input('Batch Size',min_value=100, max_value=1000, step=1, value=512 )
    model_path = st.text_input('Model Save Path',key='model path')
    test_size = st.slider('Percentage of data saved for Testing',min_value=0.10, max_value=0.90, value=0.30, step=.05)
    
    
    if st.button('Train Model', key='training'):
        # build request

        URL = 'http://medication_demand_forecast:5001/train'
        DATA = {'filepath':data_file, 'window':window_size, 'lag_size':lag_size, 'test_size':test_size,
                'epochs':epochs, 'batch_size':batch_size, 'save_model_dir':model_path}
        TRAINING_RESPONSE = requests.post(url = URL, json = DATA)

        if len(TRAINING_RESPONSE.text) < 40:       
            st.error("Model Training Failed")
            st.info(TRAINING_RESPONSE.text)
        else:
            st.success('Training was Succesful')
            st.info('Model Validation Accuracy Score: ' + str(TRAINING_RESPONSE.json().get('validation scores')))

    
    st.divider()
    
    st.markdown('#### Predictive Maintenance Analysis')
    
    col21, col22, col23 = st.columns(3)

    # inference inputs
    selected_model_path = st.text_input('Selected Model Path', key='demand forecaster model')
    analysis_save_path = st.text_input('Forecast Demand Analysis Save Path')
    input_data = st.text_input('Input Data Path')
    inf_window_size = st.number_input('Window', min_value=50, max_value=200, value=125,step=5, key='demand forecaster window')
    inf_lag_size = st.slider('Lagging Window',min_value=5, max_value=50, value=25, step=5, key='demand forecaster lag window')
    inf_batch_size = st.number_input('Batch Size',min_value=100, max_value=1000, step=1, value=512, key='demand forecaster batch' )
    interations = st.number_input('Interations', min_value=50, max_value=200, value=100,step=5, key='demand forecaster iterations')
        
    

    if st.button('Run Demand Forecast Analysis', key='analysis'):
        URL = 'http://medication_demand_forecast:5001/predict'
        DATA = {'keras_saved_model_dir':selected_model_path, 'output_saved_dir':selected_model_path, 
                'input_file':input_data, 'results_save_dir':analysis_save_path, 
                'window':inf_window_size, 'lag_size':inf_lag_size, 'batch_size':inf_batch_size, 
                'num_iters':interations}
        INFERENCE_RESPONSE = requests.post(url = URL, json = DATA)

        if len(INFERENCE_RESPONSE.text) < 40:       
            st.error("Model Training Failed")
            st.info(INFERENCE_RESPONSE.text)
        else:
            st.success('Review your Results Here: ' + str(INFERENCE_RESPONSE.json().get('Result')))
            
# Help tab frontend below
    
with help_tab:
    st.markdown("#### Coming Soon!")

    
    
    
