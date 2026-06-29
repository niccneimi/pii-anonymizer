from gliner import GLiNER
import json
import os
from tqdm import tqdm
from collections import defaultdict

from src.monitoring import recall, precision, f1_score

model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

if __name__ == "__main__":

    labels = ["PERSON", "EMAIL", "PHONE_NUMBER", "ADDRESS"]
    class_metrics = {cls: {"prec": [], "rec": [], "f1": []} for cls in labels}

    with open(os.path.join("data/processed", "train.jsonl"), "r", encoding="utf-8") as f:
        lines = f.readlines()
        for l in tqdm(lines):
            predicted_entities = []
            line = json.loads(l)
            entities = model.predict_entities(line['text'], labels, threshold=0.4)
            for ent in entities:
                predicted_entities.append({'start': ent['start'], 'end': ent['end'], 'label' : ent['label']})

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