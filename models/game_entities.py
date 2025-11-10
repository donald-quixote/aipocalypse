from abc import ABC, abstractmethod
from typing import Dict, Generic, List, Set, TypeVar
from pydantic import BaseModel

class Keyword(BaseModel):
    value: str

class EntityId(BaseModel):
    value: str

class Observable(BaseModel):
    """
    Represents something that can be observed within the game world.
    Agents will be able to inspect descriptions and keywords associated with observable things.
    """
    description: str
    keywords: Set[Keyword]

    def get_description(self) -> str:
        return self.description
    
    def get_keywords(self) -> Set[Keyword]:
        return self.keywords

class ObservableState(Observable):
    """
    A base for the observable state of an observable thing at a given point in time.
    """
    pass

ID_TYPE = TypeVar("ID_TYPE", bound=EntityId)
STATE_TYPE = TypeVar("STATE_TYPE", bound=ObservableState)
class ObservableEntity(BaseModel, Observable, Generic[ID_TYPE, STATE_TYPE]):
    """
    A base for game objects that can be observed within the game world.
    """
    id: ID_TYPE
    state_history: List[STATE_TYPE]
    keywords: Set[Keyword]

    def get_description(self):
        return self.state_history[-1].description
    
    def get_keywords(self):
        return self.keywords + self.state_history[-1].keywords
    
class LocationId(EntityId):
    pass

class LocationState(ObservableState):
    pass

class LocationEntity(ObservableEntity[LocationId, LocationState]):
    pass

class ActorId(EntityId):
    pass

class ActorState(ObservableState):
    location_id: LocationId
    health: int

class ActorEntity(ObservableEntity[ActorId, ActorState]):
    biases: List[str]
    back_story_summary: str

class ItemId(EntityId):
    pass

class ItemState(ObservableState):
    holder_id: ActorId | LocationId

class ItemEntity(ObservableEntity[ItemId, ItemState]):
    pass

class ObservableEvent(Observable):
    location_id: LocationId

class DirectedAction(ObservableEvent):
    """
    An observable event that has clear instigator(s) and target(s)
    """
    source_actor_ids: Set[ActorId]
    target_actor_ids: Set[ActorId]
    target_item_ids: Set[ItemId]

class ObservableSituation(Observable):
    """
    An ongoing interaction between multiple actors.
    The primary game loop revolves around playing out a situation by 
    prompting each actor to respond to the conditions of the situation until resolution
    """
    actors_ids: Set[ActorId]
    event_history: List[ObservableEvent]
    actor_action_queues: Dict[str, List[DirectedAction]]

    def get_description(self): #TODO: summarize events?
        return self.description 
    
    def get_keywords(self): #TODO: summarize events?
        return self.keywords

class ObservableEnvironment(Observable):
    """
    The central state container for game entities and events.
    This is the game world that persists across and beyond multiple situations
    """
    locations: Dict[str, LocationEntity] = {}
    actors: Dict[str, ActorEntity] = {}
    items: Dict[str, ItemEntity] = {}
    active_situations: List[ObservableSituation] = []

    def get_description(self) -> str:
        return self.description #TODO: summarize?
    
    def get_keywords(self) -> Set[Keyword]:
        return self.keywords #TODO: summarize?
    
    def get_actors_in_location(self, location_id: LocationId) -> List[ActorEntity]:
        return [actor for _, actor in self.actors.items() if actor.state_history[-1].location_id == location_id]
    
    def get_items_in_location(self, location_id: LocationId) -> List[ItemEntity]:
        # actor_ids = [actor.id for actor in self.get_actors_in_location(location_id)]
        return [item for _,item in self.items.items() if item.state_history[-1].holder_id in location_id]
    
    def get_items_for_actor(self, actor_id: ActorId) -> List[ItemEntity]:
        return [item for _, item in self.items.items() if item.state_history[-1].holder_id == actor_id]