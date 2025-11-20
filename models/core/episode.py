
from typing import Dict, List
from pydantic import BaseModel

from models.core.actions import Action, Outcome
from models.core.entities import ActorEntity, ObservableActorEntity, ItemEntity, JunctionEntity, LandmarkEntity, LocationEntity

class Environment(BaseModel):
    landmark: LandmarkEntity
    locations: Dict[str, LocationEntity] = {}
    junctions: Dict[str, JunctionEntity] = {}
    actors: Dict[str, ActorEntity] = {}
    items: Dict[str, ItemEntity] = {}

    actions: List[Action] = []
    outcomes: List[Outcome] = []

    def get_actor_surroundings(self, actor_id: str):
        target_actor = self.actors[actor_id]
        location = self.locations[target_actor.location_id]
        junctions = {junction.uid: junction for junction in self.junctions.values() if location.uid in [junction.from_location_id, junction.to_location_id]}
        actors = {actor.uid: actor for actor in self.actors.values() if actor.location_id == location.uid}
        items = {item.uid: item for item in self.items.values() if item.holder_id in actors.keys() or item.holder_id == location.uid or item.holder_id == actor_id}

        return Environment(
            landmark=self.landmark,
            locations={location.uid: location},
            junctions=junctions,
            actors=actors,
            items=items,
            actions=self.actions, # TODO: filter down
            outcomes=self.outcomes, # TODO: filter down
        )
    
    def get_actor_targeting_actions(self, actor_id: str) -> List[Action]:
        return [action for action in self.actions if action.target_entity_id == actor_id]
    
    def get_held_items(self) -> List[ItemEntity]:
        return [item for item in self.items.values() if item.holder_id not in self.locations.keys()]
    
    def get_dropped_items(self) -> List[ItemEntity]:
        return [item for item in self.items.values() if item.holder_id in self.locations.keys()]
    
    def get_observable_actors(self) -> List[ObservableActorEntity]:
        return [actor.get_observable() for actor in self.actors.values()]
    
class Episode(Environment):
    pass
    