import json
import os
import re
from collections import defaultdict

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
    labels = ["PERSON", "EMAIL", "PHONE_NUMBER", "ADDRESS"]
    class_metrics = {cls: {"prec": [], "rec": [], "f1": []} for cls in labels}

    with open(os.path.join("data/processed", "train.jsonl"), "r", encoding="utf-8") as f:
        lines = f.readlines()
        for l in lines:
            line = json.loads(l)
            predicted_entities = find_pii(line['text'])

            true_by_class = defaultdict(list)
            for ent in line['entities']:
                if ent['label'] in labels:
                    true_by_class[ent['label']].append(ent)

            pred_by_class = defaultdict(list)
            for ent in predicted_entities:
                if ent['label'] in labels:
                    pred_by_class[ent['label']].append(ent)

            for cls in labels:
                class_metrics[cls]["prec"].append(precision(pred_by_class[cls], true_by_class[cls]))
                class_metrics[cls]["rec"].append(recall(pred_by_class[cls], true_by_class[cls]))
                class_metrics[cls]["f1"].append(f1_score(pred_by_class[cls], true_by_class[cls]))

        macro_prec = []
        macro_rec = []
        macro_f1 = []

        for cls in labels:
            p = sum(class_metrics[cls]["prec"]) / len(class_metrics[cls]["prec"])
            r = sum(class_metrics[cls]["rec"]) / len(class_metrics[cls]["rec"])
            f = sum(class_metrics[cls]["f1"]) / len(class_metrics[cls]["f1"])

            print(f"{cls:<15} {p:<10.4f} {r:<10.4f} {f:<10.4f}")

            macro_prec.append(p)
            macro_rec.append(r)
            macro_f1.append(f)

        macro_precision = sum(macro_prec) / len(macro_prec)
        macro_recall = sum(macro_rec) / len(macro_rec)
        macro_f1 = sum(macro_f1) / len(macro_f1)

        print("-" * 60)
        print(f"{'Макро среднее':<15} {macro_precision:<10.4f} {macro_recall:<10.4f} {macro_f1:<10.4f}")