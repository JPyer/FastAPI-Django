# -*- coding: utf-8 -*-
"""
@Time ： 2020/10/19 10:56 am
@Auth ： maker 
@Email：jwjier@gmail.com
"""


# TODO URLS
'''
This should be pretty straightforward. summary and tags are used purely for the documentation site, 
they have no other functional purpose. 
name is used for getting a route’s URL by name, and response_model is used for validation of the response and documentation.
'''

from fastapi import APIRouter

from main import views

# The API model for one object.
from main.models import APISimulation

# The API model for a collection of objects.
from main.models import APISimulations

router = APIRouter()

router.get(
    "/simulation/",
    summary="Retrieve a list of all the simulations.",
    tags=["simulations"],
    response_model=APISimulations,
    name="simulations-get",
)(views.simulations_get)
router.post(
    "/simulation/",
    summary="Create a new simulation.",
    tags=["simulations"],
    response_model=APISimulation,
    name="simulations-post",
)(views.simulation_post)

router.get(
    "/simulation/{simulation_id}/",
    summary="Retrieve a specific simulation.",
    tags=["simulations"],
    response_model=APISimulation,
    name="simulation-get",
)(views.simulation_get)
router.put(
    "/simulation/{simulation_id}/",
    summary="Update a simulation.",
    tags=["simulations"],
    response_model=APISimulation,
    name="simulation-put",
)(views.simulation_put)
router.delete(
    "/simulation/{simulation_id}/",
    summary="Delete a simulation.",
    tags=["simulations"],
    response_model=APISimulation,
    name="simulation-delete",
)(views.simulation_delete)