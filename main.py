import streamlit as st
import random
import time
from model import Model, inference
from utils import format_text, show_table
import json

st.title("Extracción de entidades")

with st.sidebar:
    # Cargar archivo
    archivo = st.file_uploader("Sube un archivo de texto", type=["txt"])

    texto = st.text_input(
        "Introduce tu texto para extraer las entidades 👇",
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
        print("Texto introducido:", texto)

        model = Model()
        
        # Llamar al modelo general
        pipe_general = model.call_model_general()
        entities_general = inference(pipe_general, texto)
        print("Entidades modelo general:", entities_general)

        # Llamar al modelo de fechas
        pipe_dates = model.call_model_dates()
        entities_dates = inference(pipe_dates, texto)
        print("Entidades modelo fechas:", entities_dates)

        # Normalizar: asegurarnos de que todos tienen 'entity_group'
        for entity in entities_general + entities_dates:
            if "entity_group" not in entity:
                entity["entity_group"] = entity["entity"]  # Copiar 'entity' en 'entity_group'


        # Combinar entidades de ambos modelos
        all_entities = entities_general + entities_dates
        print("Todas las entidades combinadas:", all_entities)

        # Formatear el texto con todas las entidades
        sentence = format_text(texto, all_entities)

        # Mostrar tabla con todas las entidades
        html_table = show_table(all_entities)

        if sentence:
            st.markdown(sentence, unsafe_allow_html=True)

            st.markdown(html_table, unsafe_allow_html=True)

            st.markdown("""
                ### Leyenda de colores:
                - <span style='color:blue;'>🟦 Persona (PER)</span><br>
                - <span style='color:green;'>🟩 Organización (ORG)</span><br>
                - <span style='color:purple;'>🟪 Lugar (LOC)</span><br>
                - <span style='color:red;'>🟥 Misceláneo (MISC)</span><br>
                - <span style='color:yellow;'>🟨 Fecha (DATE)</span>
                """, unsafe_allow_html=True)

        print("Entidades finales mostradas en la app:", all_entities)

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
