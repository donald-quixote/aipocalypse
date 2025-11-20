

from typing import Dict, List
from neomodel import db

from models.core.entities import (ActorEntity, ActorInternalState, Entity, ItemEntity, JunctionEntity, LandmarkEntity, LocationEntity)
from models.core.episode import Episode


class NeoModelQueries:

    def create_or_update_landmarks(*landmarks: LandmarkEntity):
        rows = [landmark.__dict__ for landmark in landmarks]
        
        QUERY = """
            UNWIND $rows AS row

            MERGE (loc:LandmarkNode {uid: row.uid})
            SET loc.name     = row.name,
                loc.fact    = row.fact,
                loc.type     = row.type
            ;
        """
        db.cypher_query(QUERY, {"rows": rows})

    def create_or_update_locations(*locations: LocationEntity):
        rows = [location.__dict__ for location in locations]

        QUERY = """
            UNWIND $rows AS row

            MERGE (loc:LocationNode {uid: row.uid})
            SET loc.name     = row.name,
                loc.fact    = row.fact,
                loc.type     = row.type,
                loc.condition   = row.condition

            WITH row, loc
            OPTIONAL MATCH (loc)-[oldRel:LANDMARK]->(:LandmarkNode)
            DELETE oldRel
            WITH row, loc
            MATCH (lm:LandmarkNode {uid: row.landmark_id})
            WHERE loc.type = 'EXTERIOR_OPEN'
            MERGE (loc)-[:LANDMARK]->(lm)
            ;
        """
        db.cypher_query(QUERY, {"rows": rows})

    def create_or_update_junctions(*junctions: JunctionEntity):
        """NOTE: This only supports creating relations and updating props. It does not support changing the nodes in the relation"""
        rows = [junction.__dict__ for junction in junctions]

        QUERY = """
            UNWIND $rows AS row

            MATCH (from:LocationNode {uid: row.from_location_id})
            MATCH (to:LocationNode   {uid: row.to_location_id})

            MERGE (from)-[j:JUNCTION]->(to)
            SET j.uid           = row.uid,
                j.name          = row.name,
                j.fact         = row.fact,
                j.accessibility = row.accessibility,
                j.condition     = row.condition
            ;
        """
        db.cypher_query(QUERY, {"rows": rows})

    def create_or_update_actors(*actors: ActorEntity):
        rows = [actor.__dict__ for actor in actors]
        for row, actor in zip(rows, actors):
            row["internal"] = actor.internal.model_dump_json()
        
        QUERY = """
            UNWIND $rows AS row

            //UPDATE ACTOR NODE
            MERGE (a:ActorNode {uid: row.uid})
            SET a.name     = row.name,
                a.fact    = row.fact,
                a.type     = row.type,
                a.health   = row.health,
                a.arousal  = row.arousal,
                a.control  = row.control,
                a.internal = row.internal

            //UPDATE LOCATION REL
            WITH row, a
            MATCH (loc:LocationNode {uid: row.location_id})
            OPTIONAL MATCH (a)-[old:LOCATION]->(:LocationNode)
            DELETE old
            MERGE (a)-[:LOCATION]->(loc)
            ;
        """
        db.cypher_query(QUERY, {"rows": rows})

    def create_or_update_items(*items: ItemEntity):
        rows = [item.__dict__ for item in items]

        QUERY = """
            UNWIND $rows AS row

            //UPDATE ITEM NODE
            MERGE (i:ItemNode {uid: row.uid})
            SET i.name     = row.name,
                i.fact    = row.fact,
                i.condition   = row.condition

            //UPDATE HOLDER REL
            WITH row, i
            OPTIONAL MATCH (i)-[oldRel:HOLDER]->()
            DELETE oldRel
            WITH row, i
            MATCH (h:LocationNode|ActorNode {uid: row.holder_id})
            MERGE (i)-[:HOLDER]->(h)
            ;
        """
        db.cypher_query(QUERY, {"rows": rows})

    __NODE_CLASS_MAPPING = {
        "LandmarkNode": LandmarkEntity,
        "LocationNode": LocationEntity,
        "ActorNode": ActorEntity,
        "ItemNode": ItemEntity,
    }

    @classmethod
    def __hydrate_entity(cls, labels: List[str], props: Dict[str,str]) -> Entity:
        # using model_construct for partial hydration since we want to handle hydrating relationships as a separate phase
        for label in labels:
            if label in cls.__NODE_CLASS_MAPPING:
                return cls.__NODE_CLASS_MAPPING[label].model_construct(**props)
    
    @classmethod
    def load_episode_from_landmark(cls, landmark_id: str) -> Episode:

        QUERY = """
        MATCH (lm:LandmarkNode {uid: $uid})
        CALL apoc.path.subgraphAll(lm, {
            relationshipFilter: "LOCATION|LANDMARK|JUNCTION|HOLDER"
        }) YIELD nodes, relationships
        RETURN DISTINCT nodes, relationships
        ;
        """
        records, _ = db.cypher_query(QUERY, {"uid": landmark_id})
        if not records:
            return None
        
        landmark = None
        locations = {}
        actors = {}
        items = {}
        junctions = []

        intermediate = [cls.__hydrate_entity(list(n.labels), n._properties) for n in records[0][0]]
        for entity, node in zip(intermediate, records[0][0]):
            match entity:
                case LandmarkEntity():
                    landmark = entity
                case LocationEntity():
                    locations[node.id] = entity
                case ActorEntity():
                    entity.internal = ActorInternalState.model_validate_json(node._properties["internal"])
                    actors[node.id] = entity
                case ItemEntity():
                    items[node.id] = entity

        for rel in records[0][1]:
            from_node_id = rel.nodes[0].id
            to_node_id = rel.nodes[1].id
            match rel.type:
                case "LANDMARK":
                    locations[from_node_id].landmark_id = landmark.uid
                case "LOCATION":
                    actors[from_node_id].location_id = locations[to_node_id].uid
                case "HOLDER":
                    items[from_node_id].holder_id = (locations.get(to_node_id, None) or actors.get(to_node_id, None)).uid
                case "JUNCTION":
                    from_location_id = locations[from_node_id].uid
                    to_location_id = locations[to_node_id].uid
                    junction = JunctionEntity(**rel._properties, from_location_id=from_location_id, to_location_id=to_location_id)
                    junctions.append(junction)

        # running delayed pydantic validation by explicitly dumping pydantic dicts and re-instantiating
        # this is necessary since we use model_construct (which excludes validation) to partially hydrate the models from db nodes
        return Episode(
            landmark=LandmarkEntity.model_validate(landmark.model_dump(warnings="none")),
            locations={location.uid: LocationEntity.model_validate(location.model_dump(warnings="none")) for location in locations.values()},
            junctions={junction.uid: JunctionEntity.model_validate(junction.model_dump(warnings="none")) for junction in junctions},
            actors={actor.uid: ActorEntity.model_validate(actor.model_dump(warnings="none")) for actor in actors.values()},
            items={item.uid: ItemEntity.model_validate(item.model_dump(warnings="none")) for item in items.values()},
            actions = [],
            outcomes = [],
        )


        



        

