import { useEffect, useMemo, useState } from "react";
import PageShell from "@/components/layout/PageShell";
import Sidebar from "@/components/layout/Sidebar";
import MetricsPanel from "@/components/layout/MetricsPanel";
import { ChartSkeleton } from "@/components/shared/SkeletonLoader";
import PlotlyChart from "@/components/shared/PlotlyChart";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { RotateCcw, Play, MousePointerClick } from "lucide-react";
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from "@/components/ui/select";
import {
  Tabs, TabsList, TabsTrigger,
} from "@/components/ui/tabs";
import { useDebounce } from "@/hooks/useDebounce";
import { useKNNStore, useUIStore } from "@/store/store";
import { runKNN } from "@/lib/api";
import DatasetSelector from "@/components/shared/DatasetSelector";

const KNN_DATASETS = ["moons", "circles", "blobs"];

const CLASS_COLORS = ["#fbbf24", "#34d399", "#60a5fa", "#f472b6"]; // amber, emerald, sky, pink

export default function KNNPage() {
  const s = useKNNStore();
  const setTheoryOpen = useUIStore((u) => u.setTheoryOpen);
  const [resp, setResp] = useState(null);
  const [respCompare, setRespCompare] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isDemo, setIsDemo] = useState(false);

  const debouncedReq = useDebounce(
    {
      k: s.k,
      metric: s.metric,
      weights: s.weights,
      task: s.task,
      dataset: s.dataset,
      test_point: s.test_point,
      uploaded_data: s.uploadedDataset ? s.uploadedDataset.rows : null,
    },
    300
  );

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setIsDemo(false);
    Promise.all([
      runKNN(debouncedReq, controller.signal),
      s.compareMode
        ? runKNN({
            ...debouncedReq,
            weights: debouncedReq.weights === "uniform" ? "distance" : "uniform",
          }, controller.signal)
        : Promise.resolve(null),
    ])
      .then(([a, b]) => {
        setResp(a.data);
        setRespCompare(b?.data ?? null);
        setIsDemo(a.isDemo || Boolean(b?.isDemo));
        setLoading(false);
      })
      .catch((err) => {
        if (err.name !== "AbortError") {
          console.error("Unexpected error:", err);
          setLoading(false);
        }
      });
    return () => {
      controller.abort();
    };
  }, [debouncedReq, s.compareMode]);

  const onPlotClick = (e) => {
    if (!e?.points?.length) return;
    const p = e.points[0];
    s.set({ test_point: [p.x, p.y] });
  };

  return (
    <PageShell algorithm="knn">
      <div className="flex flex-col lg:flex-row min-h-[calc(100vh-3.5rem)]">
        <Sidebar
          title="K-Nearest Neighbors"
          subtitle="Distance-based classification & regression"
          footer={
            <Button
              data-testid="reset-test-point"
              variant="outline"
              className="w-full border-neutral-700 bg-neutral-900 text-neutral-200 hover:bg-neutral-800"
              onClick={() => s.set({ test_point: null })}
            >
              <RotateCcw className="h-4 w-4 mr-1.5" />
              Clear Test Point
            </Button>
          }
        >
          <div className="space-y-2">
            <Label className="text-sm text-neutral-200">Task Mode</Label>
            <Tabs
              value={s.task}
              onValueChange={(v) =>
                s.set({
                  task: v,
                  dataset: "moons",
                  uploadedDataset: null,
                  test_point: null,
                })
              }
            >
              <TabsList data-testid="tabs-task" className="bg-neutral-900 border border-neutral-800 w-full">
                <TabsTrigger
                  value="classification"
                  data-testid="tab-classification"
                  className="flex-1 data-[state=active]:bg-amber-400 data-[state=active]:text-neutral-950"
                >
                  Classification
                </TabsTrigger>
                <TabsTrigger
                  value="regression"
                  data-testid="tab-regression"
                  className="flex-1 data-[state=active]:bg-amber-400 data-[state=active]:text-neutral-950"
                >
                  Regression
                </TabsTrigger>
              </TabsList>
            </Tabs>
          </div>

          <Field label="K (Neighbors)" value={s.k} hint="1 → 50">
            <Slider
              data-testid="slider-k"
              value={[s.k]}
              min={1}
              max={50}
              step={1}
              onValueChange={(v) => s.set({ k: v[0] })}
            />
          </Field>

          <Field label="Distance Metric">
            <Select value={s.metric} onValueChange={(v) => s.set({ metric: v })}>
              <SelectTrigger data-testid="select-metric" className="bg-neutral-900 border-neutral-700 text-neutral-100">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-neutral-900 border-neutral-700 text-neutral-100">
                <SelectItem value="euclidean">Euclidean (L2)</SelectItem>
                <SelectItem value="manhattan">Manhattan (L1)</SelectItem>
              </SelectContent>
            </Select>
          </Field>

          <div className="flex items-center justify-between">
            <Label className="text-sm text-neutral-200">Distance-Weighted</Label>
            <Switch
              data-testid="switch-weights"
              checked={s.weights === "distance"}
              onCheckedChange={(v) => s.set({ weights: v ? "distance" : "uniform" })}
            />
          </div>

          <Field label="Dataset">
            <DatasetSelector
              availableDatasets={KNN_DATASETS}
              value={s.dataset}
              onChange={(name, uploadedData) => {
                if (name === "__uploaded__" && uploadedData) {
                  s.set({ dataset: "__uploaded__", uploadedDataset: uploadedData, test_point: null });
                } else {
                  s.set({ dataset: name, uploadedDataset: null, test_point: null });
                }
              }}
            />
          </Field>

          <div className="flex items-center justify-between">
            <Label className="text-sm text-neutral-200">Compare Mode (Uniform vs Distance)</Label>
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
            <div className="rounded-md bg-neutral-900/40 border border-neutral-800 px-3 py-2 flex items-center gap-2 text-xs text-neutral-400">
              <MousePointerClick className="h-3.5 w-3.5 text-amber-300" />
              Click anywhere on the boundary plot to drop a test point. Lines connect to its K neighbors.
            </div>

            {s.compareMode ? (
              <div className="grid gap-4 lg:grid-cols-2">
                <BoundaryCard
                  title="Uniform Weighting"
                  resp={s.weights === "uniform" ? resp : respCompare}
                  loading={loading}
                  testPoint={s.test_point}
                  onClick={onPlotClick}
                  k={s.k}
                  task={s.task}
                  testid="chart-uniform"
                />
                <BoundaryCard
                  title="Distance Weighting"
                  resp={s.weights === "distance" ? resp : respCompare}
                  loading={loading}
                  testPoint={s.test_point}
                  onClick={onPlotClick}
                  k={s.k}
                  task={s.task}
                  testid="chart-distance"
                />
              </div>
            ) : (
              <BoundaryCard
                title={`Decision ${s.task === "classification" ? "Boundary" : "Surface"}`}
                resp={resp}
                loading={loading}
                testPoint={s.test_point}
                onClick={onPlotClick}
                k={s.k}
                task={s.task}
                testid="chart-main"
                large
              />
            )}
          </div>

          <MetricsPanel
            items={[
              { label: "K", value: s.k, color: "text-amber-200" },
              { label: "Metric", value: s.metric },
              { label: "Weights", value: s.weights },
              { label: "Dataset", value: s.dataset },
              {
                label: "Test Prediction",
                value:
                  s.test_point && resp?.test_prediction != null
                    ? typeof resp.test_prediction === "number" && s.task === "regression"
                      ? resp.test_prediction.toFixed(3)
                      : `class ${resp.test_prediction}`
                    : "—",
                color: "text-emerald-300",
              },
            ]}
          />
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

function BoundaryCard({ title, resp, loading, testPoint, onClick, k, task, testid, large }) {
  if (loading || !resp) {
    return (
      <div className="rounded-lg border border-neutral-800 bg-neutral-900/40 p-4">
        <div className="text-[11px] uppercase tracking-[0.18em] text-neutral-500 font-mono mb-2">{title}</div>
        <ChartSkeleton height={large ? 520 : 380} label="knn" />
      </div>
    );
  }

  const numClasses = Math.max(...resp.train_labels.map((l) => Math.round(l))) + 1;
  const palette = CLASS_COLORS.slice(0, Math.max(numClasses, 2));

  const isClassification = task === "classification";

  const meshTrace = isClassification
    ? {
        z: resp.mesh_zz,
        x: resp.mesh_xx[0],
        y: resp.mesh_yy.map((r) => r[0]),
        type: "heatmap",
        showscale: false,
        colorscale: palette.map((c, i, arr) => [i / (arr.length - 1 || 1), c]),
        opacity: 0.22,
        hoverinfo: "skip",
      }
    : {
        z: resp.mesh_zz,
        x: resp.mesh_xx[0],
        y: resp.mesh_yy.map((r) => r[0]),
        type: "heatmap",
        showscale: false,
        colorscale: [
          [0, "#0c4a6e"], [0.5, "#a3a3a3"], [1, "#fbbf24"],
        ],
        opacity: 0.35,
        hoverinfo: "skip",
      };

  // training points
  const traces = [meshTrace];
  if (isClassification) {
    for (let c = 0; c < numClasses; c++) {
      const xs = [], ys = [];
      resp.train_points.forEach((p, i) => {
        if (resp.train_labels[i] === c) {
          xs.push(p[0]); ys.push(p[1]);
        }
      });
      traces.push({
        x: xs, y: ys, type: "scatter", mode: "markers",
        name: `class ${c}`,
        marker: { color: palette[c], size: 8, line: { color: "#0a0a0a", width: 1 } },
      });
    }
  } else {
    traces.push({
      x: resp.train_points.map((p) => p[0]),
      y: resp.train_points.map((p) => p[1]),
      type: "scatter", mode: "markers",
      name: "data",
      marker: {
        color: resp.train_labels, colorscale: [[0, "#0c4a6e"], [1, "#fbbf24"]],
        size: 8, line: { color: "#0a0a0a", width: 1 },
      },
    });
  }

  // neighbor lines
  if (testPoint && resp.neighbor_indices?.length) {
    const xs = [], ys = [];
    resp.neighbor_indices.forEach((idx) => {
      xs.push(testPoint[0], resp.train_points[idx][0], null);
      ys.push(testPoint[1], resp.train_points[idx][1], null);
    });
    traces.push({
      x: xs, y: ys, type: "scatter", mode: "lines",
      line: { color: "#fbbf24", width: 1, dash: "dot" },
      hoverinfo: "skip",
      showlegend: false,
    });
    traces.push({
      x: [testPoint[0]], y: [testPoint[1]], type: "scatter", mode: "markers",
      name: "test point",
      marker: { color: "#f43f5e", size: 14, symbol: "x", line: { color: "#fff", width: 2 } },
    });
  }

  return (
    <div data-testid={testid} className="rounded-lg border border-neutral-800 bg-neutral-900/40 p-4">
      <div className="flex items-center justify-between mb-2">
        <div className="text-[11px] uppercase tracking-[0.18em] text-neutral-500 font-mono">{title}</div>
        <div className="text-[10px] font-mono text-neutral-500">K = {k}</div>
      </div>
      <div className={large ? "h-[520px]" : "h-[380px]"}>
        <PlotlyChart
          testid={`${testid}-plot`}
          data={traces}
          onClick={onClick}
          layout={{
            height: large ? 520 : 380,
            xaxis: { title: "x₁" },
            yaxis: { title: "x₂" },
            showlegend: true,
          }}
          config={{ displayModeBar: false }}
          style={{}}
        />
      </div>
    </div>
  );
}
