import { useEffect, useMemo, useState } from "react";
import PageShell from "@/components/layout/PageShell";
import Sidebar from "@/components/layout/Sidebar";
import MetricsPanel from "@/components/layout/MetricsPanel";
import { ChartSkeleton } from "@/components/shared/SkeletonLoader";
import PlotlyChart from "@/components/shared/PlotlyChart";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AlertTriangle, RotateCcw, Play } from "lucide-react";
import { useDebounce } from "@/hooks/useDebounce";
import { useRegressionStore, useUIStore } from "@/store/store";
import { runRegression } from "@/lib/api";
import DatasetSelector from "@/components/shared/DatasetSelector";

const ALGOS = [
  { v: "linear_gd", label: "Linear (Gradient Descent)" },
  { v: "polynomial", label: "Polynomial" },
  { v: "ridge", label: "Ridge" },
  { v: "lasso", label: "Lasso" },
  { v: "elastic_net", label: "Elastic Net" },
];
const PENALTIES = [0.01, 0.1, 1, 10, 100];
const REGRESSION_DATASETS = ["linear", "sine", "quadratic"];

// log slider helpers (0.0001..1.0 → 0..1)
const lrToSlider = (lr) => {
  const lo = Math.log10(0.0001), hi = Math.log10(1);
  return ((Math.log10(lr) - lo) / (hi - lo)) * 100;
};
const sliderToLr = (s) => {
  const lo = Math.log10(0.0001), hi = Math.log10(1);
  return Math.pow(10, lo + (s / 100) * (hi - lo));
};

export default function RegressionPage() {
  const s = useRegressionStore();
  const setTheoryOpen = useUIStore((u) => u.setTheoryOpen);

  const [resp, setResp] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isDemo, setIsDemo] = useState(false);
  const [reqId, setReqId] = useState(0);

  const debouncedReq = useDebounce(
    {
      algo: s.algo,
      learning_rate: s.learning_rate,
      epochs: s.epochs,
      poly_degree: s.poly_degree,
      penalty: s.penalty,
      l1_ratio: s.l1_ratio,
      noise: s.noise,
      early_stopping: s.early_stopping,
      dataset: s.dataset,
      uploaded_data: s.uploadedDataset ? s.uploadedDataset.rows : null,
    },
    300
  );

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setIsDemo(false);
    runRegression(debouncedReq, controller.signal)
      .then(({ data, isDemo }) => {
        setResp(data);
        setIsDemo(isDemo);
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
  }, [debouncedReq, reqId]);

  const zeroedCount = useMemo(() => {
    if (!resp) return 0;
    return resp.coefficients.filter((c) => Math.abs(c) < 1e-6).length;
  }, [resp]);

  const showLasso = s.algo === "lasso" || s.algo === "elastic_net";

  return (
    <PageShell algorithm="regression">
      <div className="flex flex-col lg:flex-row min-h-[calc(100vh-3.5rem)]">
        <Sidebar
          title="Regression"
          subtitle="Linear, Polynomial, Ridge, Lasso, Elastic Net"
          footer={
            <div className="flex gap-2">
              <Button
                data-testid="run-button"
                className="flex-1 bg-amber-400 hover:bg-amber-300 text-neutral-950"
                onClick={() => setReqId((x) => x + 1)}
              >
                <Play className="h-4 w-4 mr-1.5" />
                Run
              </Button>
              <Button
                data-testid="reset-button"
                variant="outline"
                className="border-neutral-700 bg-neutral-900 text-neutral-200 hover:bg-neutral-800"
                onClick={() =>
                  s.set({
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
                  })
                }
              >
                <RotateCcw className="h-4 w-4" />
              </Button>
            </div>
          }
        >
          <Field label="Dataset">
            <DatasetSelector
              availableDatasets={REGRESSION_DATASETS}
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

          {/* Algorithm */}
          <Field label="Algorithm">
            <Select value={s.algo} onValueChange={(v) => s.set({ algo: v })}>
              <SelectTrigger data-testid="select-algo" className="bg-neutral-900 border-neutral-700 text-neutral-100">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-neutral-900 border-neutral-700 text-neutral-100">
                {ALGOS.map((a) => (
                  <SelectItem key={a.v} value={a.v}>{a.label}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </Field>

          {/* Learning Rate (log) */}
          <Field
            label={`Learning Rate (α)`}
            value={s.learning_rate.toExponential(2)}
            hint="0.0001 → 1.0 (log)"
          >
            <Slider
              data-testid="slider-learning-rate"
              value={[lrToSlider(s.learning_rate)]}
              min={0}
              max={100}
              step={1}
              onValueChange={(v) => s.set({ learning_rate: +sliderToLr(v[0]).toFixed(5) })}
            />
          </Field>

          {/* Epochs */}
          <Field label="Epochs / Iterations" hint="1 → 10 000">
            <Input
              data-testid="input-epochs"
              type="number"
              min={1}
              max={10000}
              value={s.epochs}
              onChange={(e) => s.set({ epochs: Math.max(1, Math.min(10000, +e.target.value || 1)) })}
              className="bg-neutral-900 border-neutral-700 text-neutral-100"
            />
          </Field>

          {/* Poly degree */}
          <Field label="Polynomial Degree" value={s.poly_degree}>
            <Slider
              data-testid="slider-poly-degree"
              value={[s.poly_degree]}
              min={1}
              max={4}
              step={1}
              onValueChange={(v) => s.set({ poly_degree: v[0] })}
            />
          </Field>

          {/* Penalty */}
          <Field label="Regularization Penalty (λ)">
            <Select value={String(s.penalty)} onValueChange={(v) => s.set({ penalty: +v })}>
              <SelectTrigger data-testid="select-penalty" className="bg-neutral-900 border-neutral-700 text-neutral-100">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-neutral-900 border-neutral-700 text-neutral-100">
                {PENALTIES.map((p) => (
                  <SelectItem key={p} value={String(p)}>{p}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </Field>

          {/* l1_ratio (only Elastic Net) */}
          {s.algo === "elastic_net" && (
            <Field label="l1_ratio" value={s.l1_ratio}>
              <Slider
                data-testid="slider-l1-ratio"
                value={[s.l1_ratio]}
                min={0.2}
                max={0.8}
                step={0.3}
                onValueChange={(v) => s.set({ l1_ratio: v[0] })}
              />
            </Field>
          )}

          {/* Noise */}
          <Field label="Noise Level" value={s.noise.toFixed(2)} hint="0.0 → 1.0">
            <Slider
              data-testid="slider-noise"
              value={[s.noise]}
              min={0}
              max={1}
              step={0.01}
              onValueChange={(v) => s.set({ noise: +v[0].toFixed(2) })}
            />
          </Field>

          {/* Early stopping */}
          <div className="flex items-center justify-between">
            <Label className="text-sm text-neutral-200">Early Stopping</Label>
            <Switch
              data-testid="switch-early-stopping"
              checked={s.early_stopping}
              onCheckedChange={(v) => s.set({ early_stopping: v })}
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
            {resp?.stopped_at_epoch != null && (
              <Alert
                data-testid="early-stop-banner"
                className="bg-amber-400/10 border-amber-400/30 text-amber-100"
              >
                <AlertTriangle className="h-4 w-4 !text-amber-300" />
                <AlertTitle className="text-amber-200">Early stopping triggered</AlertTitle>
                <AlertDescription className="text-amber-100/80">
                  Cost increased for 5 consecutive iterations. Halted at epoch {resp.stopped_at_epoch}.
                </AlertDescription>
              </Alert>
            )}

            <div className="grid gap-4 lg:grid-cols-2">
              <ChartCard title="Scatter + Fit" testid="chart-scatter-fit">
                {loading ? (
                  <ChartSkeleton label="scatter" />
                ) : (
                  <PlotlyChart
                    testid="plot-scatter-fit"
                    data={[
                      {
                        x: resp.scatter_x,
                        y: resp.scatter_y,
                        mode: "markers",
                        type: "scatter",
                        name: "Data",
                        marker: { color: "#a3a3a3", size: 6, opacity: 0.7 },
                      },
                      {
                        x: resp.curve_x,
                        y: resp.curve_y,
                        mode: "lines",
                        type: "scatter",
                        name: "Fit",
                        line: { color: "#fbbf24", width: 3 },
                      },
                    ]}
                    layout={{ height: 320, xaxis: { title: "x" }, yaxis: { title: "y" } }}
                  />
                )}
              </ChartCard>

              <ChartCard title="Cost vs Iterations" testid="chart-cost">
                {loading ? (
                  <ChartSkeleton label="cost" />
                ) : (
                  <PlotlyChart
                    testid="plot-cost"
                    data={[
                      {
                        y: resp.cost_history,
                        mode: "lines",
                        type: "scatter",
                        name: "Cost J(θ)",
                        line: { color: "#34d399", width: 2 },
                        fill: "tozeroy",
                        fillcolor: "rgba(52,211,153,0.08)",
                      },
                    ]}
                    layout={{
                      height: 320,
                      xaxis: { title: "Iteration" },
                      yaxis: { title: "Cost", type: "log" },
                    }}
                  />
                )}
              </ChartCard>
            </div>

            <ChartCard
              title={`Coefficient Bar Chart${showLasso ? ` — ${zeroedCount} of ${resp?.coefficients.length || 0} features zeroed out` : ""}`}
              testid="chart-coefficients"
            >
              {loading ? (
                <ChartSkeleton label="coeff" height={260} />
              ) : (
                <PlotlyChart
                  testid="plot-coefficients"
                  data={[
                    {
                      x: resp.feature_names,
                      y: resp.coefficients,
                      type: "bar",
                      marker: {
                        color: resp.coefficients.map((c) =>
                          Math.abs(c) < 1e-6 ? "#f43f5e" : "#fbbf24"
                        ),
                      },
                      text: resp.coefficients.map((c) => c.toFixed(3)),
                      textposition: "outside",
                    },
                  ]}
                  layout={{
                    height: 260,
                    xaxis: { title: "Feature" },
                    yaxis: { title: "Weight" },
                    transition: { duration: 500, easing: "cubic-in-out" },
                  }}
                />
              )}
            </ChartCard>
          </div>

          <MetricsPanel
            items={[
              { label: "Algorithm", value: ALGOS.find((a) => a.v === s.algo)?.label.split(" ")[0] || s.algo },
              { label: "Final Cost", value: loading ? "—" : resp.cost_history[resp.cost_history.length - 1].toExponential(2) },
              { label: "Iterations", value: loading ? "—" : resp.cost_history.length, color: "text-amber-200" },
              { label: "Stopped At", value: resp?.stopped_at_epoch ?? "—" },
              { label: "Zeroed Coefs", value: showLasso ? `${zeroedCount}/${resp?.coefficients.length || 0}` : "—", color: showLasso ? "text-rose-300" : "text-neutral-500" },
            ]}
            isLoading={loading}
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
        {value !== undefined && (
          <span className="text-xs font-mono text-amber-300">{value}</span>
        )}
      </div>
      {children}
      {hint && <div className="text-[10px] text-neutral-500 font-mono">{hint}</div>}
    </div>
  );
}

function ChartCard({ title, children, testid }) {
  return (
    <div data-testid={testid} className="rounded-lg border border-neutral-800 bg-neutral-900/40 p-4">
      <div className="flex items-center justify-between mb-2">
        <div className="text-[11px] uppercase tracking-[0.18em] text-neutral-500 font-mono">{title}</div>
      </div>
      <div className="h-[260px] md:h-[320px]">{children}</div>
    </div>
  );
}
