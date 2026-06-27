def calculate_tp_fp_fn(predict, true):
    tp = 0
    matched_true = set()
    matched_pred = set()

    for i, pred in enumerate(predict):
        for j, gt in enumerate(true):
            if j in matched_true:
                continue
            if pred["start"] == gt["start"] and pred["end"] == gt["end"] and pred["label"] == gt["label"]:
                tp += 1
                matched_true.add(j)
                matched_pred.add(i)
                break

    fp = len(predict) - len(matched_pred)
    fn = len(true) - len(matched_true)

    return tp, fp, fn

def precision(predict, true):
    tp, fp, fn = calculate_tp_fp_fn(predict, true)
    return tp / (tp + fp) if (tp + fp) > 0 else 0

def recall(predict, true):
    tp, fp, fn = calculate_tp_fp_fn(predict, true)
    return tp / (tp + fn) if (tp + fn) > 0 else 0

def f1_score(predict, true):
    p = precision(predict, true)
    r = recall(predict, true)
    return 2 * (p * r) / (p + r) if (p + r) > 0 else 0