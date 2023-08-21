import streamlit as st
from PIL import Image


st.title('How its made with...')
image = Image.open('./assets/intel-logo.png')
st.image(image, width=500)
st.header('Pharmaceutical Product Lifecycle Solution')
st.markdown('This “How its made with Intel” comprises four distinct product \
    lifecycle components that have been re-imagined – transforming them from \
        legacy to machine learning solutions powered by Intel hardware and software \
            components. The enabling technology stack includes components from across \
                Intel’s software and hardware portfolio with careful adaptions to enable\
                    this Pharmaceutical specific use case.')

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
   st.subheader("Medication Demand Forecaster")
   forecasting_image = Image.open('./assets/forecasting.png')
   st.image(forecasting_image)
   st.caption('Machine learning for demand forecasting to pick locations and amounts for shipping')
   
with col2:
   st.subheader("Pill Visual Quality Control")
   forecasting_image = Image.open('./assets/qaqc.png')
   st.image(forecasting_image)
   st.caption('Machine learning for predictive maintenance to prevent damage to manufacturing equipment')
   
with col3:
   st.subheader("Production Line Robotics Maintenance")
   forecasting_image = Image.open('./assets/robot_arm.png')
   st.image(forecasting_image)
   st.caption('Computer vision quality inspection tool to flag and remove bad pills from production line')
   
with col4:
   st.subheader('Robot Maintenance SupportBot')
   forecasting_image = Image.open('./assets/chat.png')
   st.image(forecasting_image)
   st.caption('Customer support chatbot based on fine-tuned gpt-j large language model')

st.divider()
   
st.markdown('##### Notices & Disclaimers')
st.caption('Performance varies by use, configuration, and other factors. Learn more on the Performance \
    Index site. Performance results are based on testing as of dates shown in configurations and may not\
        reflect all publicly available updates. See backup for configuration details. No product or component\
            can be absolutely secure. Your costs and results may vary. Intel technologies may require enabled\
                hardware, software, or service activation. © Intel Corporation. Intel, the Intel logo, and other\
                    Intel marks are trademarks of Intel Corporation or its subsidiaries. Other names and brands may\
                        be claimed as the property of others.')
   