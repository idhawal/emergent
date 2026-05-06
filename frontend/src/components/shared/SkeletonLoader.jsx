import { Skeleton } from "@/components/ui/skeleton";

export function ChartSkeleton({ height = 320, label = "chart" }) {
  return (
    <div
      data-testid={`skeleton-${label}`}
      className="w-full rounded-lg border border-neutral-800 bg-neutral-900/40 p-4"
      style={{ minHeight: height }}
    >
      <Skeleton className="h-4 w-32 bg-neutral-800 mb-3" />
      <Skeleton className="h-[calc(100%-1.5rem)] w-full bg-neutral-800/70 rounded" style={{ height: height - 40 }} />
    </div>
  );
}

export function MetricsSkeleton({ count = 4 }) {
  return (
    <div className="flex flex-wrap items-stretch gap-3">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="flex flex-col justify-center min-w-[120px] rounded-md border border-neutral-800 bg-neutral-900/60 px-3 py-2"
        >
          <Skeleton className="h-3 w-16 bg-neutral-700 mb-2" />
          <Skeleton className="h-5 w-24 bg-neutral-800" />
          <Skeleton className="h-2.5 w-12 bg-neutral-700 mt-2" />
        </div>
      ))}
    </div>
  );
}
