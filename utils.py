import re
import os
import math
import tiktoken
from model import Model


def extract_entities(entities):
    lista_posiciones = []
    lista_palabras = []
    diccionario_palabras = {}

    # Encontrar posiciones donde comienza una nueva entidad
    for i, entitie in enumerate(entities):
        if entitie['entity'].split("-")[0] == 'B':
            lista_posiciones.append(i)

    for i, posicion in enumerate(lista_posiciones):
        # Determinar hasta dónde va esta entidad
        hasta = lista_posiciones[i + 1] if i < len(lista_posiciones) - 1 else len(entities)
        lista_entities = entities[posicion:hasta]

        # Si por alguna razón no hay elementos, skip
        if not lista_entities:
            continue

        # Obtener tipo y palabra completa
        type_entity = lista_entities[0]['entity']
        word = " ".join([ent['word'].replace('[UKN]', '').replace('#', '') for ent in lista_entities]).strip()

        diccionario = {'word': word, 'type': type_entity}
        lista_palabras.append(diccionario)

    diccionario_palabras["palabras"] = lista_palabras

    return diccionario_palabras



def format_text(texto, lista_entities):
    texto_formateado = texto
    palabras_descartadas = []

    for dic in lista_entities:
        entidad = dic["word"]
        tipo = dic["entity_group"]

        color = {
            'ORG': 'green',
            'PER': 'blue',
            'LOC': 'purple',
            'MISC': 'red',
            'DATE': 'yellow'
        }.get(tipo, 'black')  # Color por defecto negro

        # Construir el HTML
        entidad_html = f"<span style='color:{color}'>{entidad}</span>"

        # Escapamos la entidad para que no se interprete mal en la regex
        pattern = r'\b' + re.escape(entidad) + r'(?:\b|(?=[.,]))'


        # Verificamos si hay coincidencia antes de reemplazar
        if re.search(pattern, texto_formateado):
            # Hay coincidencia, hacemos el reemplazo
            texto_formateado = re.sub(pattern, entidad_html, texto_formateado)
        else:
            palabras_descartadas.append(entidad)

    os.environ['descartadas'] = ','.join(palabras_descartadas)
    print("PALABRAS DESCARTADAS", os.environ['descartadas'])

    return texto_formateado

def show_table(entities):
    PER = ""
    ORG = ""
    MISC = ""
    LOC = ""
    DATE = ""

    for entity in entities:
        entity_group = entity['entity_group']
        word = entity['word']
        palabras_descartadas = os.environ['descartadas'].split(",")

        if ('[UNK]' not in word) and ("##" not in word) and word not in palabras_descartadas:

            tag_html = f'<li>{word}</li>'

            if entity_group == 'MISC':
                MISC += tag_html
            elif entity_group == 'PER':
                PER += tag_html
            elif entity_group == 'LOC':
                LOC += tag_html
            elif entity_group == 'ORG':
                ORG += tag_html
            elif entity_group == 'DATE':
                DATE += tag_html

    html_table = f"""
        <style>
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 14px;
        }}
        th, td {{
            padding: 10px 14px;
            border: 1px solid #ccc;
            text-align: left;
        }}
        th {{
            font-weight: bold;
            background-color: #f2f2f2;
        }}
        ul {{
            padding-left: 18px;
            margin: 0;
        }}
    </style>
        <table>
            <thead>
                <tr>
                    <th>Entidad</th>
                    <th>Palabras</th>
                </tr>
            </thead>
            <tbody>        
    """


    items = {"PERSONA": PER, "ORGANIZACIÓN":ORG, "MISCELANEA":MISC, "LOCALIZACIÓN": LOC, "FECHA": DATE}

    for key, value in items.items():
        if value != "":
            html_table += f"""<tr>
                                <td>{key}</td>
                                <td><ul>{value}</ul></td>
                            </tr>"""
            
    html_table += "</tbody></table>"

    return html_table

def check_length(texto: str) -> bool:
    model = Model()
    pipe_general = model.call_model_general()
    tokenizer = pipe_general.tokenizer

    tokens = tokenizer.tokenize(texto)
    return len(tokens) < 512

def load_text(file):
    # Leer el contenido del archivo como texto
    texto = file.read().decode("utf-8")
    return texto