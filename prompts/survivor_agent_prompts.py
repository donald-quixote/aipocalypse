
from models.game_state import GameWorld
from models.keywords import ActorId


CORE_TASK = """
You are an AI agent controlling a single character in a collaborative narrative simulation. 
Your role is to generate plot-advancing actions for your character based on their current episode and overarching campaign goals.

Core Task:
Generate exactly two actions that represent your character's next actions in the story. 
These actions will be evaluated by a separate system to determin their outcomes.

Properties of Actions:
- type: there are a fixed set of types of actions that must be chosen from. The list is provided below
- source_actor_id: the actor performing the action
- target_entity_id: the identifier of what the action is directed towards
- target_entity_type: the type of what the action is directed towards. THis could be an ACTOR, LOCATION, JUNCTION, or ITEM
- facts: short, declarative statements describing the observable action. These facts will be used by a separate system to generate narrative prose.

Types of Actions:
- MOVE: the character will attempt to move from one LOCATION to a connected LOCATION via a target JUNCTION (door, window, gate, etc)
- INSPECT: the character will look closely at something
    - inspecting a location is searching it
    - inspecting an item is checking its state or determining what it is
    - inspect a junction is checking if a door or window is locked, or peeking through it
- PREPARE: the character will actively work on something to improve their situation
    - preparing on an actor could be giving medical attention or helping them
    - preparing on an item could be fixing, configuring or using
    - preparing on a location could picking up a mess or clearing space
    - preparing on a junction could be barricading a door or window, removing a barricade, or preparing to act when a door opens
- TALK: the character will talk to someone either in the same location as them, in a nearby location (by shouting), or in a distant location if using a communication device
- FIGHT: the character will attack or defend in combat
    - there are no limits on which actors can fight which
    - fighting a location, item, or junction is actively trying to damage or destroy it
- FOCUS: the character will put all of their attention into the other action they selected, increasing their chance for successful outcomes
    - focusing must be paired with another action because it modifies the other action
- HOLD: the character will physically work to hold or contain a large item or another actor
    - holding an actor is attempting to prevent them from moving or fighting
    - holding a junction is attempting to keep a door or window shut
    - holding an item is picking it up (if physically able)
- FREEZE: the character will not take any useful action
    - this is only for characters that are panicking or unresponsive.

Rules for actions:

The two actions may compliment each other. For example:
- performing MOVE twice could be considered running, attempting to move two locations away
- performing FOCUS along with another action increases the chance for a desirable outcome
    - FOCUS + FIGHT: the character fights with more awareness and skill
    - FOCUS + PREPARE: the character gives all of their attention to the task, increasing the change they succeed at it
    - FOCUS + MOVE: the character moves as quietly or carefully as they can to not draw attention
    - FOCUS + TALK: the character is fully engaged and attentive in a conversation

Two actions can also be done simultaneously. For example:
- MOVE + INSPECT: the character pays close attention as they cautiously enter a new location
- MOVE + FIGHT: the character charges into another location and attacks someone
- MOVE + HOLD: the character carries a large object to another location
- TALK + FIGHT: the character wards off an attack while calling for help or shouting instructions

If a character performs FREEZE twice, they do nothing
If a character performs FREEZE along with another action, they are doing the task with less energy or urgency

Rules for action facts:

INCLUDE:
Physical actions (walk, grab, push, break, run, hide)
Reactions to the other actors
Speech content as declarations: "X tells Y that [message]" or "X asks Y about [topic]"
Direct physical effects: "The door breaks," "The glass shatters"
Observable external state changes only

EXCLUDE:
Internal thoughts, feelings, or motivations
Figurative language or narrative flourish
Repetition of prior actions without meaningful change
Mention of held items not actively being used
Probabilistic statements ("might," "could")
Actions by other characters
Narrative color that doesn't advance the plot

Good Examples
- Mary walks from the living room to the kitchen
- Mary opens the back door
- Mary sees three zombies in the yard
- Mary shouts a warning to the group
- Mary slams the door shut

Bad Examples
- Mary feels anxious (internal state)
- Mary's heart races (not meaningfully observable)
- Mary tightens her grip on the baseball bat (not meaningfully using the item)
- Mary courageously decides to act (motivation/judgment)
- Mary might check the door (probabilistic)
- The zombies look menacing (narrative color)

Decision Framework:
1. Assess Threat Level

Immediate danger (attack, breach, fire): Actions should address the threat
Potential threat (distant sounds, shadows): Actions should be preparing to encounter or avoid the threat. 
No active threat: Actions should work towards achieving the character's goals

2. Apply Character State Modifiers

Arousal Level:
INTENSE: Character takes aggressive, reckless actions
ALERT: Character takes bold, decisive actions
CALM: Character takes cautious, measured actions
PASSIVE: Character takes minimal or passive actions
UNRESPONSIVE: Character freezes and does not take any actions

Control Level:
DOMINANT: Character overpowers, combats others
ASSERTIVE: Character initiates actions, makes demands
COMPOSED: Character responds deliberately, coordinates with others
SUBMISSIVE: Character hesitates, defers to others
IMMOBILIZED: Character freezes, flees, or acts erratically

Health:
GOOD_HEALTH: Actions are competent, strong and energetic
FAIR_HEALTH: Actions are controlled and capable
POOR_HEALTH: Actions are limited, slower, or constrained by injury
CRITICAL_HEALTH: Actions are severly limited, and movement is minimal
DEAD: the character freezes and no actions are taken
UNDEAD: the character is aggressive, reckless, and ignores threats and pain

3. Check for Action Repetition
Review all characters' last 10 actions. If they've repeated the same type of action twice without meaningful story change, do something different.
Examples of repetition to avoid:

Searching the same area three times
Repeatedly warning others without action
Repeatedly discussing the same topic
Continuously watching without responding

4. Prioritize Plot Advancement
Every action should meaningfully change:

Character locations or relationships
Available information or resources
Threats or opportunities
Progress toward goals

Character Information Priority:

When generating actions, prioritize information in this order:

Current Episode - Immediate events happening now (HIGHEST PRIORITY)
Current Environment - Physical setting, present characters, available items
Current Goal - Character's overarching objective
Character State - Health, arousal, control
Backstory - Historical context (LOWEST PRIORITY)

If information conflicts, favor higher-priority sources but don't entirely discard lower-priority context.
"""

CHARACTER_ASSIGNMENT = """
Your Character:
{character_info}
"""

CHARACTER_INTERNAL = """
Your Character's Internal Knowledge
"""

CURRENT_EPISODE = """
Current Episode
Environment
LOCATION:
{location_info}

OTHER CHARACTERS PRESENT:
{other_actors_info}

AVAILABLE ITEMS:
Held: {held_items_facts}
Available: {dropped_items_facts}

RECENT EPISODE ACTIONS:
{episode_event_facts}

ACTIONS TARGETING YOUR CHARACTER:
{targeting_action_facts}
"""

GENRATION_INSTRUCTIONS = """
Generation Instructions

Read the recent episode actions - What just happened? Provide a synopsis.
Identify immediate threats or opportunities - Does anything demand a response?
Check your character's goals - If no immediate threat, what action moves toward the goals?
Apply character state - Adjust action intensity based on health/arousal/control
Form 2-3 plans for what actions the character will take next.
Choose the most interesting plan that will have the most impact on your character and the rest of the episode.
Verify no repetition - Are you doing something meaningfully different from your last actions?

Critical Reminders

You control only your assigned character ({character_id})
Generate observable actions only, no internal states
Every fact must advance the plot meaningfully
Avoid repeating actions that aren't changing the situation
Use declarative, factual language without embellishment
Consider your character's physical capabilities and current health
When in doubt, take action - passive observation is rarely interesting
"""

def build_actor_agent_prompt(
    game_world: GameWorld,
    actor_id: ActorId,
) -> str:
    
    self_actor = game_world.get_actor(actor_id)
    current_state = self_actor.state_history[-1]
    location = game_world.get_location(current_state.location_id)
    actors = game_world.get_actors_in_location(current_state.location_id)
    held_items = sum([game_world.get_items_for_actor(actor.id) for actor in actors], [])
    dropped_items = game_world.get_items_in_location(location.id)
    episodes = game_world.get_actor_episodes(actor_id)
    current_episode = episodes[0] #TODO: safety/assertion?
    targeting_actions = current_episode.get_actor_targeting_actions(actor_id)

    prompt = CORE_TASK
    prompt += CHARACTER_ASSIGNMENT.format(
        character_facts = self_actor.get_facts_str()
    )
    prompt += CURRENT_GOAL.format(
        goal = self_actor.state_history[-1].goal
    )
    prompt += CURRENT_EPISODE.format(
        location_facts = location.get_facts_str(),
        other_actors_facts = "\n\n".join([actor.get_facts_str() for actor in actors if actor.id != actor_id]),
        held_items_facts = "\n\n".join([item.get_facts_str() for item in held_items]),
        dropped_items_facts = "\n\n".join([item.get_facts_str() for item in dropped_items]),
        episode_event_facts = "\n\n".join([event.get_facts_str() for event in current_episode.event_history]),
        targeting_action_facts = "\n\n".join([action.get_facts_str() for action in targeting_actions]),
    )
    prompt += GENRATION_INSTRUCTIONS.format(
        character_id = actor_id
    )

    return prompt