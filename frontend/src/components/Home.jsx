import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  ChartLine, Network, GitBranch, Dna, ArrowRight, Sparkles,
} from "lucide-react";
import PageShell from "@/components/layout/PageShell";

const CARDS = [
  {
    to: "/regression",
    icon: ChartLine,
    title: "Regression",
    desc: "Linear, Polynomial, Ridge, Lasso & Elastic Net with live gradient descent and early stopping.",
    accent: "amber",
    testid: "card-regression",
  },
  {
    to: "/knn",
    icon: Network,
    title: "K-Nearest Neighbors",
    desc: "Interactive 2D decision boundaries. Click to drop a test point — see neighbors light up.",
    accent: "emerald",
    testid: "card-knn",
  },
  {
    to: "/decision-tree",
    icon: GitBranch,
    title: "Decision Trees",
    desc: "Pan-and-zoom node-link diagrams. Live pruning. Side-by-side Gini vs Entropy.",
    accent: "sky",
    testid: "card-decision-tree",
  },
  {
    to: "/genetic-algorithm",
    icon: Dna,
    title: "Genetic Algorithms",
    desc: "Real-coded GA on Sphere, Rosenbrock & Rastrigin. Watch populations converge generation by generation.",
    accent: "rose",
    testid: "card-ga",
  },
];

const accentMap = {
  amber: "ring-amber-400/30 hover:ring-amber-400/60 text-amber-300 bg-amber-400/10",
  emerald: "ring-emerald-400/30 hover:ring-emerald-400/60 text-emerald-300 bg-emerald-400/10",
  sky: "ring-sky-400/30 hover:ring-sky-400/60 text-sky-300 bg-sky-400/10",
  rose: "ring-rose-400/30 hover:ring-rose-400/60 text-rose-300 bg-rose-400/10",
};

export default function Home() {
  return (
    <PageShell algorithm="regression">
      <main className="px-4 md:px-6 py-10 md:py-16 max-w-6xl mx-auto">
        <div className="flex items-center gap-2 text-amber-300 text-xs font-mono mb-4 uppercase tracking-[0.2em]">
          <Sparkles className="h-3.5 w-3.5" />
          Interactive Lab
        </div>
        <h1 className="font-display text-4xl sm:text-5xl lg:text-6xl tracking-tight text-neutral-50 leading-[1.05]">
          Visualize, tune, and reason about
          <br />
          <span className="text-amber-300">four families of ML algorithms.</span>
        </h1>
        <p className="text-neutral-400 mt-5 max-w-2xl text-base leading-relaxed">
          A single-source-of-truth GUI —
          Regression · KNN · Decision Trees · Genetic Algorithms. Every page is
          paired with a Theory drawer of equations and parameter guides.
        </p>

        <div className="mt-10 grid gap-4 md:gap-5 sm:grid-cols-2">
          {CARDS.map((c) => {
            const Icon = c.icon;
            return (
              <Link
                key={c.to}
                to={c.to}
                data-testid={c.testid}
                className="group rounded-2xl border border-neutral-800 bg-neutral-900/40 p-6 transition-all hover:bg-neutral-900/70 hover:-translate-y-0.5"
              >
                <div className={`inline-flex items-center justify-center h-10 w-10 rounded-lg ring-1 ${accentMap[c.accent]}`}>
                  <Icon className="h-5 w-5" />
                </div>
                <h3 className="mt-4 font-display text-2xl text-neutral-50 tracking-tight">{c.title}</h3>
                <p className="text-sm text-neutral-400 mt-2 leading-relaxed">{c.desc}</p>
                <div className="flex items-center gap-1.5 text-amber-300 text-xs font-mono mt-4 uppercase tracking-[0.18em]">
                  Open
                  <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-1" />
                </div>
              </Link>
            );
          })}
        </div>

        <div className="mt-16 rounded-2xl border border-neutral-800 bg-neutral-900/40 p-6 md:p-8">
          <div className="grid gap-6 md:grid-cols-3">
            <Stat label="Algorithms" value="4 families" />
            <Stat label="Adjustable Parameters" value="30+" />
            <Stat label="Charts" value="Plotly · react-d3-tree" />
          </div>
        </div>

        <div className="mt-10 flex flex-wrap gap-3">
          <Link to="/regression">
            <Button data-testid="btn-start" className="bg-amber-400 hover:bg-amber-300 text-neutral-950">
              Start with Regression <ArrowRight className="h-4 w-4 ml-1.5" />
            </Button>
          </Link>
        </div>
      </main>
    </PageShell>
  );
}

function Stat({ label, value }) {
  return (
    <div>
      <div className="text-[10px] uppercase tracking-[0.18em] text-neutral-500 font-mono">{label}</div>
      <div className="font-display text-2xl text-neutral-50 mt-1">{value}</div>
    </div>
  );
}
