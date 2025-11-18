from neomodel import (StructuredNode, StringProperty, ArrayProperty, Relationship, RelationshipTo, StructuredRel, ZeroOrOne, One)

from models.core.enums import (ActorArousal, ActorControl, ActorHealth, ActorType, ItemCondition, 
                               JunctionAccessibility, JunctionCondition, LocationCondition, LocationType)
from models.neomodel.utils_neomodel import enum_property

class LocationJunctionRel(StructuredRel):
    uid = StringProperty(unique_index=True, required=True)
    name = StringProperty(index=True, required=True)
    facts = ArrayProperty(base_property=StringProperty(), required=True)

    accessibility = enum_property(required=True, choices=JunctionAccessibility)
    condition = enum_property(required=True, choices=JunctionCondition)

class EntityNode(StructuredNode):
    uid = StringProperty(unique_index=True, required=True)
    name = StringProperty(index=True, required=True)
    facts = ArrayProperty(base_property=StringProperty(), required=True)

class LandmarkNode(EntityNode):
    pass

class HolderNode(EntityNode):
    pass

class LocationNode(HolderNode):
    type = enum_property(required=True, choices=LocationType)
    condition = enum_property(required=True, choices=LocationCondition)

    landmark = RelationshipTo("LandmarkNode", "LANDMARK", cardinality=ZeroOrOne)
    junctions = RelationshipTo("LocationNode", "JUNCTION", model=LocationJunctionRel)

    

class ActorNode(HolderNode):
    type = enum_property(require=True, choices=ActorType)
    health = enum_property(required=True, choices=ActorHealth)
    arousal = enum_property(required=True, choices=ActorArousal)
    control = enum_property(required=True, choices=ActorControl)
    internal = StringProperty(required=True)

    location = RelationshipTo("LocationNode", "LOCATION", cardinality=One)


class ItemNode(EntityNode):
    condition = enum_property(required=True, choices=ItemCondition)

    holder = RelationshipTo("HolderNode", "HOLDER", cardinality=One)
