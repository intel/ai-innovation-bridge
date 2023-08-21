import streamlit as st
from PIL import Image
import requests

st.title('Medication Demand Forecaster')

app_tab, help_tab = st.tabs(["Application", "Help"])

with app_tab:

    col11, col22= st.columns(2)

    with col11:
        image = Image.open('./assets/forecasting.png')
        st.image(image)
    with col22:
        st.markdown("##### ")

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
    st.markdown("#### Input Descriptions:")
    st.markdown("- Manufacturer: Provide the name of the manufacturer of the robotic arm")
    st.markdown("- Model: Specify the model or specific type of the robotic arm. ")
    st.markdown("- Lubrication Type: Indicate the type of lubrication used in the robotic arm.")
    st.markdown("- Pill Type: Specify the type or category that the robotic arm is assigned to")
    st.markdown("- Age of the Machine: Enter the age or duration of use of the robotic arm.")
    st.markdown("- Motor Current: Provide the current reading from the motor of the robotic arm. ")
    st.markdown("- Temperature of Sensors: Specify the temperature readings from the sensors installed on the robotic arm.")
    st.markdown("- Number of Historic Repairs: Enter the total number of repairs or maintenance activities performed on the robotic arm in the past. ")
    st.markdown("- Last Maintenance Date: Provide the date of the last maintenance activity performed on the robotic arm.")
    st.markdown("#### Code Samples:")
    
    st.markdown("##### Conversion of XGBoost to Daal4py Model")
    daalxgboost_code = '''xgb_model = xgb.train(self.parameters, xgb_train, num_boost_round=100)
        self.d4p_model = d4p.get_gbt_model_from_xgboost(xgb_model)'''
    st.code(daalxgboost_code, language='python')
    
    st.markdown("##### Inference with Daal4py Model")
    daalxgboost_code = '''
    daal_predict_algo = d4p.gbt_classification_prediction(
            nClasses=num_class,
            resultsToEvaluate="computeClassLabels",
            fptype='float')
            
    daal_prediction = daal_predict_algo.compute(data, daal_model)
    '''
    st.code(daalxgboost_code, language='python')
    
    st.markdown('[Visit GitHub Repository for Source Code](https://github.com/intel/AI-Hackathon)')
    
    
    
    
