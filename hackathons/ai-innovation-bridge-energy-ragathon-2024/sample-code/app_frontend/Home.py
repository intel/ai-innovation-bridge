import streamlit as st
from PIL import Image


st.title('Support Bot Prototype')
image = Image.open('./assets/chat.png')
st.image(image, width=500)
st.header('Simple Prototype RAG-based Chatbot')
st.markdown("""
            Introducing our simple prototype RAG-based LLM Chatbot – an avant-garde approach to question and answer systems leveraging the power of retrieval augmented generation (RAG).

Key Features:

1. **Retrieval Augmented Generation (RAG)**: At the core of our prototype lies RAG, a sophisticated in-context learning mechanism. With RAG, each user prompt is enhanced using information fetched from a comprehensive database, granting the model the ability to access and utilize data not present during its training phase.

2. **Open-Source Integration**: Our chatbot seamlessly integrates with premier open-source components, including LangChain, PyTorch, and GPT4all, showcasing the flexibility and compatibility of current machine learning tools.

3. **Educational Utility**: This prototype primarily serves as an educational instrument. It offers a transparent view into the intricacies and workflow of RAG-based systems. It's important to note that, in its current form, it's intended for learning and experimentation purposes and not designed for production deployment.

4. **Simplified Q&A Interaction**: Our chatbot provides a straightforward Q&A interface without the complexities of conversational memory. Users can pose questions, and the chatbot, using its RAG capabilities, fetches and generates pertinent responses.

5. **Commitment to Open-Source**: In line with the open-source spirit, our chatbot relies heavily on publicly available models and datasets, making it an ideal tool for educators, researchers, and enthusiasts wanting to dive deep into RAG and LLM-based systems.

In summary, this prototype showcases the potential and operation of RAG-based systems in a simple, user-friendly chatbot. Whether you're an AI enthusiast or a seasoned researcher, this tool provides valuable insights into the future of augmented conversational systems.
            """)

st.divider()
   
st.markdown('##### Notices & Disclaimers')
st.caption('Performance varies by use, configuration, and other factors. Learn more on the Performance \
    Index site. Performance results are based on testing as of dates shown in configurations and may not\
        reflect all publicly available updates. See backup for configuration details. No product or component\
            can be absolutely secure. Your costs and results may vary. Intel technologies may require enabled\
                hardware, software, or service activation. © Intel Corporation. Intel, the Intel logo, and other\
                    Intel marks are trademarks of Intel Corporation or its subsidiaries. Other names and brands may\
                        be claimed as the property of others.')
   