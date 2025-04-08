from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from utils import extract_entities

class Model:
    def __init__(self):
        self.model = None
        self.task = "ner"
        self.tokenizer= None
    
    def call_model_general(self):
        self.model = "mrm8488/bert-spanish-cased-finetuned-ner"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model, use_fast=False)
        model_hf = AutoModelForTokenClassification.from_pretrained(self.model)
        pipe = pipeline(self.task, model=model_hf, tokenizer=self.tokenizer, aggregation_strategy="simple")  
        
        return pipe

    
    def call_model_dates(self):
        from transformers import pipeline
        self.model = "agomez302/spanish-legal-dates-ner"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model)
        model_hf = AutoModelForTokenClassification.from_pretrained(self.model)
        pipe = pipeline(self.task, model = model_hf, tokenizer = self.tokenizer, aggregation_strategy="simple")

        return pipe
    


def inference(pipe, texto):
    entities = pipe(texto)
    #print("ENTITIES", entities)
    #palabras = extract_entities(entities)

    return entities

