import Navbar from "@/components/layout/Navbar";
import TheoryDrawer from "@/components/shared/TheoryDrawer";
import { Toaster } from "@/components/ui/sonner";

export default function PageShell({ algorithm, children }) {
  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100 selection:bg-amber-300/30 selection:text-amber-50">
      <a href="#main-content" className="sr-only focus:not-sr-only focus:fixed focus:top-0 focus:left-0 focus:z-50 focus:bg-amber-400 focus:text-neutral-950 focus:px-4 focus:py-2 focus:font-bold focus:rounded-md focus:ring-2 focus:ring-offset-2 focus:ring-amber-300">
        Skip to main content
      </a>
      <Navbar />
      {algorithm && <TheoryDrawer algorithm={algorithm} />}
      <Toaster theme="dark" position="top-right" />
      <main id="main-content">
        {children}
      </main>
    </div>
  );
}
