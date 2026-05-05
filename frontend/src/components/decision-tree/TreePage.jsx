import { useEffect, useState } from "react";
import PageShell from "@/components/layout/PageShell";
import Sidebar from "@/components/layout/Sidebar";
import MetricsPanel from "@/components/layout/MetricsPanel";
import { ChartSkeleton } from "@/components/shared/SkeletonLoader";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from "@/components/ui/select";
import {
  Tabs, TabsList, TabsTrigger,
} from "@/components/ui/tabs";
import { useDebounce } from "@/hooks/useDebounce";
import { useTreeStore, useUIStore } from "@/store/store";
import { runDecisionTree } from "@/lib/api";
import DatasetSelector from "@/components/shared/DatasetSelector";
import Tree from "react-d3-tree";

const DATASETS = ["iris", "breast_cancer", "blobs"];

export default function TreePage() {
  const s = useTreeStore();
  const setTheoryOpen = useUIStore((u) => u.setTheoryOpen);
  const [respA, setRespA] = useState(null);
  const [respB, setRespB] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isDemo, setIsDemo] = useState(false);

  const debouncedReq = useDebounce(
    {
      task: s.task,
      criterion: s.criterion,
      max_depth: s.max_depth,
      min_samples_split: s.min_samples_split,
      min_samples_leaf: s.min_samples_leaf,
      dataset: s.dataset,
      uploaded_data: s.uploadedDataset ? s.uploadedDataset.rows : null,
    },
    300
  );

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setIsDemo(false);
    Promise.all([
      runDecisionTree(debouncedReq, controller.signal),
      s.compareMode
        ? runDecisionTree({
            ...debouncedReq,
            criterion: debouncedReq.criterion === "gini" ? "entropy" : "gini",
          }, controller.signal)
        : Promise.resolve(null),
    ])
      .then(([a, b]) => {
        setRespA(a.data);
        setRespB(b?.data ?? null);
        setIsDemo(a.isDemo || Boolean(b?.isDemo));
        setLoading(false);
      })
      .catch((err) => {
        if (err.name !== "AbortError") {
          console.error("Unexpected error:", err);
          setLoading(false);
        }
      });
    return () => { controller.abort(); };
  }, [debouncedReq, s.compareMode]);

  return (
    <PageShell algorithm="decision-tree">
      <div className="flex flex-col lg:flex-row min-h-[calc(100vh-3.5rem)]">
        <Sidebar
          title="Decision Trees"
          subtitle="CART splits with Gini / Entropy and live pruning."
        >
          <div className="space-y-2">
            <Label className="text-sm text-neutral-200">Task Mode</Label>
            <Tabs value={s.task} onValueChange={(v) => s.set({ task: v })}>
              <TabsList data-testid="tabs-task" className="bg-neutral-900 border border-neutral-800 w-full">
                <TabsTrigger
                  value="classifier"
                  data-testid="tab-classifier"
                  className="flex-1 data-[state=active]:bg-amber-400 data-[state=active]:text-neutral-950"
                >
                  Classifier
                </TabsTrigger>
                <TabsTrigger
                  value="regressor"
                  data-testid="tab-regressor"
                  className="flex-1 data-[state=active]:bg-amber-400 data-[state=active]:text-neutral-950"
                >
                  Regressor
                </TabsTrigger>
              </TabsList>
            </Tabs>
          </div>

          <Field label="Splitting Criterion">
            <Select value={s.criterion} onValueChange={(v) => s.set({ criterion: v })}>
              <SelectTrigger data-testid="select-criterion" className="bg-neutral-900 border-neutral-700 text-neutral-100">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-neutral-900 border-neutral-700 text-neutral-100">
                <SelectItem value="gini">Gini Impurity</SelectItem>
                <SelectItem value="entropy">Entropy (Info Gain)</SelectItem>
              </SelectContent>
            </Select>
          </Field>

          <Field label={`Max Depth ${s.max_depth === null ? "(None)" : `= ${s.max_depth}`}`} hint="Drag to prune live">
            <Slider
              data-testid="slider-max-depth"
              value={[s.max_depth ?? 0]}
              min={0}
              max={10}
              step={1}
              onValueChange={(v) => s.set({ max_depth: v[0] === 0 ? null : v[0] })}
            />
          </Field>

          <Field label="Min Samples Split" value={s.min_samples_split}>
            <Slider
              data-testid="slider-min-split"
              value={[s.min_samples_split]}
              min={2}
              max={20}
              step={1}
              onValueChange={(v) => s.set({ min_samples_split: v[0] })}
            />
          </Field>

          <Field label="Min Samples Leaf" value={s.min_samples_leaf}>
            <Slider
              data-testid="slider-min-leaf"
              value={[s.min_samples_leaf]}
              min={1}
              max={20}
              step={1}
              onValueChange={(v) => s.set({ min_samples_leaf: v[0] })}
            />
          </Field>

          <Field label="Dataset">
            <DatasetSelector
              availableDatasets={DATASETS}
              value={s.dataset}
              onChange={(name, uploadedData) => {
                if (name === "__uploaded__" && uploadedData) {
                  s.set({ dataset: "__uploaded__", uploadedDataset: uploadedData });
                } else {
                  s.set({ dataset: name, uploadedDataset: null });
                }
              }}
            />
          </Field>

          <div className="flex items-center justify-between">
            <Label className="text-sm text-neutral-200">Compare Gini vs Entropy</Label>
            <Switch
              data-testid="switch-compare"
              checked={s.compareMode}
              onCheckedChange={(v) => s.set({ compareMode: v })}
            />
          </div>

          <button
            data-testid="open-theory"
            onClick={() => setTheoryOpen(true)}
            className="text-xs text-amber-300 hover:text-amber-200 underline-offset-4 hover:underline"
          >
            ⓘ Open Theory Drawer
          </button>
        </Sidebar>

        <main className="flex-1 flex flex-col">
          {isDemo && (
            <div className="mx-4 md:mx-6 mt-4 rounded-md border border-amber-400/20 bg-amber-400/5 px-4 py-2.5 text-xs text-amber-300 font-mono">
              Backend unreachable - displaying demo data. Set{" "}
              <code className="text-amber-200">REACT_APP_BACKEND_URL</code> to connect.
            </div>
          )}
          <div className="flex-1 p-4 md:p-6 space-y-4">
            {s.compareMode ? (
              <div className="grid gap-4 lg:grid-cols-2">
                <TreeCard
                  title={`Tree A — ${s.criterion === "gini" ? "Gini" : "Entropy"}`}
                  resp={respA}
                  loading={loading}
                  testid="tree-a"
                />
                <TreeCard
                  title={`Tree B — ${s.criterion === "gini" ? "Entropy" : "Gini"}`}
                  resp={respB}
                  loading={loading}
                  testid="tree-b"
                />
              </div>
            ) : (
              <TreeCard
                title="Decision Tree Diagram"
                resp={respA}
                loading={loading}
                testid="tree-main"
                large
              />
            )}
          </div>

          <MetricsPanel
            items={
              s.compareMode && respA && respB
                ? [
                    { label: "A Accuracy", value: respA.accuracy, color: "text-emerald-300" },
                    { label: "A Depth", value: respA.depth },
                    { label: "A Leaves", value: respA.n_leaves },
                    { label: "B Accuracy", value: respB.accuracy, color: "text-amber-200" },
                    { label: "B Depth", value: respB.depth },
                    { label: "B Leaves", value: respB.n_leaves },
                  ]
                : [
                    { label: "Accuracy", value: respA?.accuracy ?? "—", color: "text-emerald-300" },
                    { label: "Depth", value: respA?.depth ?? "—" },
                    { label: "Leaves", value: respA?.n_leaves ?? "—" },
                    { label: "Criterion", value: s.criterion },
                    {
                      label: "Top Feature",
                      value: respA?.feature_importances
                        ? Object.entries(respA.feature_importances).sort((a, b) => b[1] - a[1])[0][0]
                        : "—",
                      color: "text-amber-200",
                    },
                  ]
            }
          />
          {/* Feature Importance Bar Chart */}
          {!loading && respA?.feature_importances && (
            <FeatureImportanceChart 
              importances={respA.feature_importances} 
              title={s.compareMode && respB ? `A: Feature Importance` : "Feature Importance"}
            />
          )}
          {!loading && s.compareMode && respB?.feature_importances && (
            <FeatureImportanceChart 
              importances={respB.feature_importances} 
              title="B: Feature Importance"
            />
          )}
        </main>
      </div>
    </PageShell>
  );
}

function Field({ label, value, hint, children }) {
  return (
    <div className="space-y-2">
      <div className="flex items-baseline justify-between">
        <Label className="text-sm text-neutral-200">{label}</Label>
        {value !== undefined && <span className="text-xs font-mono text-amber-300">{value}</span>}
      </div>
      {children}
      {hint && <div className="text-[10px] text-neutral-500 font-mono">{hint}</div>}
    </div>
  );
}

function TreeCard({ title, resp, loading, testid, large }) {
  if (loading || !resp) {
    return (
      <div className="rounded-lg border border-neutral-800 bg-neutral-900/40 p-4">
        <div className="text-[11px] uppercase tracking-[0.18em] text-neutral-500 font-mono mb-2">{title}</div>
        <ChartSkeleton height={large ? 560 : 420} label="tree" />
      </div>
    );
  }
  return (
    <div data-testid={testid} className="rounded-lg border border-neutral-800 bg-neutral-900/40 p-4 overflow-hidden">
      <div className="flex items-center justify-between mb-2">
        <div className="text-[11px] uppercase tracking-[0.18em] text-neutral-500 font-mono">{title}</div>
        <div className="text-[10px] font-mono text-neutral-500">acc {resp.accuracy} · depth {resp.depth} · leaves {resp.n_leaves}</div>
      </div>
      <div
        className={`${large ? "h-[560px]" : "h-[420px]"} rounded bg-neutral-950/50 border border-neutral-800 overflow-hidden`}
        data-testid={`${testid}-canvas`}
      >
        <Tree
          data={resp.tree_json}
          orientation="vertical"
          translate={{ x: 320, y: 60 }}
          pathFunc="diagonal"
          collapsible={true}
          separation={{ siblings: 1, nonSiblings: 1.4 }}
          renderCustomNodeElement={renderNode}
          styles={{
            links: { stroke: "rgba(251,191,36,0.5)", strokeWidth: 1.4 },
          }}
        />
      </div>
    </div>
  );
}

function renderNode({ nodeDatum, toggleNode }) {
  const isLeaf = !nodeDatum.children || nodeDatum.children.length === 0;
  const attr = nodeDatum.attributes || {};
  const score = attr.gini ?? attr.entropy ?? "";
  const samples = attr.samples ?? "";
  return (
    <g onClick={toggleNode}>
      <rect
        width={210}
        height={isLeaf ? 60 : 70}
        x={-105}
        y={-30}
        rx={8}
        ry={8}
        fill={isLeaf ? "#0a0a0a" : "#171717"}
        stroke={isLeaf ? "#34d399" : "#fbbf24"}
        strokeWidth={1.5}
      />
      <text
        x={0}
        y={-8}
        textAnchor="middle"
        fontFamily="'IBM Plex Mono', monospace"
        fontSize={12}
        fill="#fafafa"
      >
        {nodeDatum.name}
      </text>
      <text
        x={0}
        y={12}
        textAnchor="middle"
        fontFamily="'IBM Plex Mono', monospace"
        fontSize={10}
        fill="#a3a3a3"
      >
        {`samples: ${samples}`}
      </text>
      {score !== "" && (
        <text
          x={0}
          y={26}
          textAnchor="middle"
          fontFamily="'IBM Plex Mono', monospace"
          fontSize={10}
          fill={isLeaf ? "#34d399" : "#fbbf24"}
        >
          {`${attr.gini != null ? "gini" : "entropy"}: ${score}`}
        </text>
      )}
    </g>
  );
}

function FeatureImportanceChart({ importances, title }) {
  const sorted = Object.entries(importances)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8); // Show top 8 features

  const maxImportance = Math.max(...sorted.map(([, v]) => v));

  return (
    <div className="rounded-lg border border-neutral-800 bg-neutral-900/40 p-4">
      <div className="text-[11px] uppercase tracking-[0.18em] text-neutral-500 font-mono mb-3">{title}</div>
      <div className="space-y-2">
        {sorted.map(([feature, importance], idx) => (
          <div key={idx} className="flex items-center gap-2">
            <span className="text-xs text-neutral-400 min-w-[80px] truncate">{feature}</span>
            <div className="flex-1 h-5 bg-neutral-950/50 rounded border border-neutral-800 overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-amber-500 to-amber-400 transition-all"
                style={{
                  width: `${(importance / maxImportance) * 100}%`,
                }}
              />
            </div>
            <span className="text-[10px] font-mono text-amber-300 min-w-[45px] text-right">
              {(importance * 100).toFixed(1)}%
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
