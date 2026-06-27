import json
import os
import re

from src.monitoring import recall, precision, f1_score

def find_emails(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return [{"start": m.start(), "end": m.end(), "label": "EMAIL"} for m in re.finditer(email_pattern, text)]

def find_phone_numbers(text):
    phone_number_pattern = r'(?:\+7|8|7)[\s\-\(\)]*(\d{3})[\s\-\(\)]*(\d{3})[\s\-\(\)]*(\d{2})[\s\-\(\)]*(\d{2})'
    return [{"start": m.start(), "end": m.end(), "label": "PHONE_NUMBER"} for m in re.finditer(phone_number_pattern, text)]

def find_pii(text):
    result = []

    [result.append(el) for el in find_emails(text)] 
    [result.append(el) for el in find_phone_numbers(text)]

    result.sort(key=lambda x: x["start"])
    
    return result

if __name__ == "__main__":
    precision_a = []
    recall_a = []
    f1_score_a = []

    with open(os.path.join("data/processed", "train.jsonl"), "r", encoding="utf-8") as f:
        lines = f.readlines()
        for l in lines:
            line = json.loads(l)
            predict = find_pii(line['text'])

            precision_a.append(precision(predict, line["entities"]))
            recall_a.append(recall(predict, line["entities"]))
            f1_score_a.append(f1_score(predict, line["entities"]))

    print(f"PRECISION: {sum(precision_a)/len(precision_a)}")
    print(f"RECALL: {sum(recall_a)/len(recall_a)}")
    print(f"F1_SCORE: {sum(f1_score_a)/len(f1_score_a)}")
