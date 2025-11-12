from pydantic import BaseModel


class Keyword(BaseModel):
    value: str
    model_config = dict(frozen=True)


#Entity IDs
class EntityId(Keyword):
    """A specific noun or adjective that represents and summarizes something well"""
    pass

class LocationId(EntityId):
    """An identifier for a physical place that events can take place within, but does not act on its own"""
    pass

class ActorId(EntityId):
    """An identifier for an independent actor or being that can act on its own, taking actions and responding to stimuli"""
    pass

class ItemId(EntityId):
    """An identifier for an inanimate object that can be interacted with, but does not act on its own"""
    pass

class StaticKeywords:
    # Health Keywords
    DEAD = Keyword(value="DEAD")
    CRITICAL_HEALTH = Keyword(value="CRITICAL_HEALTH")
    POOR_HEALTH = Keyword(value="POOR_HEALTH")
    FAIR_HEALTH = Keyword(value="FAIR_HEALTH")
    GOOD_HEALTH = Keyword(value="GOOD_HEALTH")

    # Condition Keywords
    DESTROYED = Keyword(value="DESTROYED")
    DAMAGED = Keyword(value="DAMAGED")
    FUNCTIONAL = Keyword(value="FUNCTIONAL")
    GOOD_CONDITION = Keyword(value="GOOD_CONDITION")

    # Arousal Keywords
    INTENSE = Keyword(value="INTENSE")
    ALERT = Keyword(value="ALERT")
    CALM = Keyword(value="CALM")
    PASSIVE = Keyword(value="PASSIVE")
    UNRESPONSIVE = Keyword(value="UNRESPONSIVE")

    # Control Keywords
    DOMINANT = Keyword(value="DOMINANT")
    ASSERTIVE = Keyword(value="ASSERTIVE")
    COMPOSED = Keyword(value="COMPOSED")
    SUBMISSIVE = Keyword(value="SUBMISSIVE")
    IMMOBILIZED = Keyword(value="IMMOBILIZED")

    # Emotion Keywords


