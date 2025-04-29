import re
import math

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
        word = " ".join([ent['word'] for ent in lista_entities]).strip()

        diccionario = {'word': word, 'type': type_entity}
        lista_palabras.append(diccionario)

    diccionario_palabras["palabras"] = lista_palabras

    return diccionario_palabras



def format_text(texto, lista_entities):
    texto_formateado = texto

    for dic in lista_entities:
        entidad = dic["word"]
        tipo = dic["entity_group"]

        color = {
            'ORG': 'green',
            'PER': 'blue',
            'LOC': 'purple',
            'MISC': 'red',
            'DATE': 'yellow'  # Asegúrate de que 'DATE' esté aquí
        }.get(tipo, 'black')  # Color por defecto negro

        # Construir el HTML
        entidad_html = f"<span style='color:{color}'>{entidad}</span>"

        # Escapamos la entidad para que no se interprete mal en la regex
        pattern = re.escape(entidad)

        # Reemplazo en el texto original
        texto_formateado = re.sub(pattern, entidad_html, texto_formateado)
    
    # for date in dates:
    #     date_extract = date["word"]
    #     tipo = date["entity_group"]

    #     color = {
    #         'DATE': 'yellow',
    #     }.get(tipo, 'black')

    #     # Construir el HTML
    #     entidad_html = f"<span style='color:{color}'>{date_extract}</span>"

    #     # Escapamos la entidad para que no se interprete mal en la regex
    #     pattern = re.escape(date_extract)

    #     # Reemplazo en el texto original
    #     texto_formateado = re.sub(pattern, entidad_html, texto_formateado)


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

        




