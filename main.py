import streamlit as st
import random
import time
from model import Model, inference
from utils import format_text, show_table
import json

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
        #print("TEXTo", texto)
        model = Model()
        pipe = model.call_model_general()
        pipe_dates = model.call_model_dates()
        entities = inference(pipe, texto)
        dates = inference(pipe_dates, texto)
        print("DATES", dates)
        #print("inference entities", entities)
        sentence = format_text(texto, entities, dates)
        html_table = show_table(entities, dates)

        if sentence:
            st.markdown(sentence, unsafe_allow_html=True)

            st.markdown(html_table, unsafe_allow_html=True)

            st.markdown("""
                ### Leyenda de colores:
                - <span style='color:blue;'>🟦 Persona (PER)</span><br>
                - <span style='color:green;'>🟩 Organización (ORG)</span><br>
                - <span style='color:purple;'>🟪 Lugar (LOC)</span><br>
                - <span style='color:red;'>🟥 Misceláneo (MISC)</span>
                - <span style='color:yellow;'>🟥 Fechas (DATE)</span>
                """, unsafe_allow_html=True)

        #print(entities)

    else:
        st.error("Introduce algun texto 🚨")