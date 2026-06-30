def gliner_predict(model, text):
    predicted_entities = []
    labels = ["PERSON", "EMAIL", "PHONE_NUMBER", "ADDRESS"]

    entities = model.predict_entities(text, labels, threshold=0.7)

    for ent in entities:
        predicted_entities.append({'start': ent['start'], 'end': ent['end'], 'label' : ent['label']})

    predicted_entities = sorted(predicted_entities, key=lambda x: x['start'], reverse=True)
    return predicted_entities