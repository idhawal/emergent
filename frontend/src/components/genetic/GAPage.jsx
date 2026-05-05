import { useEffect, useRef, useState } from "react";
import PageShell from "@/components/layout/PageShell";
import Sidebar from "@/components/layout/Sidebar";
import MetricsPanel from "@/components/layout/MetricsPanel";
import { ChartSkeleton } from "@/components/shared/SkeletonLoader";
import PlotlyChart from "@/components/shared/PlotlyChart";
import { Slider } from "@/components/ui/slider";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Pause, Play, SkipForward, RotateCcw } from "lucide-react";
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from "@/components/ui/select";
import { useDebounce } from "@/hooks/useDebounce";
import { useGAStore, useUIStore } from "@/store/store";
import { runGA } from "@/lib/api";

const FUNCTIONS = [
  { v: "sphere", label: "Sphere" },
  { v: "rosenbrock", label: "Rosenbrock" },
  { v: "rastrigin", label: "Rastrigin" },
];

export default function GAPage() {
  const s = useGAStore();
  const setTheoryOpen = useUIStore((u) => u.setTheoryOpen);
  const [resp, setResp] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isDemo, setIsDemo] = useState(false);
  const [genIdx, setGenIdx] = useState(0);
  const [playing, setPlaying] = useState(false);
  const playRef = useRef(null);
  const lastFn = useRef(s.function);

  const debouncedReq = useDebounce(
    {
      function: s.function,
      pop_size: s.pop_size,
      mutation_rate: s.mutation_rate,
      crossover_rate: s.crossover_rate,
      generations: s.generations,
      eta_m: s.eta_m,
      eta_c: s.eta_c,
    },
    300
  );

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setPlaying(false);
    setIsDemo(false);
    runGA(debouncedReq, controller.signal)
      .then(({ data, isDemo }) => {
        setResp(data);
        setIsDemo(isDemo);
        setGenIdx(0);
        setLoading(false);
      })
      .catch((err) => {
        if (err.name !== "AbortError") {
          console.error("Unexpected error:", err);
          setLoading(false);
        }
      });
    return () => { controller.abort(); };
  }, [debouncedReq]);

  // function change → save ghost
  useEffect(() => {
    if (lastFn.current !== s.function && resp) {
      // store last fitness history as ghost
      const prevHistory = resp.history.map((h) => ({ generation: h.generation, best_fitness: h.best_fitness, avg_fitness: h.avg_fitness }));
      s.set({ ghostHistory: { fn: lastFn.current, history: prevHistory } });
      lastFn.current = s.function;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [s.function]);

  // animation
  useEffect(() => {
    if (!playing) {
      if (playRef.current) clearInterval(playRef.current);
      return;
    }
    playRef.current = setInterval(() => {
      setGenIdx((g) => {
        if (!resp) return g;
        if (g >= resp.history.length - 1) {
          setPlaying(false);
          return g;
        }
        return g + 1;
      });
    }, 80);
    return () => clearInterval(playRef.current);
  }, [playing, resp]);

  const cur = resp?.history?.[genIdx];

  return (
    <PageShell algorithm="genetic-algorithm">
      <div className="flex flex-col lg:flex-row min-h-[calc(100vh-3.5rem)]">
        <Sidebar
          title="Genetic Algorithms"
          subtitle="Real-coded GA · SBX crossover + polynomial mutation"
          footer={
            <Button
              data-testid="reset-button"
              variant="outline"
              className="w-full border-neutral-700 bg-neutral-900 text-neutral-200 hover:bg-neutral-800"
              onClick={() => s.set({ ghostHistory: null })}
            >
              <RotateCcw className="h-4 w-4 mr-1.5" />
              Clear Ghost
            </Button>
          }
        >
          <Field label="Benchmark Function">
            <Select value={s.function} onValueChange={(v) => s.set({ function: v })}>
              <SelectTrigger data-testid="select-function" className="bg-neutral-900 border-neutral-700 text-neutral-100">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-neutral-900 border-neutral-700 text-neutral-100">
                {FUNCTIONS.map((f) => (
                  <SelectItem key={f.v} value={f.v}>{f.label}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </Field>

          <Field label="Population Size" value={s.pop_size}>
            <Slider data-testid="slider-pop-size" value={[s.pop_size]} min={10} max={200} step={2} onValueChange={(v) => s.set({ pop_size: v[0] })} />
          </Field>

          <Field label="Mutation Rate" value={s.mutation_rate.toFixed(2)}>
            <Slider data-testid="slider-mutation-rate" value={[s.mutation_rate]} min={0} max={1} step={0.01} onValueChange={(v) => s.set({ mutation_rate: +v[0].toFixed(2) })} />
          </Field>

          <Field label="Crossover Rate" value={s.crossover_rate.toFixed(2)}>
            <Slider data-testid="slider-crossover-rate" value={[s.crossover_rate]} min={0} max={1} step={0.01} onValueChange={(v) => s.set({ crossover_rate: +v[0].toFixed(2) })} />
          </Field>

          <Field label="Generations" hint="1 → 500">
            <Input
              data-testid="input-generations"
              type="number"
              min={1}
              max={500}
              value={s.generations}
              onChange={(e) => s.set({ generations: Math.max(1, Math.min(500, +e.target.value || 1)) })}
              className="bg-neutral-900 border-neutral-700 text-neutral-100"
            />
          </Field>

          <Field label="ηm (mutation index)" value={s.eta_m}>
            <Slider data-testid="slider-eta-m" value={[s.eta_m]} min={1} max={50} step={1} onValueChange={(v) => s.set({ eta_m: v[0] })} />
          </Field>

          <Field label="ηc (crossover index)" value={s.eta_c}>
            <Slider data-testid="slider-eta-c" value={[s.eta_c]} min={1} max={50} step={1} onValueChange={(v) => s.set({ eta_c: v[0] })} />
          </Field>

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
            <div className="grid gap-4 lg:grid-cols-5">
              <div className="lg:col-span-3 rounded-lg border border-neutral-800 bg-neutral-900/40 p-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="text-[11px] uppercase tracking-[0.18em] text-neutral-500 font-mono">
                    2D Contour + Population
                  </div>
                  <div className="text-[10px] font-mono text-neutral-500">
                    gen {cur?.generation ?? 0} / {resp?.history.length ?? 0}
                  </div>
                </div>
                <div className="h-[420px]">
                  {loading || !resp || !cur ? (
                    <ChartSkeleton height={420} label="contour" />
                  ) : (
                    <PlotlyChart
                      testid="plot-contour"
                      data={[
                        {
                          z: resp.contour_z,
                          x: resp.contour_x[0],
                          y: resp.contour_y.map((r) => r[0]),
                          type: "contour",
                          colorscale: "Viridis",
                          opacity: 0.85,
                          contours: { coloring: "heatmap", showlabels: false },
                          showscale: false,
                        },
                        {
                          x: cur.points.map((p) => p[0]),
                          y: cur.points.map((p) => p[1]),
                          mode: "markers",
                          type: "scatter",
                          name: "Population",
                          marker: {
                            color: cur.fitness_values,
                            colorscale: [[0, "#fbbf24"], [1, "#f43f5e"]],
                            size: 8,
                            line: { color: "#0a0a0a", width: 1 },
                            showscale: false,
                          },
                        },
                        {
                          x: [cur.best_point[0]],
                          y: [cur.best_point[1]],
                          mode: "markers",
                          type: "scatter",
                          name: "Best",
                          marker: { color: "#34d399", size: 14, symbol: "star", line: { color: "#fff", width: 1 } },
                        },
                      ]}
                      layout={{
                        height: 420,
                        xaxis: { title: "x", range: [-resp.span, resp.span] },
                        yaxis: { title: "y", range: [-resp.span, resp.span] },
                      }}
                    />
                  )}
                </div>
                <div className="mt-3 flex items-center gap-2">
                  <Button
                    data-testid="btn-play-pause"
                    size="sm"
                    className="bg-amber-400 hover:bg-amber-300 text-neutral-950"
                    onClick={() => setPlaying((p) => !p)}
                  >
                    {playing ? <Pause className="h-4 w-4 mr-1.5" /> : <Play className="h-4 w-4 mr-1.5" />}
                    {playing ? "Pause" : "Play"}
                  </Button>
                  <Button
                    data-testid="btn-step"
                    size="sm"
                    variant="outline"
                    className="border-neutral-700 bg-neutral-900 text-neutral-200 hover:bg-neutral-800"
                    onClick={() => setGenIdx((g) => Math.min((resp?.history.length || 1) - 1, g + 1))}
                  >
                    <SkipForward className="h-4 w-4 mr-1.5" /> Step
                  </Button>
                  <div className="flex-1 px-3">
                    <Slider
                      data-testid="slider-generation"
                      value={[genIdx]}
                      min={0}
                      max={Math.max(0, (resp?.history.length || 1) - 1)}
                      step={1}
                      onValueChange={(v) => setGenIdx(v[0])}
                    />
                  </div>
                </div>
              </div>

              <div className="lg:col-span-2 rounded-lg border border-neutral-800 bg-neutral-900/40 p-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="text-[11px] uppercase tracking-[0.18em] text-neutral-500 font-mono">
                    Fitness vs Generations
                  </div>
                </div>
                <div className="h-[420px]">
                  {loading || !resp ? (
                    <ChartSkeleton height={420} label="fitness" />
                  ) : (
                    <PlotlyChart
                      testid="plot-fitness"
                      data={[
                        {
                          x: resp.history.map((h) => h.generation),
                          y: resp.history.map((h) => h.best_fitness),
                          type: "scatter",
                          mode: "lines",
                          name: "Best",
                          line: { color: "#34d399", width: 2 },
                        },
                        {
                          x: resp.history.map((h) => h.generation),
                          y: resp.history.map((h) => h.avg_fitness),
                          type: "scatter",
                          mode: "lines",
                          name: "Average",
                          line: { color: "#fbbf24", width: 2, dash: "dot" },
                        },
                        ...(s.ghostHistory
                          ? [
                              {
                                x: s.ghostHistory.history.map((h) => h.generation),
                                y: s.ghostHistory.history.map((h) => h.best_fitness),
                                type: "scatter",
                                mode: "lines",
                                name: `Ghost · ${s.ghostHistory.fn}`,
                                line: { color: "#a3a3a3", width: 1.5, dash: "dash" },
                                opacity: 0.6,
                              },
                            ]
                          : []),
                      ]}
                      layout={{
                        height: 420,
                        xaxis: { title: "Generation" },
                        yaxis: { title: "Fitness", type: "log" },
                      }}
                    />
                  )}
                </div>
              </div>
            </div>

            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4" data-testid="convergence-cards">
              <CompareCard label="Best Fitness" value={cur ? cur.best_fitness.toExponential(3) : "—"} accent="text-emerald-300" />
              <CompareCard label="Avg Fitness" value={cur ? cur.avg_fitness.toExponential(3) : "—"} accent="text-amber-200" />
              <CompareCard
                label="Converged @ Gen"
                value={resp?.converged_at_generation ?? "—"}
                sub={resp?.converged_at_generation ? "fitness < threshold" : "did not converge"}
              />
              <CompareCard
                label="Best Point"
                value={cur ? `(${cur.best_point[0].toFixed(2)}, ${cur.best_point[1].toFixed(2)})` : "—"}
                accent="text-neutral-100"
              />
            </div>
          </div>

          <MetricsPanel
            items={[
              { label: "Function", value: s.function, color: "text-amber-200" },
              { label: "Population", value: s.pop_size },
              { label: "Generations", value: s.generations },
              { label: "Mutation", value: s.mutation_rate.toFixed(2) },
              { label: "Crossover", value: s.crossover_rate.toFixed(2) },
              { label: "ηm / ηc", value: `${s.eta_m} / ${s.eta_c}` },
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

function CompareCard({ label, value, sub, accent = "text-neutral-100" }) {
  return (
    <div
      data-testid={`card-${label.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}
      className="rounded-lg border border-neutral-800 bg-neutral-900/40 px-4 py-3"
    >
      <div className="text-[10px] uppercase tracking-[0.18em] text-neutral-500 font-mono">{label}</div>
      <div className={`text-lg font-mono mt-1 ${accent}`}>{value}</div>
      {sub && <div className="text-[11px] text-neutral-500 mt-0.5">{sub}</div>}
    </div>
  );
}
