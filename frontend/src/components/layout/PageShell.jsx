import Navbar from "@/components/layout/Navbar";
import TheoryDrawer from "@/components/shared/TheoryDrawer";
import { Toaster } from "@/components/ui/sonner";

export default function PageShell({ algorithm, children }) {
  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100 selection:bg-amber-300/30 selection:text-amber-50">
      <Navbar />
      {algorithm && <TheoryDrawer algorithm={algorithm} />}
      <Toaster theme="dark" position="top-right" />
      {children}
    </div>
  );
}
