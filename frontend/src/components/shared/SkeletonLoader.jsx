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
