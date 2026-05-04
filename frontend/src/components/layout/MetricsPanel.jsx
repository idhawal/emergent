export default function MetricsPanel({ items = [], children, dataTestId = "metrics-panel" }) {
  return (
    <div
      data-testid={dataTestId}
      className="border-t border-neutral-800 bg-neutral-950/70 px-4 md:px-6 py-3"
    >
      <div className="flex flex-wrap items-stretch gap-3">
        {items.map((m, i) => (
          <div
            key={i}
            data-testid={`metric-${(m.label || "x").toLowerCase().replace(/\s+/g, "-")}`}
            className="flex flex-col justify-center min-w-[120px] rounded-md border border-neutral-800 bg-neutral-900/60 px-3 py-2"
          >
            <div className="text-[10px] uppercase tracking-[0.16em] text-neutral-500 font-mono">
              {m.label}
            </div>
            <div className={`mt-0.5 text-base font-mono ${m.color || "text-neutral-100"}`}>
              {m.value}
            </div>
            {m.sub && (
              <div className="text-[11px] text-neutral-500 mt-0.5">{m.sub}</div>
            )}
          </div>
        ))}
        {children}
      </div>
    </div>
  );
}
