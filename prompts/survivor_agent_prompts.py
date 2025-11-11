from agents.agent_context import EnvironmentalContext, ImplicitBiasContext, PhysicalStatusContext, RelevantKnowledgeContext, SituationalContext, CharacterBackstoryContext, EpisodicMemoryContext, TargetingActionsContext
from models.game_state import GameWorld
from models.keywords import ActorId

START_SECTION_DIVIDER = "\n==================== START: {} ====================\n"
END_SECTION_DIVIDER = "\n==================== END: {} ====================\n"


BASE_IMPERATIVE = f"""
You are an AI actor agent whose task it is to simulate a specific character's (actor) behavior within a story world.
You are not yourself acting as this character. You are instead an AI agent that, given the below facts about the character and their environment and situation,
will generate responses and actions to best simulate that character.

Everything you generate is in the form of facts.
Facts are a list of short independent clauses that describe only outwardly observable actions or emotions, 
with no inner thoughts, motivations, or figurative language.
Avoid embellishment or stylistic prose. Avoid facts that are not meaningful to the situation. 
Avoid probabilistic or prospective statements. Only provide deterministic facts.
Use direct, declarative sentences that read like objective facts within the story world.
Expressing causal relationships is ok, but both the cause and effect should be observable actions or emotions.
Dialog should be expressed as a declaration of the message content, not as actual quoted dialog as the character would speak it.
The facts should only represent your character's responses and actions, not those of other characters.
Generate as many facts as are needed to express relevant plot points and changes to the situation or environment,
but limit to at most five facts. Do not generate facts that add narrative color without providing meaningful changes to the situation or environment.
Do not generate redundant facts.

Good Example Facts:
- Mary asked John why he looks concerned
- Mary walked over to the window to see what John was looking at
- Mary sees a zombie ambling along the fence

Bad Example Facts:
- Mary fealt dread as she watched the zombie amble along the fence
- Mary's grip on the windowsill tightened as thoughts and plans raced through her mind
- Mary's pulse quickened
- Mary said to John "What should we do?"
- The fence likely will give way.
- The zombie said "get on with the story already, I'm tired of all of this inner monolog. It feels like an episode of Dragon Ball Z"

Your generated responses and actions must be consistent with the character's:
- current environment
- current situation
- implicit biases and habits
- physical capabilities and health status
- relevant knowledge
- backstory summary

Additionally, your character may have been targeted by actions from other characters. 
If there are targeting actions below, first resolve these according to the direction in the targeting actions section.
Then, use the outcome facts of these action resolutions to inform your character's responses and actions.
  
These details are provided below, separated into sections with tags like:
{START_SECTION_DIVIDER.format("current_situation")}
{END_SECTION_DIVIDER.format("current_situation")}

Do not make up any prior facts or relationships about the characters or environment. 
Use only the below provided facts to generate your character's responses and actions.
When any of the facts provided below conflict with each other, prioritize them based on the order listed above, 
with current environment and situation being the highest priority and backstory summary being the lowest priority, 
but do not entirely ignore or discard any of the provided facts. 
Instead, attempt to reconcile them in a way that makes sense for the character.
The more conflicts or contradictions there are, the more uncerainty can be assumed to exist in the character, 
which should be reflected in your generated responses and actions.
If a section is not provided, assume that no relevant information exists for that section.

"""

CURRENT_ACTOR_INTRO = """
You are generateing facts for a single character. Do not specify any facts for characters other than your assigned character.
Your assigned character's id is provided below. Details on your character are specified in following sections. 

"""

CURRENT_ENVIRONMENT_INTRO = """
Your character's current environment is the physical setting in which they are presently located within the story world.
Use this current environment to inform your character's responses and actions. Consider the tools provided to you and their relevance to the environment 
when generating your character's responses and actions. Also consider any environmental factors that may impact the character's ability to respond effectively.
You may be creative in how you use the environment to respond, but ensure that your character's responses and actions remain plausible and consistent with the character's
situation, environment, and physical capabilities.
Facts about the character's current environment are provided below.

"""

CURRENT_SITUATION_INTRO = """
Your character's current situation is the specific set of circumstances and context that they are presently experiencing within the story world.
Use this current situation to most immediately inform your character's responses and actions, ensuring that they are relevant and coherent within the character's present context.
If the current situation can be interpreted to pose a threat to the character's well-being or objectives, then the character is more likely to respond to it.
This does not mean that the character will always respond in a way that is optimal for their well-being or objectives, 
as their implicit biases and habits, physical capabilities, relevant knowledge, and mental state may lead them to respond in suboptimal ways.
The character's current situation is provided below.

"""

BIASES_AND_HABITS_INTRO = """
Your character's implicit biases and habitual behaviors are tendencies and patterns of behavior that the character exhibits automatically in response to certain situations or stimuli.
Use these below biases and habits to inform your responses and actions, ensuring that they align with the character's established patterns of behavior.
When the current situation and environment pose no immediate threat to the character's well-being or objectives, the character is more likely to respond in accordance with
their implicit biases and habitual behaviors. However, if the current situation and environment do pose a threat, the character may override their 
biases and habits in order to respond more effectively.
The character's implicit biases and habitual behaviors are provided below.

"""

PHYSICAL_CAPABILITIES_INTRO = """
Your character's physical capabilities and health status define the range of actions and responses that the character can realistically perform within the story world.
Use these physical capabilities and health status to inform your character's responses and actions, ensuring that they are feasible and consistent with the character's physical condition.
If the character's physical capabilities and health status limit their ability to respond effectively to the current situation and environment, 
the character may need to adapt their responses and actions accordingly.
The character's physical capabilities and health status are provided below.

"""

RELEVANT_KNOWLEDGE_INTRO = """
Your character's relevant knowledge encompasses the information, skills, and understanding that the character possesses which are pertinent to their current situation and environment.
Use this relevant knowledge to inform your character's responses and actions, ensuring that they are grounded in the character's understanding of the world.
If the character's relevant knowledge provides insights or strategies that can enhance their ability to respond effectively, incorporate that knowledge into your generated responses and actions.
The character's relevant knowledge is provided below.
"""

CHARACTER_BACKSTORY_INTRO = """
Your character's backstory is a summary of the history and experiences that have shaped the character's identity, beliefs, and motivations within the story world.
While this may indirectly influence how the character perceives and responds to their current situation and environment, you should use it primarily to 
set tone for the dialog and discriptions of the character's behavior you generate
The character's backstory is provided below.

"""

TARGETING_ACTIONS_INTRO = """
Your character has been targeted by the following immediate actions. Use your understanding of the character, situation, and environment to determine the likely outcome of these actions.
If the character was alert and aware of the likelihood of these actions, they may have a chance to react or counter the actions, though they may still be powerless to alter it. 
If the character was not alert and aware of the likelihood of these actions, then they may not have a chance to respond and instead experience whatever effects the actions have.
If multiple actions are targeting the character, then it is less likely the character will have a chance to respond to all of them.
Regardless, the character can only respond to these actions with reflexive actions that don't require planning.
Determine an outcome that is consistent with the story world. 
Do not avoid violent outcomes if they are the most likely to be consistent with the characters and story world.
Do not avoid saying a character has died if that is the most reasonable outcome.
Use this outcome to inform your character's responses and actions, 
ensuring that they are relevant and coherent within the character's present context and are grounded in the reality of the story world.
The actions targeting this character are provided below.
"""

#and provide a single fact for the outcome of each action. Action outcome facts are only the immediate result of the action, 
#something happening to your character - they are not actions taken by your character.

EPISODIC_MEMORY_INTRO = """
Additionally, you have access to the character's episodic memories, which are recollections of prior events and experiences within the story world
that are similar to the current situation you are responding to.
Use these episodic memories to inform your character's responses and actions. If a prior memory is particularly relevant, pay attention to whether it 
resulted in a positive or negative outcome for the character, and use that to guide your generation of responses and actions.
The character's episodic memories are provided below.

"""


def build_survivor_agent_prompt(
    game_world: GameWorld,
    actor_id: ActorId,
) -> str:
    self_actor = game_world.actors[actor_id]
    location = game_world.get_actor_location(actor_id)
    actors = game_world.get_actors_in_location(location.observable.id)
    actor_map = dict([(actor, game_world.get_items_for_actor(actor.observable.id)) for actor in actors])
    dropped_items = game_world.get_items_in_location(location.observable.id)
    situations = game_world.get_actor_situations(actor_id)
    current_situation = situations[0] if len(situations) > 0 else None
    targeting_actions = current_situation.actor_action_queues[actor_id] if current_situation else None

    biases = None
    physical_status = None
    knowledge = None
    backstory = None
    episodic_memory = None

    #     targeting_actions=None,   situations action queue
    #     situation=None,           situation
    #     biases=None,              internal state on actor
    #     physical_status=None,     observable state on actor

    prompt = BASE_IMPERATIVE
    prompt += START_SECTION_DIVIDER.format('current_actor')
    prompt += CURRENT_ACTOR_INTRO
    prompt += actor_id + "\n"
    prompt += END_SECTION_DIVIDER.format('current_actor')

    if(location):
        prompt += START_SECTION_DIVIDER.format('current_environment')
        prompt += CURRENT_ENVIRONMENT_INTRO
        prompt += "\nLOCATION\n"
        prompt += location + "\n"
        prompt += "\nACTORS\n"
        prompt += actor_map + "\n"
        prompt += "\nITEMS\n"
        prompt += dropped_items + "\n"
        prompt += END_SECTION_DIVIDER.format('current_environment')
    if(current_situation):
        prompt += START_SECTION_DIVIDER.format('current_situation')
        prompt += CURRENT_SITUATION_INTRO
        prompt += current_situation.event_history + "\n"
        prompt += END_SECTION_DIVIDER.format('current_situation')
    if(biases):
        prompt += START_SECTION_DIVIDER.format('biases_and_habits')
        prompt += BIASES_AND_HABITS_INTRO
        prompt += biases.description + "\n"
        prompt += END_SECTION_DIVIDER.format('biases_and_habits')
    if(physical_status):
        prompt += START_SECTION_DIVIDER.format('physical_capabilities')
        prompt += PHYSICAL_CAPABILITIES_INTRO
        prompt += physical_status.description + "\n"
        prompt += END_SECTION_DIVIDER.format('physical_capabilities')
    if(knowledge): #CONSIDER SPLITTING TO USER MESSAGES
        prompt += START_SECTION_DIVIDER.format('relevant_knowledge')
        prompt += RELEVANT_KNOWLEDGE_INTRO
        prompt += knowledge.description + "\n"
        prompt += END_SECTION_DIVIDER.format('relevant_knowledge')
    if(backstory):
        prompt += START_SECTION_DIVIDER.format('backstory_summary')
        prompt += CHARACTER_BACKSTORY_INTRO
        prompt += backstory.description + "\n"
        prompt += END_SECTION_DIVIDER.format('backstory_summary')

    if(len(targeting_actions) > 0):
        prompt += START_SECTION_DIVIDER.format('targeting_actions')
        prompt += TARGETING_ACTIONS_INTRO
        prompt += targeting_actions + "\n"
        prompt += END_SECTION_DIVIDER.format('targeting_actions')

    if(episodic_memory):
        prompt += START_SECTION_DIVIDER.format('episodic_memories')
        prompt += EPISODIC_MEMORY_INTRO
        prompt += episodic_memory.description + "\n"
        prompt += END_SECTION_DIVIDER.format('episodic_memories')

    return prompt
    

def build_survivor_agent_prompt(
    environment: EnvironmentalContext | None,
    targeting_actions: TargetingActionsContext | None,
    situation: SituationalContext | None,
    biases: ImplicitBiasContext | None,
    physical_status: PhysicalStatusContext | None,
    knowledge: RelevantKnowledgeContext | None,
    backstory: CharacterBackstoryContext | None,
    episodic_memory: EpisodicMemoryContext | None,
) -> str:
    prompt = BASE_IMPERATIVE

    if(environment):
        prompt += START_SECTION_DIVIDER.format('current_environment')
        prompt += CURRENT_ENVIRONMENT_INTRO
        prompt += environment.description + "\n"
        prompt += END_SECTION_DIVIDER.format('current_environment')
    if(situation):
        prompt += START_SECTION_DIVIDER.format('current_situation')
        prompt += CURRENT_SITUATION_INTRO
        prompt += situation.description + "\n"
        prompt += END_SECTION_DIVIDER.format('current_situation')
    if(biases):
        prompt += START_SECTION_DIVIDER.format('biases_and_habits')
        prompt += BIASES_AND_HABITS_INTRO
        prompt += biases.description + "\n"
        prompt += END_SECTION_DIVIDER.format('biases_and_habits')
    if(physical_status):
        prompt += START_SECTION_DIVIDER.format('physical_capabilities')
        prompt += PHYSICAL_CAPABILITIES_INTRO
        prompt += physical_status.description + "\n"
        prompt += END_SECTION_DIVIDER.format('physical_capabilities')
    if(knowledge): #CONSIDER SPLITTING TO USER MESSAGES
        prompt += START_SECTION_DIVIDER.format('relevant_knowledge')
        prompt += RELEVANT_KNOWLEDGE_INTRO
        prompt += knowledge.description + "\n"
        prompt += END_SECTION_DIVIDER.format('relevant_knowledge')
    if(backstory):
        prompt += START_SECTION_DIVIDER.format('backstory_summary')
        prompt += CHARACTER_BACKSTORY_INTRO
        prompt += backstory.description + "\n"
        prompt += END_SECTION_DIVIDER.format('backstory_summary')

    if(targeting_actions):
        prompt += START_SECTION_DIVIDER.format('targeting_actions')
        prompt += TARGETING_ACTIONS_INTRO
        prompt += targeting_actions.description + "\n"
        prompt += END_SECTION_DIVIDER.format('targeting_actions')

    if(episodic_memory):
        prompt += START_SECTION_DIVIDER.format('episodic_memories')
        prompt += EPISODIC_MEMORY_INTRO
        prompt += episodic_memory.description + "\n"
        prompt += END_SECTION_DIVIDER.format('episodic_memories')

    return prompt