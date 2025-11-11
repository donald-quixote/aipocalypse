from typing import List, Set

from pydantic import BaseModel

from models.generations import GeneratableTuple
from models.keywords import ActorId, ItemId, LocationId
from models.observables import ObservableAction, ObservableActorEntity, ObservableEvent, ObservableItemEntity, ObservableLocationEntity, ObservableOutcome


class LocationEntity(BaseModel):
    """
    Combines the observable state (facts) of a location with narrative prose grounded in and embelishing these facts
    """
    observable: ObservableLocationEntity
    narrative_description: str

class ActorEntity(BaseModel):
    """
    Combines the observable state (facts) of an actor (story character) with narrative prose grounded in and embelishing these facts
    """
    observable: ObservableActorEntity
    narrative_description: str

class ItemEntity(BaseModel):
    """
    Combines the observable state (facts) of an item with narrative prose grounded in and embelishing these facts
    """
    observable: ObservableItemEntity
    narrative_description: str

class Situation(BaseModel):
    """
    An ongoing interaction between multiple actors.
    The primary game loop revolves around playing out a situation by 
    prompting each actor to respond to the conditions of the situation until resolution
    """
    actors_ids: List[ActorId]
    event_history: List[ObservableEvent | ObservableAction | ObservableOutcome]
    actor_action_queues: List[GeneratableTuple[ActorId, List[ObservableEvent | ObservableAction]]]

class GameWorld(BaseModel):
    """
    The central state container for game entities and events.
    This is the game world that persists across and beyond multiple situations
    """
    locations: List[GeneratableTuple[LocationId, LocationEntity]] = {}
    actors: List[GeneratableTuple[ActorId, ActorEntity]] = {}
    items: List[GeneratableTuple[ItemId, ItemEntity]] = {}
    active_situations: List[Situation] = []

    #TODO: support merging of situations
    def get_actor_situations(self, actor_id: ActorId) -> List[Situation]:
        return [situ for situ in self.active_situations if actor_id in situ.actors_ids]
    
    def get_actor_location(self, actor_id: ActorId) -> LocationEntity:
        actor = self.actors[actor_id]
        return self.locations[actor.observable.state_history[-1].location_id]

    def get_actors_in_location(self, location_id: LocationId) -> List[ActorEntity]:
        return [actor for _, actor in self.actors.items() if actor.state_history[-1].location_id == location_id]
    
    def get_item_location(self, item_id: ItemId) -> LocationEntity:
        item = self.items[item_id]
        return self.locations[item.observable.state_history[-1].location_id]

    def get_items_in_location(self, location_id: LocationId) -> List[ItemEntity]:
        # actor_ids = [actor.id for actor in self.get_actors_in_location(location_id)]
        return [item for _,item in self.items.items() if item.state_history[-1].holder_id in location_id]
    
    def get_items_for_actor(self, actor_id: ActorId) -> List[ItemEntity]:
        return [item for _, item in self.items.items() if item.state_history[-1].holder_id == actor_id]