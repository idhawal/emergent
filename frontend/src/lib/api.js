// Mock API layer that mirrors backend contracts defined in spec.md §5.
// Each function returns a Promise resolving to data in the exact shape the
// real FastAPI backend will produce. This lets the frontend be developed
// fully independently per the spec's "decoupled Client–Server architecture".

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ---------- helpers ----------
const range = (n) => Array.from({ length: n }, (_, i) => i);
const rand = (a = -1, b = 1) => a + Math.random() * (b - a);
const gauss = () => {
  // Box-Muller
  let u = 0, v = 0;
  while (u === 0) u = Math.random();
  while (v === 0) v = Math.random();
  return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
};

// ---------- /api/regression ----------
export async function runRegression(req) {
  await sleep(280);
  const {
    algo = "linear_gd",
    learning_rate = 0.01,
    epochs = 1000,
    poly_degree = 1,
    penalty = 1,
    l1_ratio = 0.5,
    noise = 0.3,
    early_stopping = false,
  } = req;

  const N = 80;
  const scatter_x = range(N).map((i) => -3 + (6 * i) / (N - 1));
  // synthetic poly signal
  const trueCoef = [1.5, -0.8, 0.4, -0.2];
  const scatter_y = scatter_x.map((x) => {
    let y = 0;
    for (let d = 0; d < poly_degree + 1; d++) y += (trueCoef[d] || 0) * Math.pow(x, d);
    return y + gauss() * noise * 1.2;
  });

  const curve_x = range(200).map((i) => -3 + (6 * i) / 199);
  // For Lasso emulate sparsity by zeroing high-degree coeffs based on penalty
  const learnedCoefs = trueCoef.slice(0, poly_degree + 1).map((c, i) => {
    if (algo === "lasso" && penalty >= 10) return i > 1 ? 0 : c * (1 - penalty / 200);
    if (algo === "ridge") return c * (1 / (1 + penalty / 50));
    if (algo === "elastic_net") {
      const shrink = 1 / (1 + penalty / 80);
      return penalty >= 10 && i > 2 ? 0 : c * shrink;
    }
    return c + gauss() * 0.05;
  });
  const curve_y = curve_x.map((x) => {
    let y = 0;
    for (let d = 0; d < learnedCoefs.length; d++) y += learnedCoefs[d] * Math.pow(x, d);
    return y;
  });

  // cost history
  let stoppedAt = null;
  const cost = [];
  let prev = 5 + Math.random() * 2;
  for (let e = 0; e < epochs; e++) {
    const target = 0.05 + noise * 0.4;
    const decay = Math.exp(-learning_rate * e * 8);
    let c = target + (prev - target) * decay + gauss() * 0.005 * decay;
    if (early_stopping && e > 30 && Math.random() < 0.0008) {
      // simulate occasional bumps; trigger early stop after 5 increases
      c = cost[cost.length - 1] + 0.02;
    }
    cost.push(Math.max(c, 0.0001));
    // detect 5 consecutive increases
    if (early_stopping && cost.length > 6) {
      const tail = cost.slice(-6);
      let inc = 0;
      for (let i = 1; i < tail.length; i++) if (tail[i] > tail[i - 1]) inc++;
      if (inc >= 5) {
        stoppedAt = e;
        break;
      }
    }
  }

  const feature_names = range(learnedCoefs.length).map((i) => (i === 0 ? "bias" : `x^${i}`));

  return {
    curve_x,
    curve_y,
    scatter_x,
    scatter_y,
    cost_history: cost,
    coefficients: learnedCoefs,
    feature_names,
    stopped_at_epoch: stoppedAt,
  };
}

// ---------- /api/knn ----------
function makeMoons(n = 200, noise = 0.15) {
  const pts = [];
  const labels = [];
  const half = Math.floor(n / 2);
  for (let i = 0; i < half; i++) {
    const t = (Math.PI * i) / half;
    pts.push([Math.cos(t) + gauss() * noise, Math.sin(t) + gauss() * noise]);
    labels.push(0);
  }
  for (let i = 0; i < half; i++) {
    const t = (Math.PI * i) / half;
    pts.push([1 - Math.cos(t) + gauss() * noise, 0.5 - Math.sin(t) + gauss() * noise]);
    labels.push(1);
  }
  return { pts, labels };
}
function makeCircles(n = 200, noise = 0.08) {
  const pts = [];
  const labels = [];
  for (let i = 0; i < n; i++) {
    const cls = i % 2;
    const r = cls === 0 ? 0.5 : 1.0;
    const t = Math.random() * 2 * Math.PI;
    pts.push([r * Math.cos(t) + gauss() * noise, r * Math.sin(t) + gauss() * noise]);
    labels.push(cls);
  }
  return { pts, labels };
}
function makeBlobs(n = 200) {
  const centers = [[-1.5, -1], [1.5, 1.2], [0, 1.5]];
  const pts = [];
  const labels = [];
  for (let i = 0; i < n; i++) {
    const c = i % centers.length;
    pts.push([centers[c][0] + gauss() * 0.4, centers[c][1] + gauss() * 0.4]);
    labels.push(c);
  }
  return { pts, labels };
}
function makeSine(n = 120, noise = 0.2) {
  const pts = [];
  const labels = [];
  for (let i = 0; i < n; i++) {
    const x = -3 + (6 * i) / (n - 1);
    const y = Math.sin(x) + gauss() * noise;
    pts.push([x, y]);
    labels.push(y);
  }
  return { pts, labels };
}

export async function runKNN(req) {
  await sleep(220);
  const { k = 5, metric = "euclidean", weights = "uniform", task = "classification", dataset = "moons", test_point = null } = req;

  let data;
  if (dataset === "moons") data = makeMoons();
  else if (dataset === "circles") data = makeCircles();
  else if (dataset === "blobs") data = makeBlobs();
  else data = makeSine();

  const { pts, labels } = data;
  // build mesh
  const xs = pts.map((p) => p[0]);
  const ys = pts.map((p) => p[1]);
  const xmin = Math.min(...xs) - 0.6;
  const xmax = Math.max(...xs) + 0.6;
  const ymin = Math.min(...ys) - 0.6;
  const ymax = Math.max(...ys) + 0.6;
  const G = 60;
  const mesh_xx = [];
  const mesh_yy = [];
  const mesh_zz = [];
  for (let j = 0; j < G; j++) {
    const rowX = [], rowY = [], rowZ = [];
    for (let i = 0; i < G; i++) {
      const x = xmin + ((xmax - xmin) * i) / (G - 1);
      const y = ymin + ((ymax - ymin) * j) / (G - 1);
      rowX.push(x);
      rowY.push(y);
      rowZ.push(predictKNN([x, y], pts, labels, k, metric, weights, task));
    }
    mesh_xx.push(rowX);
    mesh_yy.push(rowY);
    mesh_zz.push(rowZ);
  }

  let neighbor_indices = [];
  let test_prediction = null;
  if (test_point) {
    const dists = pts.map((p, idx) => ({ idx, d: distance(test_point, p, metric) }));
    dists.sort((a, b) => a.d - b.d);
    neighbor_indices = dists.slice(0, k).map((x) => x.idx);
    test_prediction = predictKNN(test_point, pts, labels, k, metric, weights, task);
  }

  return {
    train_points: pts,
    train_labels: labels,
    mesh_xx,
    mesh_yy,
    mesh_zz,
    neighbor_indices,
    test_prediction,
    bounds: { xmin, xmax, ymin, ymax },
  };
}

function distance(a, b, metric) {
  if (metric === "manhattan") return Math.abs(a[0] - b[0]) + Math.abs(a[1] - b[1]);
  return Math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2);
}
function predictKNN(point, pts, labels, k, metric, weights, task) {
  const dists = pts.map((p, idx) => ({ idx, d: distance(point, p, metric) }));
  dists.sort((a, b) => a.d - b.d);
  const top = dists.slice(0, k);
  if (task === "classification") {
    const tally = {};
    top.forEach((t) => {
      const w = weights === "distance" ? 1 / (t.d + 1e-6) : 1;
      tally[labels[t.idx]] = (tally[labels[t.idx]] || 0) + w;
    });
    let best = null;
    let bestV = -Infinity;
    Object.entries(tally).forEach(([k2, v]) => {
      if (v > bestV) {
        bestV = v;
        best = parseInt(k2, 10);
      }
    });
    return best;
  }
  let num = 0, den = 0;
  top.forEach((t) => {
    const w = weights === "distance" ? 1 / (t.d + 1e-6) : 1;
    num += labels[t.idx] * w;
    den += w;
  });
  return num / den;
}

// ---------- /api/decision_tree ----------
function buildMockTree(criterion, maxDepth, dataset, depth = 0, samples = 150) {
  const featureNames =
    dataset === "iris"
      ? ["sepal_length", "sepal_width", "petal_length", "petal_width"]
      : dataset === "breast_cancer"
      ? ["mean_radius", "mean_texture", "mean_perimeter"]
      : ["x_0", "x_1"];
  const leafLimit = maxDepth === null ? 4 : Math.min(maxDepth, 5);
  const isLeaf = depth >= leafLimit || samples < 6;
  const f = featureNames[depth % featureNames.length];
  const threshold = (Math.random() * 4 + 0.5).toFixed(2);
  const score = criterion === "gini" ? +(Math.random() * 0.5).toFixed(3) : +(Math.random() * 1.4).toFixed(3);
  if (isLeaf) {
    return {
      name: `class = ${Math.floor(Math.random() * 3)}`,
      attributes: {
        [criterion]: score,
        samples,
        class_dist: [Math.floor(samples * 0.6), Math.floor(samples * 0.3), samples - Math.floor(samples * 0.6) - Math.floor(samples * 0.3)],
      },
    };
  }
  const leftN = Math.floor(samples * (0.4 + Math.random() * 0.2));
  return {
    name: `${f} ≤ ${threshold}`,
    attributes: {
      [criterion]: score,
      samples,
      class_dist: [Math.floor(samples * 0.4), Math.floor(samples * 0.3), samples - Math.floor(samples * 0.4) - Math.floor(samples * 0.3)],
    },
    children: [
      buildMockTree(criterion, maxDepth, dataset, depth + 1, leftN),
      buildMockTree(criterion, maxDepth, dataset, depth + 1, samples - leftN),
    ],
  };
}
function countLeaves(node) {
  if (!node.children) return 1;
  return node.children.reduce((s, c) => s + countLeaves(c), 0);
}
function treeDepth(node) {
  if (!node.children) return 1;
  return 1 + Math.max(...node.children.map(treeDepth));
}

export async function runDecisionTree(req) {
  await sleep(260);
  const { task = "classifier", criterion = "gini", max_depth = 3, dataset = "iris" } = req;
  const tree_json = buildMockTree(criterion, max_depth, dataset);
  const accuracy = +(0.85 + Math.random() * 0.13).toFixed(3);
  const featImpKeys =
    dataset === "iris"
      ? ["sepal_length", "sepal_width", "petal_length", "petal_width"]
      : dataset === "breast_cancer"
      ? ["mean_radius", "mean_texture", "mean_perimeter"]
      : ["x_0", "x_1"];
  const raw = featImpKeys.map(() => Math.random());
  const sum = raw.reduce((a, b) => a + b, 0);
  const feature_importances = {};
  featImpKeys.forEach((k, i) => (feature_importances[k] = +(raw[i] / sum).toFixed(3)));
  return {
    tree_json,
    accuracy,
    depth: treeDepth(tree_json),
    n_leaves: countLeaves(tree_json),
    feature_importances,
  };
}

// ---------- /api/genetic_algorithm ----------
const benchFns = {
  sphere: (x, y) => x * x + y * y,
  rosenbrock: (x, y) => (1 - x) ** 2 + 100 * (y - x * x) ** 2,
  rastrigin: (x, y) => 20 + (x * x - 10 * Math.cos(2 * Math.PI * x)) + (y * y - 10 * Math.cos(2 * Math.PI * y)),
};

export async function runGA(req) {
  await sleep(320);
  const { function: fn = "sphere", pop_size = 50, mutation_rate = 0.1, crossover_rate = 0.8, generations = 80, eta_m = 20, eta_c = 15 } = req;

  const f = benchFns[fn];
  const span = fn === "rosenbrock" ? 2.5 : 5.0;

  // contour grid
  const G = 60;
  const contour_x = [];
  const contour_y = [];
  const contour_z = [];
  for (let j = 0; j < G; j++) {
    const rx = [], ry = [], rz = [];
    for (let i = 0; i < G; i++) {
      const x = -span + (2 * span * i) / (G - 1);
      const y = -span + (2 * span * j) / (G - 1);
      rx.push(x);
      ry.push(y);
      rz.push(f(x, y));
    }
    contour_x.push(rx);
    contour_y.push(ry);
    contour_z.push(rz);
  }

  // initial population
  let pop = range(pop_size).map(() => [rand(-span, span), rand(-span, span)]);
  const history = [];
  let best = Infinity;
  let convergedAt = null;
  for (let g = 0; g < generations; g++) {
    const fitness_values = pop.map((p) => f(p[0], p[1]));
    const best_fit = Math.min(...fitness_values);
    const avg_fit = fitness_values.reduce((a, b) => a + b, 0) / fitness_values.length;
    const best_idx = fitness_values.indexOf(best_fit);
    history.push({
      generation: g + 1,
      points: pop.map((p) => [p[0], p[1]]),
      fitness_values: [...fitness_values],
      best_fitness: best_fit,
      avg_fitness: avg_fit,
      best_point: [pop[best_idx][0], pop[best_idx][1]],
    });
    if (best_fit < best - 1e-4) best = best_fit;
    if (convergedAt === null && best_fit < 0.05 * (1 - mutation_rate * 0.5)) convergedAt = g + 1;

    // selection by tournament + simulated SBX-ish crossover + polynomial mutation
    const newPop = [];
    while (newPop.length < pop_size) {
      const a = pop[Math.floor(Math.random() * pop_size)];
      const b = pop[Math.floor(Math.random() * pop_size)];
      let child = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
      if (Math.random() < crossover_rate) {
        const beta = (1 + 1 / (eta_c + 1)) * (Math.random() - 0.5);
        child = [a[0] + beta * (b[0] - a[0]), a[1] + beta * (b[1] - a[1])];
      }
      if (Math.random() < mutation_rate) {
        child[0] += gauss() * (1 / (eta_m + 1)) * span;
        child[1] += gauss() * (1 / (eta_m + 1)) * span;
      }
      // pull slightly toward best
      child[0] = child[0] * 0.985 + history[history.length - 1].best_point[0] * 0.015;
      child[1] = child[1] * 0.985 + history[history.length - 1].best_point[1] * 0.015;
      child[0] = Math.max(-span, Math.min(span, child[0]));
      child[1] = Math.max(-span, Math.min(span, child[1]));
      newPop.push(child);
    }
    pop = newPop;
  }

  return {
    contour_x,
    contour_y,
    contour_z,
    history,
    converged_at_generation: convergedAt,
    span,
  };
}
