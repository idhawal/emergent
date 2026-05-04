import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetDescription } from "@/components/ui/sheet";
import { useUIStore } from "@/store/store";
import { BlockMath, InlineMath } from "react-katex";
import "katex/dist/katex.min.css";
import { ScrollArea } from "@/components/ui/scroll-area";

const CONTENT = {
  regression: {
    title: "Regression — Theory",
    description: "Linear, Polynomial, Ridge, Lasso & Elastic Net.",
    sections: [
      {
        h: "Model Explanation",
        body: (
          <p className="text-sm text-neutral-300 leading-relaxed">
            Regression models the relationship between input features and a continuous
            target. <span className="text-amber-300">Linear regression</span> learns a
            weight for each feature by minimizing squared error. Polynomial regression
            extends this with non-linear basis features. <span className="text-amber-300">Ridge</span>{" "}
            and <span className="text-amber-300">Lasso</span> add L2 / L1 penalties to
            constrain weights — Lasso drives some weights to exactly zero, performing
            implicit feature selection. <span className="text-amber-300">Elastic Net</span>{" "}
            blends both via the <code className="font-mono text-xs text-neutral-200">l1_ratio</code>.
          </p>
        ),
      },
      {
        h: "Mathematical Formulation",
        body: (
          <div className="space-y-3 text-sm text-neutral-200">
            <div>
              <div className="text-xs text-neutral-500 mb-1">Cost (MSE)</div>
              <BlockMath math={"J(\\theta) = \\frac{1}{2m}\\sum_{i=1}^{m}(h_\\theta(x_i)-y_i)^2"} />
            </div>
            <div>
              <div className="text-xs text-neutral-500 mb-1">Gradient Descent Update</div>
              <BlockMath math={"\\theta_j := \\theta_j - \\alpha\\,\\frac{\\partial J}{\\partial \\theta_j}"} />
            </div>
            <div>
              <div className="text-xs text-neutral-500 mb-1">Ridge / Lasso / Elastic Net</div>
              <BlockMath math={"J_{ridge}=J(\\theta)+\\lambda\\sum\\theta_j^2"} />
              <BlockMath math={"J_{lasso}=J(\\theta)+\\lambda\\sum|\\theta_j|"} />
              <BlockMath math={"J_{en}=J(\\theta)+\\lambda\\bigl[r\\sum|\\theta_j|+\\tfrac{1-r}{2}\\sum\\theta_j^2\\bigr]"} />
            </div>
          </div>
        ),
      },
      {
        h: "Parameter Guide",
        body: (
          <ul className="text-sm text-neutral-300 space-y-1.5">
            <li><span className="text-amber-300 font-mono">α (learning rate)</span> — step size for gradient descent.</li>
            <li><span className="text-amber-300 font-mono">epochs</span> — total optimization iterations.</li>
            <li><span className="text-amber-300 font-mono">poly_degree</span> — order of polynomial features.</li>
            <li><span className="text-amber-300 font-mono">λ (penalty)</span> — regularization strength.</li>
            <li><span className="text-amber-300 font-mono">l1_ratio</span> — Elastic Net L1 vs L2 mix.</li>
            <li><span className="text-amber-300 font-mono">noise</span> — synthetic dataset Gaussian noise.</li>
            <li><span className="text-amber-300 font-mono">early_stopping</span> — halt if cost rises 5x consecutively.</li>
          </ul>
        ),
      },
      {
        h: "Usage Instructions",
        body: (
          <ol className="text-sm text-neutral-300 space-y-1.5 list-decimal pl-4">
            <li>Pick an algorithm in the dropdown.</li>
            <li>Tune learning rate (log scale) and epochs.</li>
            <li>Toggle Early Stopping to see the amber alert when triggered.</li>
            <li>Slide λ on Lasso to watch coefficients snap to zero.</li>
          </ol>
        ),
      },
    ],
  },
  knn: {
    title: "K-Nearest Neighbors — Theory",
    description: "Distance-based classification and regression.",
    sections: [
      {
        h: "Model Explanation",
        body: (
          <p className="text-sm text-neutral-300 leading-relaxed">
            KNN is a non-parametric, instance-based learner. To predict a new point it
            finds the K closest training samples by a chosen distance metric and either
            votes (classification) or averages (regression) their targets. With
            distance-weighted voting, closer neighbors contribute more.
          </p>
        ),
      },
      {
        h: "Mathematical Formulation",
        body: (
          <div className="space-y-3 text-sm text-neutral-200">
            <div>
              <div className="text-xs text-neutral-500 mb-1">Euclidean</div>
              <BlockMath math={"d(x,y)=\\sqrt{\\sum_i (x_i-y_i)^2}"} />
            </div>
            <div>
              <div className="text-xs text-neutral-500 mb-1">Manhattan</div>
              <BlockMath math={"d(x,y)=\\sum_i |x_i-y_i|"} />
            </div>
            <div>
              <div className="text-xs text-neutral-500 mb-1">Distance-weighted vote</div>
              <BlockMath math={"\\hat y = \\arg\\max_c \\sum_{i\\in N_k} \\frac{\\mathbf{1}[y_i=c]}{d(x,x_i)+\\epsilon}"} />
            </div>
          </div>
        ),
      },
      {
        h: "Parameter Guide",
        body: (
          <ul className="text-sm text-neutral-300 space-y-1.5">
            <li><span className="text-amber-300 font-mono">K</span> — neighborhood size; small K = high variance.</li>
            <li><span className="text-amber-300 font-mono">metric</span> — Euclidean (L2) or Manhattan (L1).</li>
            <li><span className="text-amber-300 font-mono">weights</span> — uniform vs distance-weighted.</li>
            <li><span className="text-amber-300 font-mono">task</span> — classification (vote) vs regression (mean).</li>
          </ul>
        ),
      },
      {
        h: "Usage Instructions",
        body: (
          <ol className="text-sm text-neutral-300 space-y-1.5 list-decimal pl-4">
            <li>Pick a 2D dataset to populate the plot.</li>
            <li>Click anywhere on the boundary plot to drop a test point.</li>
            <li>The K nearest neighbors are connected with lines.</li>
            <li>Toggle Compare Mode to view Uniform vs Distance side-by-side.</li>
          </ol>
        ),
      },
    ],
  },
  "decision-tree": {
    title: "Decision Trees — Theory",
    description: "CART recursive splitting with Gini and Entropy.",
    sections: [
      {
        h: "Model Explanation",
        body: (
          <p className="text-sm text-neutral-300 leading-relaxed">
            A decision tree recursively partitions the feature space into axis-aligned
            regions. At each internal node the algorithm chooses the feature/threshold
            that maximizes purity gain. Pruning via depth or sample-count limits is the
            primary defense against overfitting.
          </p>
        ),
      },
      {
        h: "Mathematical Formulation",
        body: (
          <div className="space-y-3 text-sm text-neutral-200">
            <div>
              <div className="text-xs text-neutral-500 mb-1">Entropy</div>
              <BlockMath math={"\\mathrm{Info}(D) = -\\sum_i p_i \\log_2 p_i"} />
            </div>
            <div>
              <div className="text-xs text-neutral-500 mb-1">Information Gain</div>
              <BlockMath math={"\\mathrm{Gain}(A) = \\mathrm{Info}(D) - \\mathrm{Info}_A(D)"} />
            </div>
            <div>
              <div className="text-xs text-neutral-500 mb-1">Gini Impurity</div>
              <BlockMath math={"\\mathrm{Gini}(D) = 1 - \\sum_i p_i^2"} />
            </div>
          </div>
        ),
      },
      {
        h: "Parameter Guide",
        body: (
          <ul className="text-sm text-neutral-300 space-y-1.5">
            <li><span className="text-amber-300 font-mono">criterion</span> — Gini (faster) or Entropy (info-theoretic).</li>
            <li><span className="text-amber-300 font-mono">max_depth</span> — hard cap on tree depth, the main pruning lever.</li>
            <li><span className="text-amber-300 font-mono">min_samples_split</span> — minimum samples for an internal node.</li>
            <li><span className="text-amber-300 font-mono">min_samples_leaf</span> — minimum samples in each leaf.</li>
          </ul>
        ),
      },
      {
        h: "Usage Instructions",
        body: (
          <ol className="text-sm text-neutral-300 space-y-1.5 list-decimal pl-4">
            <li>Pick a classification dataset (Iris, Breast Cancer, Blobs).</li>
            <li>Drag <InlineMath math={"\\text{max\\_depth}"} /> to watch nodes fade out — pruning live.</li>
            <li>Toggle Compare Mode to render Gini vs Entropy trees side-by-side.</li>
          </ol>
        ),
      },
    ],
  },
  "genetic-algorithm": {
    title: "Genetic Algorithms — Theory",
    description: "Real-coded GA with SBX crossover & polynomial mutation.",
    sections: [
      {
        h: "Model Explanation",
        body: (
          <p className="text-sm text-neutral-300 leading-relaxed">
            Real-coded GAs evolve a population of candidate solutions in continuous
            space. Selection picks parents by fitness, Simulated Binary Crossover (SBX)
            combines them, and Polynomial Mutation perturbs offspring locally — both
            controlled by distribution indices ηc and ηm.
          </p>
        ),
      },
      {
        h: "Benchmarks",
        body: (
          <div className="space-y-3 text-sm text-neutral-200">
            <div>
              <div className="text-xs text-neutral-500 mb-1">Sphere</div>
              <BlockMath math={"f(x) = \\sum_i x_i^2"} />
            </div>
            <div>
              <div className="text-xs text-neutral-500 mb-1">Rosenbrock</div>
              <BlockMath math={"f(x,y)=(1-x)^2 + 100(y-x^2)^2"} />
            </div>
            <div>
              <div className="text-xs text-neutral-500 mb-1">Rastrigin</div>
              <BlockMath math={"f(x)=10n + \\sum_i [x_i^2 - 10\\cos(2\\pi x_i)]"} />
            </div>
          </div>
        ),
      },
      {
        h: "Parameter Guide",
        body: (
          <ul className="text-sm text-neutral-300 space-y-1.5">
            <li><span className="text-amber-300 font-mono">pop_size</span> — number of individuals per generation.</li>
            <li><span className="text-amber-300 font-mono">mutation_rate</span> — chance of polynomial mutation.</li>
            <li><span className="text-amber-300 font-mono">crossover_rate</span> — chance of SBX recombination.</li>
            <li><span className="text-amber-300 font-mono">ηc / ηm</span> — distribution indices controlling spread.</li>
          </ul>
        ),
      },
      {
        h: "Usage Instructions",
        body: (
          <ol className="text-sm text-neutral-300 space-y-1.5 list-decimal pl-4">
            <li>Choose a benchmark function.</li>
            <li>Press Play to animate population evolution.</li>
            <li>Switch functions to retain a ghost overlay of prior fitness curves.</li>
          </ol>
        ),
      },
    ],
  },
};

export default function TheoryDrawer({ algorithm }) {
  const open = useUIStore((s) => s.theoryOpen);
  const setOpen = useUIStore((s) => s.setTheoryOpen);
  const c = CONTENT[algorithm] || CONTENT.regression;
  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetContent
        side="right"
        data-testid="theory-drawer"
        className="w-full sm:max-w-xl bg-neutral-950 border-neutral-800 text-neutral-100"
      >
        <SheetHeader>
          <SheetTitle className="font-display text-2xl text-neutral-50 tracking-tight">
            {c.title}
          </SheetTitle>
          <SheetDescription className="text-neutral-400">{c.description}</SheetDescription>
        </SheetHeader>
        <ScrollArea className="h-[calc(100vh-7rem)] pr-3 mt-4">
          <div className="space-y-6 pb-10">
            {c.sections.map((s, i) => (
              <section key={i}>
                <h3 className="text-[11px] uppercase tracking-[0.18em] text-amber-300/80 font-mono mb-2">
                  {s.h}
                </h3>
                {s.body}
              </section>
            ))}
          </div>
        </ScrollArea>
      </SheetContent>
    </Sheet>
  );
}
