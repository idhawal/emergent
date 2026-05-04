import numpy as np
from typing import List, Tuple, Optional


def sphere(x: np.ndarray) -> float:
    """Sphere function: f(x) = sum(x_i^2)"""
    return np.sum(x ** 2)


def rosenbrock(x: np.ndarray) -> float:
    """Rosenbrock function: f(x,y) = (1-x)^2 + 100(y-x^2)^2"""
    return (1 - x[0]) ** 2 + 100 * (x[1] - x[0] ** 2) ** 2


def rastrigin(x: np.ndarray) -> float:
    """Rastrigin function: f(x) = 10n + sum(x_i^2 - 10*cos(2*pi*x_i))"""
    n = len(x)
    return 10 * n + np.sum(x ** 2 - 10 * np.cos(2 * np.pi * x))


def get_benchmark_function(name: str):
    """Get benchmark function by name."""
    functions = {
        "sphere": sphere,
        "rosenbrock": rosenbrock,
        "rastrigin": rastrigin
    }
    if name not in functions:
        raise ValueError(f"Unknown function: {name}")
    return functions[name]


def tournament_selection(population: np.ndarray, fitness: np.ndarray, tournament_size: int = 3) -> np.ndarray:
    """Tournament selection."""
    idx = np.random.choice(len(population), tournament_size, replace=False)
    best_idx = idx[np.argmin(fitness[idx])]
    return population[best_idx].copy()


def sbx_crossover(parent1: np.ndarray, parent2: np.ndarray, eta_c: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Simulated Binary Crossover (SBX).
    Returns two offspring.
    """
    offspring1 = parent1.copy()
    offspring2 = parent2.copy()
    
    for i in range(len(parent1)):
        if np.random.random() <= 0.5:
            if abs(parent1[i] - parent2[i]) > 1e-14:
                beta = 1.0
                u = np.random.random()
                
                if u <= 0.5:
                    beta = (2 * u) ** (1 / (eta_c + 1))
                else:
                    beta = (1 / (2 * (1 - u))) ** (1 / (eta_c + 1))
                
                offspring1[i] = 0.5 * ((1 + beta) * parent1[i] + (1 - beta) * parent2[i])
                offspring2[i] = 0.5 * ((1 - beta) * parent1[i] + (1 + beta) * parent2[i])
    
    return offspring1, offspring2


def polynomial_mutation(individual: np.ndarray, eta_m: float, bounds: Tuple[float, float]) -> np.ndarray:
    """
    Polynomial mutation.
    Returns mutated individual.
    """
    mutated = individual.copy()
    lower, upper = bounds
    
    for i in range(len(individual)):
        if np.random.random() <= 1.0 / len(individual):
            delta = 0.0
            u = np.random.random()
            
            if u <= 0.5:
                delta = (2 * u) ** (1 / (eta_m + 1)) - 1
            else:
                delta = 1 - (2 * (1 - u)) ** (1 / (eta_m + 1))
            
            mutated[i] = individual[i] + delta * (upper - lower)
            mutated[i] = np.clip(mutated[i], lower, upper)
    
    return mutated


def generate_contour(function_name: str, span: float, grid_size: int = 60) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate contour grid for visualization."""
    func = get_benchmark_function(function_name)
    
    x = np.linspace(-span, span, grid_size)
    y = np.linspace(-span, span, grid_size)
    xx, yy = np.meshgrid(x, y)
    
    zz = np.zeros_like(xx)
    for i in range(grid_size):
        for j in range(grid_size):
            zz[i, j] = func(np.array([xx[i, j], yy[i, j]]))
    
    return xx, yy, zz


def run_genetic_algorithm(
    function: str,
    pop_size: int,
    mutation_rate: float,
    crossover_rate: float,
    generations: int,
    eta_m: float,
    eta_c: float
) -> dict:
    """Run genetic algorithm with SBX crossover and polynomial mutation."""
    
    # Get benchmark function
    func = get_benchmark_function(function)
    
    # Set search space bounds
    span = 2.5 if function == "rosenbrock" else 5.0
    bounds = (-span, span)
    
    # Generate contour grid
    contour_x, contour_y, contour_z = generate_contour(function, span)
    
    # Initialize population
    population = np.random.uniform(bounds[0], bounds[1], (pop_size, 2))
    
    # Store history
    history = []
    converged_at_generation = None
    best_fitness_ever = float('inf')
    
    for gen in range(generations):
        # Evaluate fitness
        fitness = np.array([func(ind) for ind in population])
        
        # Track best
        best_idx = np.argmin(fitness)
        best_fitness = fitness[best_idx]
        avg_fitness = np.mean(fitness)
        
        if best_fitness < best_fitness_ever:
            best_fitness_ever = best_fitness
        
        # Check convergence
        if converged_at_generation is None and best_fitness < 0.05:
            converged_at_generation = gen + 1
        
        # Store history
        history.append({
            "generation": gen + 1,
            "points": population.tolist(),
            "fitness_values": fitness.tolist(),
            "best_fitness": float(best_fitness),
            "avg_fitness": float(avg_fitness),
            "best_point": population[best_idx].tolist()
        })
        
        # Create new population
        new_population = []
        
        while len(new_population) < pop_size:
            # Selection
            parent1 = tournament_selection(population, fitness)
            parent2 = tournament_selection(population, fitness)
            
            # Crossover
            if np.random.random() < crossover_rate:
                child1, child2 = sbx_crossover(parent1, parent2, eta_c)
            else:
                child1, child2 = parent1.copy(), parent2.copy()
            
            # Mutation
            if np.random.random() < mutation_rate:
                child1 = polynomial_mutation(child1, eta_m, bounds)
            if np.random.random() < mutation_rate:
                child2 = polynomial_mutation(child2, eta_m, bounds)
            
            new_population.extend([child1, child2])
        
        # Trim to exact population size
        population = np.array(new_population[:pop_size])
    
    return {
        "contour_x": contour_x.tolist(),
        "contour_y": contour_y.tolist(),
        "contour_z": contour_z.tolist(),
        "history": history,
        "converged_at_generation": converged_at_generation
    }
