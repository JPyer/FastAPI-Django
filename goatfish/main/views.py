from django.shortcuts import render

# Create your views here.
from fastapi import Body
from fastapi import Depends

from .models import APISimulation
from .models import APISimulations
from .models import DamnFastAPISimulation
from .models import Simulation
from .models import User
from .utils import get_simulation
from .utils import get_user


def simulations_get(user: User = Depends(get_user)) -> APISimulations:
    """
    Return a list of available simulations.
    """
    simulations = user.simulation_set.all()
    api_simulations = [APISimulation.from_model(s) for s in simulations]
    return APISimulations(items=api_simulations)


def simulation_post(
    simulation: DamnFastAPISimulation,
    user: User = Depends(get_user)
) -> APISimulation:
    """
    Create a new simulation.
    """
    s = Simulation.from_api(user, simulation)
    s.save()
    return APISimulation.from_model(s)


def simulation_get(
    simulation: Simulation = Depends(get_simulation),
    user: User = Depends(get_user)
) -> APISimulation:
    """
    Return a specific simulation object.
    """
    return APISimulation.from_model(simulation)


def simulation_put(
    simulation: Simulation = Depends(get_simulation),
    sim_body: DamnFastAPISimulation = Body(...),
    user: User = Depends(get_user),
) -> APISimulation:
    """
    Update a simulation.
    """
    simulation.update_from_api(sim_body)
    simulation.save()
    return APISimulation.from_model(simulation)


def simulation_delete(
    simulation: Simulation = Depends(get_simulation),
    user: User = Depends(get_user)
) -> APISimulation:
    """
    Delete a simulation.
    """
    d = APISimulation.from_model(simulation)
    simulation.delete()
    return d