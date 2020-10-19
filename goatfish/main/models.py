from django.db import models

# Create your models here.
# TODO Since we have an API and a database, and the models for the two are neither semantically nor functionally identical,we’ll have two sections in our models.py, one for each model type.
from typing import Any
from typing import Dict
from typing import List

import shortuuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from pydantic import BaseModel


def generate_uuid() -> str:
    """Generate a UUID."""
    return shortuuid.ShortUUID().random(20)


##########
# Models
#


class CharIDModel(models.Model):
    """Base model that gives children random string UUIDs."""

    id = models.CharField(
        max_length=30,
        primary_key=True,
        default=generate_uuid,
        editable=False
    )

    class Meta:
        abstract = True


class User(AbstractUser):
    api_key = models.CharField(
        max_length=100,
        default=generate_uuid,
        db_index=True,
    )

    def __str__(self):
        return self.username


class Simulation(CharIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    start_date = models.DateField()
    end_date = models.DateField()

    @classmethod
    def from_api(cls, user: User, model: "DamnFastAPISimulation"):
        """
        Return a Simulation instance from an APISimulation instance.
        """
        return cls(
            user=user,
            name=model.name,
            start_date=model.start_date,
            end_date=model.end_date,
        )

    def update_from_api(self, api_model: "DamnFastAPISimulation"):
        """
        Update the Simulation Django model from an APISimulation instance.
        """
        self.name = api_model.name
        self.start_date = api_model.start_date
        self.end_date = api_model.end_date

    def __str__(self):
        return self.name

class DamnFastAPISimulation(BaseModel):
    name: str
    start_date: date
    end_date: date

    @classmethod
    def from_model(cls, instance: Simulation):
        """
        Convert a Django Simulation model instance to an APISimulation instance.
        """
        return cls(
            id=instance.id,
            name=instance.name,
            start_date=instance.start_date,
            end_date=instance.end_date,
        )


class APISimulation(DamnFastAPISimulation):
    id: str


class APISimulations(BaseModel):
    items: List[APISimulation]

    @classmethod
    def from_qs(cls, qs):
        """
        Convert a Django Simulation queryset to APISimulation instances.
        """
        return cls(items=[APISimulation.from_model(i) for i in qs])