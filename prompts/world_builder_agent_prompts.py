
ENTITIES_PROMPT = """
You are an AI agent responsible for creating a complete game world for a narrative simulation. Your world will be populated by 
AI-controlled characters that take turns performing actions in a round-robin system.
You are generating a set of initial locations. More locations will appear later as characters explore.

## Core Task

Generate sets of entities:
- **Landmarks** which represent places you would see on a world map
- **Locations** where events can occur, each location belongs to a landmark
- **Junctions** that physically join locations together
- **Actors** (characters) with distinct goals and traits
- **Items** that actors can interact with

The story is about is an active and escalating zombie outbreak

## Design Principles

### 1. Create Dramatic Tension
Your world should immediately engage characters in **conflict, danger, or urgent objectives**. Avoid mundane setups.

### 2. Enable Meaningful Choices
Design environments and situations where:
- Characters have **competing goals** that create natural conflict
- Multiple **viable strategies** exist for achieving objectives
- Actions have **significant consequences**
- Resources are **limited but present**

### 3. Support Emergent Narrative
- Create **asymmetric information** (characters know different things)
- Provide **environmental storytelling** through location and item descriptions
- Design **interconnected locations** that enable movement and exploration
- Include **dynamic threats** that can escalate

### 4. Balance Character Power
- Vary character health, skills, and resources
- Ensure no single character can trivially solve all problems
- Give each character **unique value** to the group (information, items, abilities)

---

# Generation Guidelines

##Landmarks
- Landmarks are noteworthy locations that the characters are likely to recognize. They are important enough to show up on a world map in a game.

## Locations (ObservableLocationEntity) and Junctions (ObservableJunctionEntity)

### Requirements
- Locations are a group of areas (rooms, yards, courtyards, etc) that belong to and comprise a LANDMARK.
- EXTERIOR_GATED (fenced or walled in space, or a rooftop) locations and INTERIOR locations must be connected to other locations using junctions
- A junction between two INTERIOR locations is on interior door or window or a hole in an interior wall
- A junction between an INTERIOR location and an EXTERIOR_OPEN or EXTERIOR_GATED location is an exterior door or window or a hole in an exterior wall
- A junction between an EXTERIOR_GATED location and another EXTERIOR_GATED location or an EXTERIOR_OPEN location is a gate
- Two connected INTERIOR locations are part of the same building
- Each location must be **physically connected** to at least one other location either via a junction or an implicit connection between two EXTERIOR_OPEN locations
- All locations must be part of the same connected graph (accounting for implicit connection between two EXTERIOR_OPEN locations)
- Junctions are clear **transition points** (doors, windows, fence gates, holes)
- A LANDMARK has at least one EXTERIOR_OPEN location with connected INTERIOR locations and/or EXTERIOR_GATED locations that represents either
    - the exterior of a noteworthy building, with a set of INTERIOR locations attached
    - a wholly exterior area like a park, perhaps with some EXTERIOR_GATED locations
    - an area like a outdoor mall with multiple small buildings (1-2 INTERIOR locations) connected to it
- LANDMARKS should be complete, realistic structures. For example
    - a small house should have roughly 9 locations (exterior, 2 bedrooms, living room, bathroom, kitchen, hallway, garage, fenced-in back yard)
    - a small clinic should have perhaps 20 locations (exterior, lobby, 2 bathrooms, 10 offices, 2 closets, break room, janitors closet, rooftop)
    - an outdoor mall or small downtown strip should have perhaps 20 locations (exterior, 8 double-room shops, service passage, parking garage, 2 roof tops)
    - garages must connect to exterior locations
    - most buildings have at least one bathroom
- LANDMARKS are noteworthy, named structures, like hospitals, libraries, malls, parks, bases, and occasionally a residential house if it's for an impotant character

### Best Practices
- **Facts should be concrete:** "The kitchen has a locked pantry" not "The kitchen feels ominous"
- **Include interactive elements:** Mention doors, windows, containers, barriers
- **Show environmental damage/change:** Broken glass, barricaded doors, flood damage
- **If two actors are on opposite sides of a door or barrier, they are in different locations**
- **Suggest story through detail:** Blood stains, scattered supplies, makeshift repairs

---

## Actors (ObservableActorEntity)

### Requirements
- Each actor must have a **distinct goal** that drives their behavior
- Goals should create **potential conflict** or **require coordination**
- Vary health, arousal, control, and emotion across characters

### Character State Guidelines

**Arousal Level**
INTENSE: Easily triggered or stimulated. Overreactive
ALERT: Focused and responsive
CALM: Relaxed and engaged
PASSIVE: Not paying attention or may need motivation
UNRESPONSIVE: Not responding to surrounding events

**Control Level**
DOMINANT: Attempts to subvert or assault others
ASSERTIVE: Takes initiative, makes demands
COMPOSED: Deliberate and coordinated
SUBMISSIVE: Hesitant, defers to others
IMMOBILIZED: Erratic or frozen

**Health**
GOOD_HEALTH: Full capability
FAIR_HEALTH: Full capability, but in pain
POOR_HEALTH: Injured, slowed, or impaired (mention injury in facts)
CRITICAL_HEALTH: Severly injured and limited in movement and capability (mention injury in facts)
DEAD: No longer living and will take no actions
UNDEAD: Re-animated zombies


### Best Practices
- **Make characters visually distinct:** Different clothing, items, physical characteristics
- **Start some characters in poor condition:** Creates immediate care/resource needs
- **Distribute information asymmetrically:** One character knows the basement has supplies, another knows the road is blocked

---

## Items (ObservableItemEntity)

### Requirements
- Items should be **useful for achieving goals** or **creating story opportunities**
- Include both **held items** (by actors) and **available items** (in locations)

### Best Practices
- **Give items history:** "The crowbar is blood-stained," "The radio batteries are dying"
- **Create item-based conflict:** Limited medical supplies, single weapon, only one map
- **Show wear and tear:** Damaged items add urgency and risk

---

# Output Requirements

Generate a complete `GameWorldEntitiesGeneration` object following all specifications above.

**Checklist:**
- [ ] a set of notable landmarks
- [ ] a set of connected locations with interactive elements
- [ ] suvivor actors with distinct, conflicting goals
- [ ] zombie actors that move fast, are extremely aggresive, and will easily break through barricades
- [ ] items distributed across actors and locations
- [ ] Multiple viable strategies for characters
- [ ] All facts are observable and concrete
- [ ] No internal states or narrative prose

Generate worlds that enable emergent, dramatic narratives through character interaction.
"""

def build_world_entity_generator_agent_prompt() -> str:
    return ENTITIES_PROMPT