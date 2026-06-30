import json

def convert_to_gliner_data(path):
    prepared_data = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    for l in lines:
        line = json.loads(l)
        splitted_text = line['text'].split(" ")
        ner = [None] * len(splitted_text)

        for ent in line['entities']:
            start_char = ent['start']
            end_char = ent['end']
            label = ent['label']

            start_token_idx = None
            end_token_idx = None
            
            char_position = 0
            for i, token in enumerate(splitted_text):
                token_start = line['text'].find(token, char_position)
                token_end = token_start + len(token)
                char_position = token_start + len(token) + 1
                
                if token_start >= start_char and token_end <= end_char:
                    if start_token_idx is None:
                        start_token_idx = i
                    end_token_idx = i
                elif token_start < end_char and token_end > start_char:
                    if start_token_idx is None:
                        start_token_idx = i
                    end_token_idx = i
                elif token_start >= end_char:
                    break
            
            if start_token_idx is not None and end_token_idx is not None:
                for i in range(start_token_idx, end_token_idx + 1):
                    ner[i] = label
        
        ner_formatted = []
        i = 0
        while i < len(ner):
            if ner[i] is not None:
                start = i
                label = ner[i]
                while i < len(ner) and ner[i] == label:
                    i += 1
                end = i - 1
                ner_formatted.append([start, end, label])
            else:
                i += 1
        
        prepared_data.append({
            "tokenized_text": splitted_text,
            "ner": ner_formatted
        })
    
    return prepared_data


if __name__ == "__main__":
    convert_to_gliner_data("data/processed/train.jsonl")