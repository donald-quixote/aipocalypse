
from typing import List
from toon import encode_pydantic
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from models.core.episode import Environment, Episode
from prompts.prompt_fragments import PromptFragments
from prompts.prompt_generations import SurivorActionGeneration

class SurvivorAgentPrompt:

    GENERATED_TYPE = SurivorActionGeneration

    def build_prompt_messages(
        episode: Episode, 
        actor_id: str,
    ) -> List[BaseMessage]:

        PROMPT_HEADER = """
        You are an AI agent controlling a single character in a collaborative narrative simulation. 
        Your role is to generate two plot-advancing actions for your character based on their current episode and overarching campaign goals.
        """

        DECISION_FRAMEWORK = """
        Decision Framework:
            1. Assess Threat Level
                Immediate danger (attack, breach, fire): Actions should address or escape the threat
                Potential threat (distant sounds, shadows): Actions should be preparing to encounter or avoid the threat. 
                No active threat: Actions should work towards achieving the character's goals

            2. Apply Character State Modifiers
                The character's arousal, control, and health should inform what actions they would choose and are able to take.

            3. Check for Action Repetition
                Review this characters' last few actions. If they've repeated the same type of action twice without meaningful story change, do something different.
                Examples of repetition to avoid:
                    - INSPECT the same area multiple times
                    - Repeatedly TALK to warn others of the same threat
                    - Repeatedly TALK to discuss the same topic
                    - Repeatedly FIGHT with actions that will not incapacitate

            4. Prioritize Plot Advancement
                Every action should meaningfully change:
                    - Character locations or relationships
                    - Available information or resources
                    - Threats or opportunities
                    - Progress toward goals
        """

        WORKING_CONTEXT = """
        Your Character:
            {character_info}

        Environment:
            Current Landmark:    
                {landmark_name}

            Locations (within landmark):
                {location_info}

            Junctions:
                {junctions_info}

            Actors:
                {actors_info}

            Items:
                Held by actors: 
                    {held_items_info}
                Laying out: 
                    {dropped_items_info}

            Recent actions:
                {episode_action_info}
        
        Critical Instructions

        Read the recent actions - What just happened? Provide a synopsis.
        Identify immediate threats or opportunities - Does anything demand a response?
        Check your character's goals - If no immediate threat, what action moves toward the goals?
        Apply character state - Adjust actions and intensity based on health/arousal/control
        Choose actions that will have the most impact on your character and the rest of the episode.
        Verify no repetition - Are you doing something meaningfully different from your last actions?
        Provide two, distinctly different plans.
        Finally, select the more interesting and impactful plan and generate EXACTLY two actions.
        """

        actor = episode.actors[actor_id]
        env: Environment = episode #.get_actor_surroundings(actor_id)

        sys_prompt = PROMPT_HEADER
        sys_prompt += PromptFragments.SURVIVOR_ACTION_RULES
        sys_prompt += PromptFragments.SURVIVOR_ACTOR_STATE
        sys_prompt += DECISION_FRAMEWORK
        sys_prompt += WORKING_CONTEXT.format(
            character_info = encode_pydantic(actor),
            landmark_name = env.landmark.name,
            location_info = encode_pydantic(env.locations[actor.location_id]),
            junctions_info = encode_pydantic(list(env.junctions.values())),
            actors_info = encode_pydantic(env.get_observable_actors()),
            held_items_info = encode_pydantic(env.get_held_items()),
            dropped_items_info = encode_pydantic(env.get_dropped_items()),
            episode_action_info = encode_pydantic(env.actions),
        )
        sys_prompt += PromptFragments.CONFLICTING_CONTEXT_RULE

        return [
            SystemMessage(sys_prompt),
            HumanMessage(PromptFragments.ACTOR_USER_PROMPT)
        ]