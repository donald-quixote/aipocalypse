
from typing import List
from pydantic import BaseModel

from models.core.actions import Action, Outcome
from models.core.entities import ActorEntity, ItemEntity, JunctionEntity, LandmarkEntity, LocationEntity


class Episode(BaseModel):
    landmark: LandmarkEntity
    locations: List[LocationEntity] = []
    junctions: List[JunctionEntity] = []
    actors: List[ActorEntity] = []
    items: List[ItemEntity] = []

    actions: List[Action] = []
    outcomes: List[Outcome] = []