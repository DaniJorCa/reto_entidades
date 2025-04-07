class Model:
    def __init__(self):
        self.model = "pabloOmega/text-entities-detection"
        self.task= "object-detection"
    
    def call_model(self):
        from transformers import pipeline

        pipe = pipeline(self.task, self.model)

        return pipe
    
