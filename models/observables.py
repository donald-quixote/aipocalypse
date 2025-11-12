from enum import StrEnum
from typing import Generic, List, TypeVar
from pydantic import BaseModel

from models.keywords import ActorId, ItemId, Keyword, EntityId, LocationId, StaticKeywords

class Observable(BaseModel):
    """
    Represents something that can be observed by agents within the story world.
    Agents will be able to inspect facts and keywords associated with observable things.
    """

    """Short, declarative statements about something."""
    facts: List[str]

    """Specific nouns or adjectives that best represent and summarize the state of something"""
    keywords: List[Keyword]

    def get_facts(self) -> List[str]:
        return self.facts
    
    def get_keywords(self) -> List[Keyword]:
        return self.keywords

class ObservableState(Observable):
    """
    A base for the observable state of an observable entity (noun) at a given point in time.
    This object's facts and keywords should not be actions.
    This object's facts and keywords should describe details that may change over time and that represent a point-in-time state.
    Static, unchanging details and attributes of an entity should go directly on the entity and not in its observable state.
    """
    pass

class ObservableHealth(StrEnum):
    DEAD = "DEAD"
    CRITICAL_HEALTH = "CRITICAL_HEALTH"
    POOR_HEALTH = "POOR_HEALTH"
    FAIR_HEALTH = "FAIR_HEALTH"
    GOOD_HEALTH = "GOOD_HEALTH"

class ObservableCondition(StrEnum):
    DESTROYED = "DESTROYED"
    DAMAGED = "DAMAGED"
    FUNCTIONAL = "FUNCTIONAL"
    GOOD_CONDITION = "GOOD_CONDITION"

class ObservableArousal(StrEnum):
    INTENSE = "INTENSE"
    ALERT = "ALERT"
    CALM = "CALM"
    PASSIVE = "PASSIVE"
    UNRESPONSIVE = "UNRESPONSIVE"

class ObservableControl(StrEnum):
    DOMINANT = "DOMINANT"
    ASSERTIVE = "ASSERTIVE"
    COMPOSED = "COMPOSED"
    SUBMISSIVE = "SUBMISSIVE"
    IMMOBILIZED = "IMMOBILIZED"

ID_TYPE = TypeVar("ID_TYPE", bound=EntityId)
STATE_TYPE = TypeVar("STATE_TYPE", bound=ObservableState)
class ObservableEntity(Observable, Generic[ID_TYPE, STATE_TYPE]):
    """
    A base for entities (nouns) that can be observed by agents. 
    This object's facts and keywords should not be actions.
    This object's facts and keywords should describe static, unchanging details and attributes.
    Dynamically changing details that represent a point-in-time state belong in the observable state_history.
    """
    id: ID_TYPE
    state_history: List[STATE_TYPE]
    keywords: List[Keyword]

    def get_facts(self) -> List[str]:
        return self.facts + self.state_history[-1].facts
    
    def get_keywords(self) -> List[Keyword]:
        return self.keywords + self.state_history[-1].keywords

class ObservableLocationState(ObservableState):
    condition: ObservableCondition

class ObservableLocationEntity(ObservableEntity[LocationId, ObservableLocationState]):
    pass

class ObservableActorState(ObservableState):
    location_id: LocationId
    health: ObservableHealth
    arousal: ObservableArousal
    control: ObservableControl
    emotion: Keyword

class ObservableActorEntity(ObservableEntity[ActorId, ObservableActorState]):
    pass

class ObservableItemState(ObservableState):
    holder_id: ActorId | LocationId
    condition: ObservableCondition

class ObservableItemEntity(ObservableEntity[ItemId, ObservableItemState]):
    pass

class ObservableEvent(Observable):
    """
    Events that can be observed by agents.
    This object's facts and keywords should not be static descriptions of entities or attributes.
    This object's facts and keywords should describe events that occur without instigation by actors.
    Events have clear instigator(s) and potentially target(s) as well.
    Events can only be triggered by environmental elements (locations, items)
    This object's facts and keywords should not describe the outcomes of the event, rather only the event itself.
    """
    location_id: LocationId
    source_entity_ids: List[LocationId | ItemId]
    impacted_actor_ids: List[ActorId]
    impacted_item_ids: List[ItemId]

class ObservableAction(Observable):
    """
    Actions or activities that can be observed by agents.
    This object's facts and keywords should not be static descriptions of entities or attributes.
    This object's facts and keywords should describe actions and activities.
    Actions are clear verbs that will meanigfully change the state of entities.
    Do not use verbs like "remaining" "continuing" "standing" or other words that signify a lack of change.
    If there will be no meaningful change from an action, then do not generate that action.
    Actions have clear instigator(s) and potentially target(s) as well.
    Actions can only be instigated by actors.
    This object's facts and keywords should not describe the outcomes of the action, rather only the action itself.
    """
    location_id: LocationId
    source_actor_ids: List[ActorId]
    target_actor_ids: List[ActorId]
    target_item_ids: List[ItemId]

class ObservableOutcome(Observable):
    """
    The outcomes (states, attributes) of events (actions, activities) that can be observed by agents.
    This object's facts and keywords should not describe actions and activities.
    This object's facts and keywords should be static descriptions of states and attributes of a targeted entity
    as resulting from the action.
    """
    location_id: LocationId