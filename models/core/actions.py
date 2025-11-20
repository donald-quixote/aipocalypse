
import random
from typing import List
from pydantic import BaseModel

from models.core.entities import ActorEntity, ItemEntity, JunctionEntity, LocationEntity
from models.core.enums import ActionType, EntityType, OutcomeType


class Action(BaseModel):
    uid: str
    type: ActionType
    location_id: str
    source_actor_id: str
    target_entity_id: str
    target_entity_type: EntityType
    fact: str


class Outcome(BaseModel):

    """the action that caused this outcome"""
    action_id: str

    """how successful the action was from the perspective of the source actor"""
    type: OutcomeType

    """how much attention does the action draw (how loud or visible is it)"""
    attention: int

    """resulting status of the action's source entity. If there are no status changes to source entity, omit this"""
    resulting_source_entity_status: ActorEntity | None = None 

    """resulting status of the action's target entity. If there are no status changes to target entity, omit this"""
    resulting_target_entity_status: LocationEntity | JunctionEntity | ActorEntity | ItemEntity | None = None

    """a single, short declarative statement about the outcome of an action. Should not describe further actions."""
    fact: str
