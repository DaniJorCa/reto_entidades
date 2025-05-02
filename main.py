import streamlit as st
import streamlit.components.v1 as components

import random
import time
from model import Model, inference
from utils import format_text, show_table, check_length, load_text
import json

st.title("Extracción de entidades")

with st.sidebar:

    opcion = st.selectbox(
    "Selecciona un modelo:",
    ["Español", "Inglés", "Ambos"]
    )

    # Cargar archivo
    archivo = st.file_uploader("Sube un archivo de texto", type=["txt"])

    frase = st.text_input(
        "Introduce tu texto para extraer las entidades 👇",
    )

    if archivo:
        texto = load_text(archivo)
        st.text_area("Contenido del archivo:", value=texto, height=300)
    elif frase:
        texto = frase
    else:
        texto = None
        
    submit = st.button("Extraer Entidades")

if submit and opcion:
    if texto:
        # Comprobamos que el texto tiene menos de 512 caracteres
        is_not_too_large = check_length(texto)

        if is_not_too_large:
            print("Texto introducido:", texto)

            model = Model()

            entities_general = []
            entities_multi = []
            
            # Llamar al modelo general
            if opcion == 'Español' or opcion == 'Ambos':
                pipe_general = model.call_model_general()
                entities_general = inference(pipe_general, texto)

            # Llamar al modelo de fechas
            pipe_dates = model.call_model_dates()
            entities_dates = inference(pipe_dates, texto)

            # Llamar al modelo multilingual
            if opcion == 'Inglés' or opcion == 'Ambos':
                pipe_multi = model.call_model_multilinguage()
                entities_multi =inference(pipe_multi, texto)

            # Normalizar: asegurarnos de que todos tienen 'entity_group'
            for entity in entities_general + entities_dates + entities_multi:
                if "entity_group" not in entity:
                    entity["entity_group"] = entity["entity"]  # Copiar 'entity' en 'entity_group'


            # Combinar entidades de ambos modelos
            all_entities = entities_general + entities_dates + entities_multi
            print("Todas las entidades combinadas:", all_entities)

            # Formatear el texto con todas las entidades
            sentence = format_text(texto, all_entities)

            # Mostrar tabla con todas las entidades
            html_table = show_table(all_entities)

            if sentence:
                st.markdown(sentence, unsafe_allow_html=True)

                components.html(html_table, height=400, scrolling=True)

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
            st.error("El texto tiene mas de 512 caracteres. Por favor intruduce un texto mas pequeño.")
    else:
        st.error("Introduce algun texto 🚨")