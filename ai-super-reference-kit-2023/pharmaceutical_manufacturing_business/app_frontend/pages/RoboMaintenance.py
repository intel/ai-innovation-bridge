import streamlit as st
import requests
import os
from PIL import Image

st.title('Robotics Predictive Maintenance')

app_tab, help_tab = st.tabs(["Application", "Help"])

with app_tab:

    col11, col22= st.columns(2)

    with col11:
        image = Image.open('./assets/robot_arm.png')
        st.image(image)
    with col22:
        st.markdown("##### Introducing our cutting-edge predictive maintenance tool that harnesses the power of \
        Intel oneDAL tool on Xeon CPUs to accelerate XGBoost inference. By leveraging advanced acceleration \
            techniques, our tool enables accurate prediction of maintenance needs, helping you proactively \
                address issues before breakdowns occur, ensuring uninterrupted operations and optimized maintenance schedules.")

    st.divider()
    
    st.markdown('#### Predictive Maintenance Model Training')
    
    data_file = st.text_input('Training Data File Path',key='data')
    model_name = st.text_input('Model Name',key='model name', help='The name of the model without extensions')
    model_path = st.text_input('Model Save Path',key='model path', help='Provide the path without file name')
    test_size = st.slider('Percentage of data saved for Testing',min_value=5, max_value=50, value=25, step=5)
    
    
    if st.button('Train Model', key='training'):
        # build request

        URL = 'http://robot_maintenance:5003/train'
        DATA = {'file':data_file, 'model_name':model_name, 'model_path':model_path, 
                  'test_size': test_size, 'ncpu': 4}
        TRAINING_RESPONSE = requests.post(url = URL, json = DATA)

        if len(TRAINING_RESPONSE.text) < 40:       
            st.error("Model Training Failed")
            st.info(TRAINING_RESPONSE.text)
        else:
            st.success('Training was Succesful')
            st.info('Model Validation Accuracy Score: ' + str(TRAINING_RESPONSE.json().get('validation scores')))

    
    st.divider()
    
    st.markdown('#### Predictive Maintenance Analysis')
    
    selected_model_path = st.text_input('Selected Model Path',key='model path selection')

    col21, col22, col23 = st.columns(3)

    # default
    manufacturer_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    model_list = ['Gen1', 'Gen2', 'Gen3', 'Gen4']
    lubrication_type_list = ['LTA', 'LTB', 'LTC']
    product_assignment_list = ['PillA', 'PillB', 'PillC']

    with col21:
        manufacturer = st.selectbox('Manufacturer', manufacturer_list)
        generation = st.selectbox('Generation', model_list)
        age = st.number_input('Robot Age', min_value=0, max_value=25, step=1, value=0)

    with col22:
        temperature = st.number_input('Temperature', min_value=50, max_value=300, step=1)
        motor_current = st.number_input('Motor Current', min_value=0.00, max_value=10.00, step=.05, value=5.00)
        lubrication_type = st.selectbox('Lubrication Type', lubrication_type_list)
    with col23:
        last_maintenance = st.number_input('Last Maintenance', min_value=0, max_value=60, step=1)
        num_repairs = st.number_input('Repair Counts', min_value=0, max_value=50, step=1)
        product_assignment = st.selectbox('Pill Product Assignment', product_assignment_list)
        
        
    sample = [{'Age':age, 'Temperature':temperature, 'Last_Maintenance':last_maintenance, 'Motor_Current':motor_current,
       'Number_Repairs':num_repairs, 'Manufacturer':manufacturer, 
       'Generation':generation,'Lubrication':lubrication_type, 'Product_Assignment':product_assignment}]

    if st.button('Run Maintenance Analysis', key='analysis'):
        URL = 'http://robot_maintenance:5003/predict'
        DATA = {'sample':sample, 'model':selected_model_path, 'num_class':3}
        INFERENCE_RESPONSE = requests.post(url = URL, json = DATA)

        if len(INFERENCE_RESPONSE.text) < 40:       
            st.error("Model Training Failed")
            st.info(INFERENCE_RESPONSE.text)
        else:
            st.success(str(INFERENCE_RESPONSE.json().get('Maintenance Recommendation')))
            
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
    
    
    
    
