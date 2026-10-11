/* Mop math engine - pure arithmetic, every borrowed number labeled. */
(function (root) {
  "use strict";
  function r1(x) { return Math.round(x * 10) / 10; }
  function r2(x) { return Math.round(x * 100) / 100; }

  function dilutePlan(ratio, bucketL) {
    if (!(ratio > 0) || !(bucketL > 0)) return { error: "ratio and bucket size must be positive" };
    var ml = r1(bucketL * 1000 / ratio);
    return { ratio: ratio, bucketL: bucketL, concentrateMl: ml };
  }

  function bottlePlan(bottleMl, ratio, bucketL, bucketsWeek) {
    if (!(bottleMl > 0) || !(ratio > 0) || !(bucketL > 0) || !(bucketsWeek > 0)) return { error: "bottle, ratio, bucket and pace must be positive" };
    var mlPerBucket = bucketL * 1000 / ratio;
    if (mlPerBucket > bottleMl) return { error: "one bucket needs more than the whole bottle" };
    var buckets = r1(bottleMl / mlPerBucket);
    var weeks = r1(buckets / bucketsWeek);
    return { bottleMl: bottleMl, ratio: ratio, bucketL: bucketL, bucketsWeek: bucketsWeek, mlPerBucket: r1(mlPerBucket), buckets: buckets, weeks: weeks };
  }

  function costPlan(price, bottleMl, ratio, bucketL, bucketsWeek) {
    if (!(price > 0) || !(bottleMl > 0) || !(ratio > 0) || !(bucketL > 0) || !(bucketsWeek > 0)) return { error: "price, bottle, ratio, bucket and pace must be positive" };
    var mlPerBucket = bucketL * 1000 / ratio;
    if (mlPerBucket > bottleMl) return { error: "one bucket needs more than the whole bottle" };
    var perBucket = r2(price * mlPerBucket / bottleMl);
    var perYear = r2(perBucket * bucketsWeek * 52);
    return { price: price, bottleMl: bottleMl, ratio: ratio, bucketL: bucketL, bucketsWeek: bucketsWeek, perBucket: perBucket, perYear: perYear };
  }

  function renderDilute(r) {
    return "For a labeled 1:" + r.ratio + " dilution, " + (r.bucketL === 1 ? "a" : "a " + r.bucketL + "-liter") + " bucket needs " + r.concentrateMl + " ml of concentrate - the rest is water.";
  }

  function renderBottle(r) {
    return "A " + r.bottleMl + " ml bottle at a labeled 1:" + r.ratio + " dilution covers " + r.buckets + " buckets of " + r.mlPerBucket + " ml each - about " + r.weeks + " weeks at " + r.bucketsWeek + " buckets a week.";
  }

  function renderCost(r) {
    return "Each bucket costs about " + r.perBucket + " in concentrate at a labeled 1:" + r.ratio + " dilution - about " + r.perYear + " a year at " + r.bucketsWeek + " buckets a week.";
  }

  var api = { dilutePlan: dilutePlan, bottlePlan: bottlePlan, costPlan: costPlan,
              renderDilute: renderDilute, renderBottle: renderBottle, renderCost: renderCost };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.MopMath = api;
})(typeof window !== "undefined" ? window : this);
