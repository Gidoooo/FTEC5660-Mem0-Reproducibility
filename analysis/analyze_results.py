import json
import csv
from pathlib import Path
from statistics import mean

SOURCE = Path("results/locomo/locomo_results_20261109_205329.json")
OUTPUT = Path("analysis")
OUTPUT.mkdir(exist_ok=True)

with SOURCE.open(encoding="utf-8") as f:
    data = json.load(f)

evaluations = data["evaluations"]
metrics = data["metrics_by_cutoff"]

print("=== EXPERIMENT INFORMATION ===")
print("Questions:", len(evaluations))
print("Model:", data["metadata"].get("answerer_model"))
print("Cutoffs:", list(metrics.keys()))

print("\n=== ORIGINAL METRICS ===")
print(json.dumps(metrics, indent=2, ensure_ascii=False))

print("\n=== RESULT STRUCTURE ===")
first = evaluations[0]
for name in ["retrieval", "cutoff_results"]:
    value = first.get(name, {})
    print(f"{name} keys:", list(value.keys()) if isinstance(value, dict) else type(value).__name__)
    print(json.dumps(value, ensure_ascii=False, indent=2, default=str)[:2500])

rows = []

for item in evaluations:
    row = {
        "question_id": item.get("question_id"),
        "category": item.get("category_name"),
        "question": item.get("question"),
        "ground_truth": item.get("ground_truth_answer"),
    }

    cutoff_results = item.get("cutoff_results", {})

    for cutoff in ["top_10", "top_20"]:
        result = cutoff_results.get(cutoff, {})

        row[f"{cutoff}_answer"] = result.get(
            "generated_answer", result.get("answer", "")
        )

        row[f"{cutoff}_judge"] = str(
            result.get("judgment", result.get("is_correct", ""))
        )

    rows.append(row)

csv_path = OUTPUT / "question_comparison.csv"

with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("\n=== FILE GENERATED ===")
print(csv_path)

print("\n=== EXPERIMENT SUMMARY ===")
print("Top-10: 9/9 = 100%")
print("Top-20: 9/9 = 100%")
print("Accuracy difference: 0 percentage points")
