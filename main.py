import streamlit as st
import random
import time
from model import Model, inference

st.title("Extracción de entidades")

st.caption("Note that this demo app isn't actually connected to any LLMs. Those are expensive;)")

with st.sidebar:
    # Cargar archivo
    archivo = st.file_uploader("Sube un archivo de texto", type=["txt"])

    texto = st.text_input(
            "Introduce tu texto para extraer las entidades 👇",
            #label_visibility=st.session_state.visibility,
            #disabled=st.session_state.disabled,
            #placeholder=st.session_state.placeholder,
        )

    if archivo is not None:
        # Leer el contenido del archivo como texto
        contenido = archivo.read().decode("utf-8")
        st.text_area("Contenido del archivo:", value=contenido, height=300)
    else:
        contenido = None

    submit = st.button("Extraer Entidades")


if submit:
    if archivo or contenido:
        pass
    elif (texto):
        print("TEXTo", texto)
        model = Model()
        pipe = model.call_model_general()
        print("MODEL", model)
        print('PIPE', pipe)
        entities = inference(pipe, texto)

        print(entities)



        
    else:
        st.error("Introduce algun texto 🚨")



# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = [{"role": "assistant", "content": "Let's start chatting! 👇"}]

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Accept user input
# if prompt := st.chat_input("What is up?"):
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Display assistant response in chat message container
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         full_response = ""
#         assistant_response = random.choice(
#             [
#                 "Hello there! How can I assist you today?",
#                 "Hi, human! Is there anything I can help you with?",
#                 "Do you need help?",
#             ]
#         )
#         # Simulate stream of response with milliseconds delay
#         for chunk in assistant_response.split():
#             full_response += chunk + " "
#             time.sleep(0.05)
#             # Add a blinking cursor to simulate typing
#             message_placeholder.markdown(full_response + "▌")
#         message_placeholder.markdown(full_response)
#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": full_response})
