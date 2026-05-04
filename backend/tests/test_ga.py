import pytest
from app.services.ga_service import run_genetic_algorithm, sphere, rosenbrock, rastrigin


def test_ga_fitness_decreases():
    """Best fitness in generation N ≤ best fitness in generation 1 for minimization."""
    result = run_genetic_algorithm(
        function="sphere",
        pop_size=20,
        mutation_rate=0.1,
        crossover_rate=0.8,
        generations=50,
        eta_m=20,
        eta_c=15
    )
    
    history = result["history"]
    first_fitness = history[0]["best_fitness"]
    last_fitness = history[-1]["best_fitness"]
    
    assert last_fitness <= first_fitness, "Best fitness should decrease or stay same over generations"


def test_benchmark_functions():
    """Test that benchmark functions work correctly."""
    import numpy as np
    
    # Sphere: minimum at [0, 0] should be 0
    assert abs(sphere(np.array([0.0, 0.0]))) < 1e-10
    assert sphere(np.array([1.0, 1.0])) > 0
    
    # Rosenbrock: minimum at [1, 1] should be 0
    assert abs(rosenbrock(np.array([1.0, 1.0]))) < 1e-10
    assert rosenbrock(np.array([0.0, 0.0])) > 0
    
    # Rastrigin: minimum at [0, 0] should be 0
    assert abs(rastrigin(np.array([0.0, 0.0]))) < 1e-10
    assert rastrigin(np.array([1.0, 1.0])) > 0


def test_ga_response_structure():
    """Test that GA response has all required fields."""
    result = run_genetic_algorithm(
        function="sphere",
        pop_size=30,
        mutation_rate=0.1,
        crossover_rate=0.8,
        generations=30,
        eta_m=20,
        eta_c=15
    )
    
    required_fields = ["contour_x", "contour_y", "contour_z", "history", "converged_at_generation"]
    for field in required_fields:
        assert field in result, f"Missing field: {field}"
    
    assert len(result["history"]) > 0, "History should not be empty"
    
    # Check history entry structure
    entry = result["history"][0]
    assert "generation" in entry
    assert "points" in entry
    assert "fitness_values" in entry
    assert "best_fitness" in entry
    assert "avg_fitness" in entry
    assert "best_point" in entry
