# Mop math

What "dilute 1:100" actually means in your bucket, how many buckets a bottle covers, and what one clean floor costs. Exact arithmetic in the browser, every borrowed number labeled.

Live site: https://ilanis-agent.github.io/mopmath/

## The three tools

- **Dilution plan** - `dilutePlan(ratio, bucketL)`: the label ratio and bucket size become exact milliliters of concentrate.
- **Bottle plan** - `bottlePlan(bottleMl, ratio, bucketL, bucketsWeek)`: a bottle becomes the buckets it covers and the weeks it lasts.
- **Cost plan** - `costPlan(price, bottleMl, ratio, bucketL, bucketsWeek)`: the price becomes the cost per bucket and per year.

## Labeled norms (illustrative references, not rules)

- A labeled ratio like 1:100 means one part concentrate per hundred parts of the mix, read straight off the product label.
- Always follow your own bottle's label and safety directions first.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (35 cases, 105 checks)

Regenerate the oracle expectations: `python3 oracle.py`
