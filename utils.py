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
