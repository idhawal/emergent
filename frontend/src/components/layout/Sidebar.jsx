export default function Sidebar({ title, subtitle, children, footer }) {
  return (
    <aside
      data-testid="control-panel"
      className="w-full lg:w-[340px] xl:w-[360px] shrink-0 border-r border-neutral-800 bg-neutral-950/60"
    >
      <div className="px-5 py-4 border-b border-neutral-800">
        <div className="text-[11px] uppercase tracking-[0.18em] text-amber-300/80 font-mono">
          Control Panel
        </div>
        <h2 className="font-display text-xl text-neutral-50 tracking-tight mt-0.5">
          {title}
        </h2>
        {subtitle && (
          <p className="text-xs text-neutral-400 mt-1 leading-relaxed">{subtitle}</p>
        )}
      </div>
      <div className="p-5 space-y-5 overflow-y-auto max-h-[calc(100vh-200px)]">
        {children}
      </div>
      {footer && (
        <div className="px-5 py-4 border-t border-neutral-800 sticky bottom-0 bg-neutral-950/95">
          {footer}
        </div>
      )}
    </aside>
  );
}
