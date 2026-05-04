import Plot from "react-plotly.js";

export const darkLayout = {
  paper_bgcolor: "rgba(0,0,0,0)",
  plot_bgcolor: "rgba(0,0,0,0)",
  font: {
    family: "'IBM Plex Mono', ui-monospace, monospace",
    color: "#d4d4d4",
    size: 11,
  },
  margin: { l: 50, r: 20, t: 30, b: 40 },
  xaxis: {
    gridcolor: "rgba(255,255,255,0.06)",
    zerolinecolor: "rgba(255,255,255,0.12)",
    color: "#a3a3a3",
    linecolor: "rgba(255,255,255,0.12)",
  },
  yaxis: {
    gridcolor: "rgba(255,255,255,0.06)",
    zerolinecolor: "rgba(255,255,255,0.12)",
    color: "#a3a3a3",
    linecolor: "rgba(255,255,255,0.12)",
  },
  legend: {
    bgcolor: "rgba(20,20,22,0.85)",
    bordercolor: "rgba(255,255,255,0.08)",
    borderwidth: 1,
    font: { color: "#e5e5e5", size: 11 },
  },
  hoverlabel: {
    bgcolor: "#0a0a0a",
    bordercolor: "#404040",
    font: { color: "#fafafa", family: "'IBM Plex Mono', monospace" },
  },
};

export default function PlotlyChart({ data, layout, config, style, testid = "plotly-chart", onClick, onRelayout }) {
  return (
    <div data-testid={testid} className="w-full h-full">
      <Plot
        data={data}
        layout={{ ...darkLayout, ...(layout || {}) }}
        config={{ displayModeBar: false, responsive: true, ...(config || {}) }}
        useResizeHandler
        style={{ width: "100%", height: "100%", ...(style || {}) }}
        onClick={onClick}
        onRelayout={onRelayout}
      />
    </div>
  );
}
