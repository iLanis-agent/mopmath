#!/usr/bin/env python3
"""Oracle mirror of engine.js for Mop math. Writes expected.json (with trailing newline)."""
import json, math

def r1(x): return math.floor(x * 10 + 0.5) / 10
def r2(x): return math.floor(x * 100 + 0.5) / 100

def jsnum(x):
    if isinstance(x, float) and x == int(x) and abs(x) < 1e15:
        return int(x)
    return x

def fmt(x):
    if isinstance(x, float) and x == int(x):
        return str(int(x))
    return repr(x) if isinstance(x, float) else str(x)

def dilutePlan(ratio, bucketL):
    if not (ratio > 0) or not (bucketL > 0):
        return {"error": "ratio and bucket size must be positive"}
    ml = r1(bucketL * 1000 / ratio)
    return {"ratio": jsnum(float(ratio)), "bucketL": jsnum(float(bucketL)), "concentrateMl": jsnum(ml)}

def bottlePlan(bottleMl, ratio, bucketL, bucketsWeek):
    if not (bottleMl > 0) or not (ratio > 0) or not (bucketL > 0) or not (bucketsWeek > 0):
        return {"error": "bottle, ratio, bucket and pace must be positive"}
    mlPerBucket = bucketL * 1000 / ratio
    if mlPerBucket > bottleMl:
        return {"error": "one bucket needs more than the whole bottle"}
    buckets = r1(bottleMl / mlPerBucket)
    weeks = r1(buckets / bucketsWeek)
    return {"bottleMl": jsnum(float(bottleMl)), "ratio": jsnum(float(ratio)), "bucketL": jsnum(float(bucketL)),
            "bucketsWeek": jsnum(float(bucketsWeek)), "mlPerBucket": jsnum(r1(mlPerBucket)),
            "buckets": jsnum(buckets), "weeks": jsnum(weeks)}

def costPlan(price, bottleMl, ratio, bucketL, bucketsWeek):
    if not (price > 0) or not (bottleMl > 0) or not (ratio > 0) or not (bucketL > 0) or not (bucketsWeek > 0):
        return {"error": "price, bottle, ratio, bucket and pace must be positive"}
    mlPerBucket = bucketL * 1000 / ratio
    if mlPerBucket > bottleMl:
        return {"error": "one bucket needs more than the whole bottle"}
    perBucket = r2(price * mlPerBucket / bottleMl)
    perYear = r2(perBucket * bucketsWeek * 52)
    return {"price": jsnum(float(price)), "bottleMl": jsnum(float(bottleMl)), "ratio": jsnum(float(ratio)),
            "bucketL": jsnum(float(bucketL)), "bucketsWeek": jsnum(float(bucketsWeek)),
            "perBucket": jsnum(perBucket), "perYear": jsnum(perYear)}

def renderDilute(r):
    return ("For a labeled 1:" + fmt(r["ratio"]) + " dilution, " + ("a" if r["bucketL"] == 1 else "a " + fmt(r["bucketL"]) + "-liter") +
            " bucket needs " + fmt(r["concentrateMl"]) + " ml of concentrate - the rest is water.")

def renderBottle(r):
    return ("A " + fmt(r["bottleMl"]) + " ml bottle at a labeled 1:" + fmt(r["ratio"]) + " dilution covers " + fmt(r["buckets"]) +
            " buckets of " + fmt(r["mlPerBucket"]) + " ml each - about " + fmt(r["weeks"]) + " weeks at " + fmt(r["bucketsWeek"]) + " buckets a week.")

def renderCost(r):
    return ("Each bucket costs about " + fmt(r["perBucket"]) + " in concentrate at a labeled 1:" + fmt(r["ratio"]) +
            " dilution - about " + fmt(r["perYear"]) + " a year at " + fmt(r["bucketsWeek"]) + " buckets a week.")

CASES = []
CASES.append({"fn": "dilutePlan", "args": [100, 5]})
CASES.append({"fn": "dilutePlan", "args": [64, 4]})
CASES.append({"fn": "dilutePlan", "args": [200, 10]})
CASES.append({"fn": "dilutePlan", "args": [50, 3]})
CASES.append({"fn": "dilutePlan", "args": [128, 1]})
CASES.append({"fn": "dilutePlan", "args": [256, 7.5]})
CASES.append({"fn": "dilutePlan", "args": [0, 5]})
CASES.append({"fn": "dilutePlan", "args": [100, 0]})
CASES.append({"fn": "dilutePlan", "args": [32, 2]})
CASES.append({"fn": "dilutePlan", "args": [180, 6]})
CASES.append({"fn": "dilutePlan", "args": [75, 4.5]})
CASES.append({"fn": "dilutePlan", "args": [500, 8]})
CASES.append({"fn": "bottlePlan", "args": [500, 100, 5, 3]})
CASES.append({"fn": "bottlePlan", "args": [750, 64, 4, 2]})
CASES.append({"fn": "bottlePlan", "args": [1000, 200, 10, 4]})
CASES.append({"fn": "bottlePlan", "args": [250, 50, 3, 1]})
CASES.append({"fn": "bottlePlan", "args": [946, 128, 1, 7]})
CASES.append({"fn": "bottlePlan", "args": [600, 32, 2, 5]})
CASES.append({"fn": "bottlePlan", "args": [0, 100, 5, 3]})
CASES.append({"fn": "bottlePlan", "args": [500, 0, 5, 3]})
CASES.append({"fn": "bottlePlan", "args": [40, 100, 5, 3]})
CASES.append({"fn": "bottlePlan", "args": [500, 100, 5, 0]})
CASES.append({"fn": "bottlePlan", "args": [300, 180, 6, 2]})
CASES.append({"fn": "bottlePlan", "args": [2000, 500, 8, 3]})
CASES.append({"fn": "costPlan", "args": [8, 500, 100, 5, 3]})
CASES.append({"fn": "costPlan", "args": [12, 750, 64, 4, 2]})
CASES.append({"fn": "costPlan", "args": [5.5, 1000, 200, 10, 4]})
CASES.append({"fn": "costPlan", "args": [15, 946, 128, 1, 7]})
CASES.append({"fn": "costPlan", "args": [9.99, 600, 32, 2, 5]})
CASES.append({"fn": "costPlan", "args": [0, 500, 100, 5, 3]})
CASES.append({"fn": "costPlan", "args": [8, 500, 100, 5, 0]})
CASES.append({"fn": "costPlan", "args": [8, 40, 100, 5, 3]})
CASES.append({"fn": "costPlan", "args": [6.75, 300, 180, 6, 2]})
CASES.append({"fn": "costPlan", "args": [22, 2000, 500, 8, 3]})
CASES.append({"fn": "costPlan", "args": [11.5, 400, 75, 4.5, 6]})

out = []
for c in CASES:
    fn = {"dilutePlan": dilutePlan, "bottlePlan": bottlePlan, "costPlan": costPlan}[c["fn"]]
    r = fn(*c["args"])
    is_err = "error" in r
    if is_err:
        render = r["error"]
    else:
        render = {"dilutePlan": renderDilute, "bottlePlan": renderBottle, "costPlan": renderCost}[c["fn"]](r)
    out.append({"fn": c["fn"], "args": c["args"], "result": r, "render": render, "isError": is_err})

with open("expected.json", "w") as f:
    json.dump(out, f, separators=(",", ":"))
    f.write("\n")
print("wrote", len(out), "cases")
