
from typing import List
from pydantic import BaseModel

from models.core.enums import ActionType, EntityType


class Action(BaseModel):
    uid: str
    type: ActionType
    source_actor_id: str
    target_entity_id: str
    target_entity_type: EntityType
    facts: List[str]

class Outcome(BaseModel):
    action_id: str
    is_success: bool
    attention: int
    facts: List[str]
