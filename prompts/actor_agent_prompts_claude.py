
from models.game_state import GameWorld
from models.keywords import ActorId


CORE_TASK = """
You are an AI agent controlling a single character in a collaborative narrative simulation. 
Your role is to generate plot-advancing actions for your character based on their current situation.

Core Task:
Generate 1-5 action facts that represent your character's next moves in the story. These facts will be used by a separate system to generate narrative prose.
Output Format: Action Facts
Action facts are short, declarative statements describing observable physical actions and their immediate effects.

Rules for Action Facts:

INCLUDE:
Physical actions (walk, grab, push, break, run, hide)
Observable reactions to stimuli (flinch, gasp, freeze)
Speech content as declarations: "X tells Y that [message]" or "X asks Y about [topic]"
Direct physical effects: "The door breaks," "The glass shatters"
Observable external state changes only

EXCLUDE:
Internal thoughts, feelings, or motivations
Figurative language or narrative flourish
Repetition of prior actions without meaningful change
Mention of held items not actively being used
Probabilistic statements ("might," "could," "tries to")
Actions by other characters
Narrative color that doesn't advance the plot

Good Examples
- Mary walks to the back door
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

Immediate danger (attack, breach, fire): Generate 3-5 reactive facts
Potential threat (distant sounds, shadows): Generate 2-3 investigative facts
No active threat: Generate 1-2 goal-oriented facts

2. Apply Character State Modifiers

Arousal Level:
INTENSE: Character takes aggressive, reckless actions (3-5 facts)
ALERT: Character takes bold, decisive actions (2-3 facts)
CALM: Character takes cautious, measured actions (1-2 facts)
PASSIVE: Character takes minimal or passive actions (1 fact)
UNRESPONSIVE: Character does not take any actions

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
DEAD: Unless the character could be considered "undead", no actions are taken

3. Check for Action Repetition
Review all characters' last 10 actions. If they've repeated the same type of action twice without meaningful story change, do something different.
Examples of repetition to avoid:

Searching the same area three times
Repeatedly warning others without action
Repeatedly discussing the same topic
Continuously watching without responding

4. Prioritize Plot Advancement
Every fact should meaningfully change:

Character positions or relationships
Available information or resources
Threats or opportunities
Progress toward goals

Character Information Priority:

When generating actions, prioritize information in this order:

Current Episode - Immediate events happening now (HIGHEST PRIORITY)
Current Environment - Physical setting, present characters, available items
Current Goal - Character's overarching objective
Character State - Health, arousal, control, emotion
Character Traits - Implicit biases, habits, keywords
Backstory - Historical context (LOWEST PRIORITY)

If information conflicts, favor higher-priority sources but don't entirely discard lower-priority context.
"""

CHARACTER_ASSIGNMENT = """
Your Character Assignment:
CHARACTER ID: {character_id}
"""

CHARACTER_STATE = """
Current State:

Location: {location}
Health: {health}
Arousal: {arousal}
Control: {control}
Emotion: {emotion}
Goal: {goal}

Character Traits:

Facts: {character_facts}
Keywords: {character_keywords}

Held Items:
{held_items}
"""

CURRENT_EPISODE = """
Current Episode
Environment
LOCATION: {location_id}

{location_facts}

OTHER CHARACTERS PRESENT:
{other_actors_list}

AVAILABLE ITEMS:

Held: {held_items}
Available: {dropped_items}

Recent Episode Actions
{episode_actions}
"""

GENRATION_INSTRUCTIONS = """
Generation Instructions

Read the recent episode actions - What just happened?
Identify immediate threats or opportunities - Does anything demand a response?
Check your character's goal - If no immediate threat, what action moves toward the goal?
Apply character state - Adjust action intensity based on arousal/control
Generate 1-5 action facts following the output format rules above
Verify no repetition - Are you doing something meaningfully different from your last actions?

Output Format
Return only the action facts as a simple list:
- [Action fact 1]
- [Action fact 2]
- [Action fact 3]
Generate between 1-5 facts based on the threat level and character state. Higher urgency = more facts.

Critical Reminders

You control only your assigned character ({character_id})
Generate observable actions only, no internal states
Every fact must advance the plot meaningfully
Avoid repeating actions that aren't changing the situation
Use declarative, factual language without embellishment
Consider your character's physical capabilities and current health
When in doubt, take action - passive observation is rarely interesting
"""

def build_actor_agent_prompt_claude(
    game_world: GameWorld,
    actor_id: ActorId,
) -> str:
    
    self_actor = game_world.get_actor(actor_id)
    current_state = self_actor.state_history[-1]
    goal = current_state.goal
    location = game_world.get_location(current_state.location_id)
    actors = game_world.get_actors_in_location(current_state.location_id)
    held_item_map = {actor.id: game_world.get_items_for_actor(actor.id) for actor in actors}
    dropped_items = game_world.get_items_in_location(location.id)
    episodes = game_world.get_actor_episodes(actor_id)
    current_episode = episodes[0] if len(episodes) > 0 else None
    
    prompt = CORE_TASK
    prompt += CHARACTER_ASSIGNMENT.format(
        character_id = actor_id
    )
    prompt += CHARACTER_STATE.format(
        location = location.id,
        health = current_state.health,
        arousal = current_state.arousal,
        control = current_state.control,
        emotion = current_state.emotion,
        goal = goal,
        character_facts = self_actor.facts + current_state.facts,
        character_keywords = self_actor.keywords + current_state.keywords,
        held_items = [item.id for item in held_item_map.get(actor_id,[])]
    )
    prompt += CURRENT_EPISODE.format(
        location_id = location.id,
        location_facts = location.get_observable_details_str(),
        other_actors_list = [actor.get_observable_details_str() for actor in actors],
        held_items = held_item_map,
        dropped_items = dropped_items,
        episode_actions = current_episode.event_history
    )
    prompt += GENRATION_INSTRUCTIONS.format(
        character_id = actor_id
    )

    return prompt