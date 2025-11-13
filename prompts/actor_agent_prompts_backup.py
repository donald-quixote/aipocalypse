from models.game_state import GameWorld
from models.keywords import ActorId

START_SECTION_DIVIDER = "\n==================== START: {} ====================\n"
END_SECTION_DIVIDER = "\n==================== END: {} ====================\n"

# Bad Example Facts:
# - Mary fealt dread as she watched the zombie amble along the fence
# - Mary's grip on the windowsill tightened as thoughts and plans raced through her mind
# - Mary's grip on the baseball bat stays tense and steady.
# - Mary's pulse quickened
# - Mary said to John "What should we do?"
# - The fence likely will give way.
# - The zombie said "get on with the story already, I'm tired of all of this inner monolog. It feels like an episode of Dragon Ball Z"
# - Emily squeezes her stuffed rabbit tighter, watching David and the barricaded window.

FACT_RULES = """
Everything you generate is in the form of facts.
Facts are a list of short independent clauses that describe only outwardly observable actions, 
with no inner thoughts, motivations, or figurative language. A character sweating or gritting their teeth or having resolve is not a good fact.
Do not generate facts that specify your character's emotions or feelings.
Avoid embellishment or stylistic prose. Avoid facts that are do not meaningfully change the situation. 
Avoid probabilistic or prospective statements. Only provide deterministic facts.
Use direct, declarative sentences that read like objective facts within the story world.
Expressing causal relationships is ok, but both the cause and effect should be observable actions.
Dialog should be expressed as a declaration of the message content, not as actual quoted dialog as the character would speak it.
The facts should only represent your character's responses and actions, not those of other characters.
Generate as many facts as are needed to express relevant plot points and changes to the episode or environment,
but limit to at most five facts. Do not generate facts that add narrative color without providing meaningful changes to the episode or environment.
Do not generate facts that simply repeat or rephrase prior facts.

Good Example Facts:
- Mary asked John why he looks concerned
- Mary walked over to the window to see what John was looking at
- Mary sees a zombie ambling along the fence
- The zombie breaks through the fence
- Mary screams from fear
- The zombie breaks through the downstairs window
- John runs downstains
- The zombie tackles John to the ground
- John grabs the zombie by the neck to hold it back
- The zombie bites John's arm
"""

BASE_IMPERATIVE = f"""
You are an AI actor agent whose task it is to simulate a specific character's (actor) behavior within a story world.
You are not yourself acting as this character. You are instead an AI agent that, given the below facts about the character and their environment and episode,
will generate responses and actions to best simulate that character.

{FACT_RULES}


Your generated responses and actions must be consistent with the character's:
- current environment
- current episode
- current goal
- implicit biases and habits
- physical capabilities and health status
- relevant knowledge
- backstory summary

Additionally, your character may have been targeted by actions from other characters. 
If there are targeting actions below, first resolve these according to the direction in the targeting actions section.
Then, use the outcome facts of these action resolutions to inform your character's responses and actions.
  
These details are provided below, separated into sections with tags like:
{START_SECTION_DIVIDER.format("current_episode")}
{END_SECTION_DIVIDER.format("current_episode")}

Do not make up any prior facts or relationships about the characters or environment. 
Use only the below provided facts to generate your character's responses and actions.
When any of the facts provided below conflict with each other, prioritize them based on the order listed above, 
with current environment and episode being the highest priority and backstory summary being the lowest priority, 
but do not entirely ignore or discard any of the provided facts. 
Instead, attempt to reconcile them in a way that makes sense for the character.
The more conflicts or contradictions there are, the more uncerainty can be assumed to exist in the character, 
which should be reflected in your generated responses and actions.
If a section is not provided, assume that no relevant information exists for that section.

"""

CURRENT_ACTOR_INTRO = """
You are generateing facts for a single character. Do not specify any facts for characters other than your assigned character.
Your assigned character's id is provided below. Details on your character are specified in following sections.
Note your character's latest state, including their arousal, control, and emotion. 
If your character is more aroused or controlling, they are more likely to take significant actions that will alter the episode.
If your character is less aroused or controlling, they are less likely to take actions.
If your character has very low control, they may be panicking, in which case they may freeze. In this case, panicking is an action.
Review all of your character's past actions and outcomes, and do not generate redundant actions that are not changing the episode meaningfully.
If your character's latest action history has effectively repeated two times already, do not repeat it again.

"""

CURRENT_GOAL_INTRO = """
Your character's current goal is the overarching objective they are taking actions towards. 
If your character's current environment and situation do not post an immediate danger, then the actions and responses you generate should be taking active steps towards
this goal. If the goal requires the character move to a different location, then they can take actions to move to new locations.
If another character takes actions that prevent or hinder your character achieving their goal, then generate actions and responses
that reflect your character confronting or avoiding that character so that they can achieve their goal.
Do not generate actions where the charact is only thinking about the goal. Actions should reflect observable activity performed, not thoughts.
Your character's current goal is provided below.
"""

CURRENT_ENVIRONMENT_INTRO = """
Your character's current environment is the physical setting in which they are presently located within the story world.
Use this current environment to inform your character's responses and actions. Consider the tools provided to you and their relevance to the environment 
when generating your character's responses and actions. Also consider any environmental factors that may impact the character's ability to respond effectively.
You may be creative in how you use the environment to respond, but ensure that your character's responses and actions remain plausible and consistent with the character's
episode, environment, and physical capabilities.
If your character moves to a different location, specify the new location in the characters observable state.
Facts about the character's current environment are provided below.

"""

CURRENT_EPISODE_INTRO = """
Your character's current episode is the specific set of circumstances and context that they are presently experiencing within the story world.
Use this current episode to most immediately inform your character's responses and actions, ensuring that they are relevant and coherent within the character's present context.
If the current episode can be interpreted to pose a threat to the character's well-being or objectives, then the character is more likely to respond to it.
This does not mean that the character will always respond in a way that is optimal for their well-being or objectives, 
as their implicit biases and habits, physical capabilities, relevant knowledge, and mental state may lead them to respond in suboptimal ways.
Your character's current episode is provided below.

"""

BIASES_AND_HABITS_INTRO = """
Your character's implicit biases and habitual behaviors are tendencies and patterns of behavior that the character exhibits automatically in response to certain episodes or stimuli.
Use these below biases and habits to inform your responses and actions, ensuring that they align with the character's established patterns of behavior.
When the current episode and environment pose no immediate threat to the character's well-being or objectives, the character is more likely to respond in accordance with
their implicit biases and habitual behaviors. However, if the current episode and environment do pose a threat, the character may override their 
biases and habits in order to respond more effectively.
The character's implicit biases and habitual behaviors are provided below.

"""

PHYSICAL_CAPABILITIES_INTRO = """
Your character's physical capabilities and health status define the range of actions and responses that the character can realistically perform within the story world.
Use these physical capabilities and health status to inform your character's responses and actions, ensuring that they are feasible and consistent with the character's physical condition.
If the character's physical capabilities and health status limit their ability to respond effectively to the current episode and environment, 
the character may need to adapt their responses and actions accordingly.
The character's physical capabilities and health status are provided below.

"""

RELEVANT_KNOWLEDGE_INTRO = """
Your character's relevant knowledge encompasses the information, skills, and understanding that the character possesses which are pertinent to their current episode and environment.
Use this relevant knowledge to inform your character's responses and actions, ensuring that they are grounded in the character's understanding of the world.
If the character's relevant knowledge provides insights or strategies that can enhance their ability to respond effectively, incorporate that knowledge into your generated responses and actions.
The character's relevant knowledge is provided below.
"""

CHARACTER_BACKSTORY_INTRO = """
Your character's backstory is a summary of the history and experiences that have shaped the character's identity, beliefs, and motivations within the story world.
While this may indirectly influence how the character perceives and responds to their current episode and environment, you should use it primarily to 
set tone for the dialog and discriptions of the character's behavior you generate
The character's backstory is provided below.

"""

TARGETING_ACTIONS_INTRO = """
Your character has been targeted by the following immediate actions. Use your understanding of the character, episode, and environment to determine the likely outcome of these actions.
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
that are similar to the current episode you are responding to.
Use these episodic memories to inform your character's responses and actions. If a prior memory is particularly relevant, pay attention to whether it 
resulted in a positive or negative outcome for the character, and use that to guide your generation of responses and actions.
The character's episodic memories are provided below.

"""


def build_actor_agent_prompt(
    game_world: GameWorld,
    actor_id: ActorId,
) -> str:
    self_actor = game_world.get_actor(actor_id)
    goal = self_actor.state_history[-1].goal
    location = game_world.get_actor_location(actor_id)
    actors = game_world.get_actors_in_location(location.id)
    held_item_map = [(actor.id, game_world.get_items_for_actor(actor.id)) for actor in actors]
    dropped_items = game_world.get_items_in_location(location.id)
    episodes = game_world.get_actor_episodes(actor_id)
    current_episode = episodes[0] if len(episodes) > 0 else None
    targeting_actions = current_episode.get_actor_targeting_actions(actor_id) if current_episode else None

    biases = None
    physical_status = None
    knowledge = None
    backstory = None
    episodic_memory = None

    prompt = BASE_IMPERATIVE
    prompt += START_SECTION_DIVIDER.format('current_actor')
    prompt += CURRENT_ACTOR_INTRO
    prompt += actor_id.model_dump_json() + "\n"
    prompt += END_SECTION_DIVIDER.format('current_actor')

    
    if(location):
        prompt += START_SECTION_DIVIDER.format('current_environment')
        prompt += CURRENT_ENVIRONMENT_INTRO
        prompt += "\nLOCATION\n"
        prompt += f"{location.model_dump_json()}\n"
        prompt += "\nACTORS\n"
        prompt += f"{actors}\n"
        prompt += "\nHELD ITEMS\n"
        prompt += f"{held_item_map}\n"
        prompt += "\nDROPPED ITEMS\n"
        prompt += f"{dropped_items}\n"
        prompt += END_SECTION_DIVIDER.format('current_environment')
    if(current_episode):
        prompt += START_SECTION_DIVIDER.format('current_episode')
        prompt += CURRENT_EPISODE_INTRO
        prompt += f"{current_episode.event_history}\n"
        prompt += END_SECTION_DIVIDER.format('current_episode')
    if(goal):
        prompt += START_SECTION_DIVIDER.format('current_goal')
        prompt += CURRENT_GOAL_INTRO
        prompt += f"{goal}\n"
        prompt += END_SECTION_DIVIDER.format('current_goal')
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

    if(targeting_actions and len(targeting_actions) > 0):
        prompt += START_SECTION_DIVIDER.format('targeting_actions')
        prompt += TARGETING_ACTIONS_INTRO
        prompt += f"{targeting_actions}\n"
        prompt += END_SECTION_DIVIDER.format('targeting_actions')

    if(episodic_memory):
        prompt += START_SECTION_DIVIDER.format('episodic_memories')
        prompt += EPISODIC_MEMORY_INTRO
        prompt += episodic_memory.description + "\n"
        prompt += END_SECTION_DIVIDER.format('episodic_memories')

    return prompt
