from typing import List
from pydantic import BaseModel

from models.core.enums import (ActorArousal, ActorControl, ActorHealth, ActorType, ItemCondition, 
                               JunctionAccessibility, JunctionCondition, LocationCondition, LocationType)


class Entity(BaseModel):
    """A base for entities that can be observed and interacted with"""

    """A unique identifier for an entity (person, place, thing)
    Format: 'type_number',
    begining with its type (landmark, location, junction, actor, item),
    and ending with a random integer between 1000000 and 9999999"""
    uid: str

    """A proper name for an entity that distinguishes it from other entities.
    For actors: their first and last name
    For landmarks: the name of a public location like a business, park, or building
    For locations: a descriptive room or area name
    For junctions: a descriptive name for the door, window, gate, or other opening"""
    name: str

    """a single, declaritive statement that describes the current state of the entity"""
    fact: str

class LandmarkEntity(Entity):
    """A public, noteworthy location that would appear on a map"""
    pass

class LocationEntity(Entity):
    """A space like a room, yard, courtyard, street, playground, etc that exists within a landmark"""

    type: LocationType
    condition: LocationCondition
    landmark_id: str | None = None
    
class JunctionEntity(Entity):
    """A connecting passage (door, window, gate, hole, etc) between two locations"""

    condition: JunctionCondition
    accessibility: JunctionAccessibility

    """if a junction is locked or barricaded, the 'from' side is where the barricade or lock can be controlled. It is the side attempting to keep the junction blocked."""
    from_location_id: str

    """if a junction is locked or barricaded, the 'to' side is the side lacking control. It is the side that is being blocked out."""
    to_location_id: str

class ActorInternalState(BaseModel):
    """Internal goals, knwledge, and emotions that are not observable to other actors, but direct the actions of this actor
    """

    actor_id: str

    """The overarching goal of the actor. They may have to address other immediate scenarios, but when they are not under threat or urgency, this goal drives their actions.
    A campaign goal is the character's end goal of their story. 
    Examples include: finding and rescuing a loved one, escaping the city alive, taking down a rival band of survivors, extracting an important person, extracting an important asset, finding a cure, etc."""
    campaign_goal: str

    """The actor's goal within the current scenario. They may have to address immediate threats or obstacles, but when they are not under immediate threat, this goal drives their actions.
    An episode goal is the character's planned objective while they are at the current landmark. Examples include: escaping the landmark, killing all zombies at the landmark, 
    or finding, obtaining, killing or otherwise taking action on a specific person, item, or location."""
    episode_goal: str

    """The actor's most immediate goal in the middle of action. They may have to address immediate threats, but unless they are actively having to fend off attacks, this goal drives their urgent actions.
    an immediate goal is the next step in a character's plan towards achieving their episode goal. Examples include: removing a barricade, reaching the kitchen, finding a weapon, protecting a person"""
    immediate_goal: str
    
    emotion: str

    """If the actor get's bitten by a zombie, they become infected."""
    is_infected: bool = False

class ObservableActorEntity(Entity):
    type: ActorType
    health: ActorHealth
    arousal: ActorArousal
    control: ActorControl
    location_id: str

class ActorEntity(ObservableActorEntity):
    internal: ActorInternalState

    def get_observable(self):
        copy = self.__dict__.copy()
        copy.pop("internal")
        return ObservableActorEntity(**copy)
   
class ItemEntity(Entity):
    condition: ItemCondition
    holder_id: str
