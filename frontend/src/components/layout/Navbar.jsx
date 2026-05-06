import { NavLink, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Info, FlaskConical, AlertCircle } from "lucide-react";
import { useUIStore } from "@/store/store";

const navItems = [
  { to: "/regression", label: "Regression", testid: "nav-regression" },
  { to: "/knn", label: "KNN", testid: "nav-knn" },
  { to: "/decision-tree", label: "Decision Trees", testid: "nav-decision-tree" },
  { to: "/genetic-algorithm", label: "Genetic Algorithms", testid: "nav-ga" },
];

const ALGO_ROUTES = ['/regression', '/knn', '/decision-tree', '/genetic-algorithm'];

export default function Navbar() {
  const setTheoryOpen = useUIStore((s) => s.setTheoryOpen);
  const hasSeenTheoryHint = useUIStore((s) => s.hasSeenTheoryHint);
  const setHasSeenTheoryHint = useUIStore((s) => s.setHasSeenTheoryHint);
  const location = useLocation();
  const showTheoryButton = ALGO_ROUTES.includes(location.pathname);
  
  return (
    <header
      data-testid="top-nav"
      className="sticky top-0 z-30 w-full border-b border-neutral-800 bg-neutral-950/95 backdrop-blur supports-[backdrop-filter]:bg-neutral-950/80"
    >
      <div className="flex h-14 items-center gap-2 px-4 md:px-6">
        <div className="flex items-center gap-2 mr-4 md:mr-8">
          <div className="grid place-items-center h-8 w-8 rounded-md bg-amber-400/15 text-amber-300 ring-1 ring-amber-400/30">
            <FlaskConical className="h-4 w-4" />
          </div>
          <div className="leading-tight">
            <div className="font-display text-[15px] tracking-tight text-neutral-50">
              ML Visualizer
            </div>
          </div>
        </div>

        <nav className="flex items-center gap-1 overflow-x-auto">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              data-testid={item.testid}
              className={({ isActive }) =>
                [
                  "px-3 py-1.5 rounded-md text-sm font-medium transition-colors whitespace-nowrap focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-neutral-950 focus-visible:ring-amber-400 focus-visible:outline-none",
                  isActive
                    ? "bg-amber-400/10 text-amber-200 ring-1 ring-amber-400/25"
                    : "text-neutral-300 hover:text-neutral-50 hover:bg-neutral-800/60",
                ].join(" ")
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="ml-auto flex items-center gap-2">
          {showTheoryButton && (
            <div className="relative">
              <Button
                data-testid="theory-button-global"
                variant="outline"
                size="sm"
                className="border-neutral-700 bg-neutral-900 text-neutral-200 hover:bg-neutral-800 hover:text-amber-200"
                onClick={() => {
                  setTheoryOpen(true);
                  setHasSeenTheoryHint(true);
                }}
              >
                <Info className="h-4 w-4 mr-1.5" />
                Theory
              </Button>
              {!hasSeenTheoryHint && (
                <div className="absolute top-0 right-0 -mr-1 -mt-1">
                  <div className="relative">
                    <div className="inline-flex items-center gap-1 bg-amber-400 text-neutral-950 px-2 py-1 rounded-md text-xs font-medium whitespace-nowrap">
                      <AlertCircle className="h-3 w-3" />
                      Learn theory
                    </div>
                    <div className="absolute bottom-full right-1/2 translate-x-1/2 mb-1 pointer-events-none">
                      <div className="bg-neutral-800 text-amber-200 text-xs px-2 py-1 rounded whitespace-nowrap border border-neutral-700">
                        Learn how this works
                        <div className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-neutral-800"></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
