from fastapi import APIRouter
from app.models.schemas import GARequest, GAResponse
from app.services.ga_service import run_genetic_algorithm

router = APIRouter()


@router.post("/genetic_algorithm", response_model=GAResponse)
async def genetic_algorithm_endpoint(request: GARequest):
    """Run genetic algorithm with specified parameters."""
    result = run_genetic_algorithm(
        function=request.function,
        pop_size=request.pop_size,
        mutation_rate=request.mutation_rate,
        crossover_rate=request.crossover_rate,
        generations=request.generations,
        eta_m=request.eta_m,
        eta_c=request.eta_c
    )
    return result
