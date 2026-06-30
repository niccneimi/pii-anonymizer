import json, os
from collections import defaultdict
from gliner import GLiNER
from tqdm import tqdm

from src.detector.gliner_detector import gliner_predict
from src.detector.regex_detector import find_pii
from src.monitoring import recall, precision, f1_score

model = GLiNER.from_pretrained("models/gliner_pii") 

def detect_pii(text, mode="ensemble"):
    if mode == "ensemble":
        gliner_entities = gliner_predict(model, text)
        regex_entities = find_pii(text)

        final_entities = []
        for ent in regex_entities:
            if ent["label"] in ["EMAIL", "PHONE_NUMBER"]:
                final_entities.append(ent)

        taken_spans = set()
        for ent in regex_entities:
            for i in range(ent["start"], ent["end"]):
                taken_spans.add(i)

        for ent in gliner_entities:
            if ent["label"] in ["PERSON", "ADDRESS"]:
                overlap = any(i in taken_spans for i in range(ent["start"], ent["end"]))
                if not overlap:
                    final_entities.append(ent)
                    for i in range(ent["start"], ent["end"]):
                        taken_spans.add(i)

        final_entities.sort(key=lambda x: x["start"], reverse=True)
        return final_entities
    elif mode == "use_regex_only":
        return find_pii(text)
    elif mode == "use_gliner_only":       
        return gliner_predict(model, text)

if __name__ == "__main__":
    labels = ["PERSON", "EMAIL", "PHONE_NUMBER", "ADDRESS"]
    class_metrics = {cls: {"prec": [], "rec": [], "f1": []} for cls in labels}

    with open(os.path.join("data/processed", "test.jsonl"), "r", encoding="utf-8") as f:
        lines = f.readlines()
        for l in tqdm(lines):
            line = json.loads(l)
            predicted_entities = detect_pii(line['text'], "use_regex_only")

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