import { create } from "zustand";
import { persist } from "zustand/middleware";

export const useUIStore = create(
  persist(
    (set) => ({
      theoryOpen: false,
      setTheoryOpen: (v) => set({ theoryOpen: v }),
      hasSeenTheoryHint: false,
      setHasSeenTheoryHint: (v) => set({ hasSeenTheoryHint: v }),
    }),
    {
      name: "ml-visualizer-ui",
    }
  )
);

export const useRegressionStore = create((set) => ({
  algo: "linear_gd",
  learning_rate: 0.01,
  epochs: 1000,
  poly_degree: 2,
  penalty: 1,
  l1_ratio: 0.5,
  noise: 0.3,
  early_stopping: false,
  dataset: "linear",
  uploadedDataset: null,
  set: (patch) => set(patch),
}));

export const useKNNStore = create((set) => ({
  k: 5,
  metric: "euclidean",
  weights: "uniform",
  task: "classification",
  dataset: "moons",
  uploadedDataset: null,
  test_point: null,
  compareMode: false,
  set: (patch) => set(patch),
}));

export const useTreeStore = create((set) => ({
  task: "classifier",
  criterion: "gini",
  max_depth: 3,
  min_samples_split: 2,
  min_samples_leaf: 1,
  dataset: "iris",
  uploadedDataset: null,
  compareMode: false,
  set: (patch) => set(patch),
}));

export const useGAStore = create((set) => ({
  function: "sphere",
  pop_size: 50,
  mutation_rate: 0.1,
  crossover_rate: 0.8,
  generations: 80,
  eta_m: 20,
  eta_c: 15,
  ghostHistory: null, // for function-switcher comparison
  set: (patch) => set(patch),
}));
