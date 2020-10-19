# -*- coding: utf-8 -*-
"""
@Time ： 2020/10/19 11:08 am
@Auth ： maker 
@Email：jwjier@gmail.com
"""

from typing import Type

from django.db import models
from fastapi import Header
from fastapi import HTTPException
from fastapi import Path
from goatfish.main.models import Simulation,User

# This is to avoid typing it once every object.
API_KEY_HEADER = Header(..., description="The user's API key.")


def get_user(x_api_key: str = API_KEY_HEADER) -> User:
    """
    Retrieve the user by the given API key.
    """
    u = User.objects.filter(api_key=x_api_key).first()
    if not u:
        raise HTTPException(status_code=400, detail="X-API-Key header invalid.")
    return u


def get_object(
    model_class: Type[models.Model],
    id: str,
    x_api_key: str
) -> models.Model:
    """
    Retrieve an object for the given user by id.

    This is a generic helper method that will retrieve any object by ID,
    ensuring that the user owns it.
    """
    user = get_user(x_api_key)
    instance = model_class.objects.filter(user=user, pk=id).first()
    if not instance:
        raise HTTPException(status_code=404, detail="Object not found.")
    return instance


def get_simulation(
    simulation_id: str = Path(..., description="The ID of the simulation."),
    x_api_key: str = Header(...),
):
    """
    Retrieve the user's simulation from the given simulation ID.
    """
    return get_object(Simulation, simulation_id, x_api_key)