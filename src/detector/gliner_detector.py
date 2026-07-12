import torch
from gliner import GLiNER

_model = None

def gliner_predict(text, labels):
    global _model

    if _model is None:
        _model = GLiNER.from_pretrained("models/gliner_pii")
        if torch.cuda.is_available():
            _model = _model.to("cuda")

    entities = _model.predict_entities(text, labels, threshold=0.7)
    
    predicted_entities = []
    for ent in entities:
        predicted_entities.append({
            'start': ent['start'],
            'end': ent['end'],
            'text': ent['text'],
            'label': ent['label'],
            'score': ent['score']
        })
    
    predicted_entities = sorted(predicted_entities, key=lambda x: x['start'], reverse=True)
    
    return predicted_entities
