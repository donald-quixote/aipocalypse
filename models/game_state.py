from typing import Dict, List, NoReturn, Set

from pydantic import BaseModel

from models.keywords import ActorId, ItemId, LocationId
from models.observables import ObservableAction, ObservableActorEntity, ObservableEvent, ObservableItemEntity, ObservableLocationEntity, ObservableOutcome


class Episode(BaseModel):
    """
    An ongoing interaction between multiple actors.
    The primary game loop revolves around playing out a episode by 
    prompting each actor to respond to the conditions of the episode until resolution
    """
    actor_ids: Set[ActorId] = {}
    event_history: List[ObservableEvent | ObservableAction | ObservableOutcome] = []
    actor_action_queues: Dict[ActorId, List[ObservableEvent | ObservableAction]] = {}

    def get_actor_targeting_actions(self, actor_id: ActorId) -> List[ObservableEvent | ObservableAction]:
        return self.actor_action_queues.setdefault(actor_id, [])
    
    def remove_processed_actions(self, actor_id: ActorId) -> NoReturn:
        del self.actor_action_queues[actor_id]


class GameWorld(BaseModel):
    """
    The central state container for game entities and events.
    This is the game world that persists across and beyond multiple episodes
    """
    locations: Dict[LocationId, ObservableLocationEntity] = {}
    actors: Dict[ActorId, ObservableActorEntity] = {}
    items: Dict[ItemId, ObservableItemEntity] = {}
    active_episodes: List[Episode] = []

    def get_actor(self, actor_id: ActorId) -> ObservableActorEntity:
        return self.actors[actor_id]

    def get_location(self, location_id: LocationId) -> ObservableLocationEntity:
        return self.locations[location_id]
    
    def get_item(self, item_id: ItemId) -> ObservableItemEntity:
        return self.items[item_id]

    #TODO: support merging of episode
    def get_actor_episodes(self, actor_id: ActorId) -> List[Episode]:
        return [episode for episode in self.active_episodes if actor_id in episode.actor_ids]
    
    def get_actor_location(self, actor_id: ActorId) -> ObservableLocationEntity:
        return self.get_location(self.get_actor(actor_id).state_history[-1].location_id)

    def get_actors_in_location(self, location_id: LocationId) -> List[ObservableActorEntity]:
        return [actor for actor in self.actors.values() if actor.state_history[-1].location_id == location_id]
    
    def get_item_location(self, item_id: ItemId) -> ObservableLocationEntity:
        return self.get_location(self.get_item(item_id).state_history[-1].location_id)

    def get_items_in_location(self, location_id: LocationId) -> List[ObservableItemEntity]:
        # actor_ids = [actor.id for actor in self.get_actors_in_location(location_id)]
        return [item for item in self.items.values() if item.state_history[-1].holder_id == location_id]
    
    def get_items_for_actor(self, actor_id: ActorId) -> List[ObservableItemEntity]:
        return [item for item in self.items.values() if item.state_history[-1].holder_id == actor_id]


class GameWorldManager:
    __game_world: GameWorld = None

    def get() -> GameWorld:
        return GameWorldManager.__game_world
    
    def set(game_world: GameWorld) -> NoReturn:
        GameWorldManager.__game_world = game_world