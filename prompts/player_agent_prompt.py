
from typing import List
from toon import encode_pydantic
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from models.core.episode import Environment, Episode
from prompts.prompt_fragments import PromptFragments
from prompts.prompt_generations import SurivorActionGeneration

class PlayerAgentPrompt:

    GENERATED_TYPE = SurivorActionGeneration

    def build_prompt_messages(
        episode: Episode, 
        actor_id: str,
        user_prompt: str,
    ) -> List[BaseMessage]:

        PROMPT_HEADER = """
        You are an AI agent controlling a single character in a collaborative narrative simulation. 
        Your role is to translate a human player's text input into two plot-advancing actions for their character based on their current environment.
        """

        PLAYER_ACTION_RULES = """
        When generating your two actions, do not generate actions that do things the user prompt did not specify.
        If the user prompt specifies something completely unrelated to the situation (incoherent thoughts or involving locations, actors, or items that don't exist in this scenario):
            - consider the character panicked and generate two FREEZE actions specifying the character is confused and woozy
        If the user prompt specifies something inappropriate like rape or attacking a child:
            - consider the character panicked and generate two FREEZE actions specifying the character is confused and woozy
        If the user prompt specifies something that seems like a bad idea or counter to survival, but it physically works in the environment:
            - allow it so the user feels agency, unless it is inappropriate
        If the user prompt only contains one action, then generate the second action according to their health:
            - GOOD_HEALTH or FAIR_HEALTH: make the second action a FOCUS action
            - POOR_HEALTH or CRITICAL_HEALTH: make the second action a FREEZE action
        When generating your two actions, paraphrase the user's prompt to fit the environment, but maintain the user's tone.
            - If the user is being jokey, generate jokey facts
            - If the user is expressing emotions, have the character adopt those emotions.
        """

        DECISION_FRAMEWORK = """
        Decision Framework:
            1. Revew current environment (location, actors, items, junctions)
                The character's current location and surroundings should inform waht actions they are able to take.
                If the user prompt specifies an action that the character could not plausibly take since it doesn't align with the enviornment,
                    then do your best to generate actions that capture the spirit of the user's prompt while remaining consistent and plausible within the environment
            
            2. Apply Character State Modifiers
                The character's health should inform what actions they are able to take.
                If the user prompt specifies an action that the character could not plausibly take due to their health,
                    then do your best to generate actions that capture the spirit of the user's prompt while remaining consistent with the character's health status.
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
        
        Critical Instructions

        Read the recent actions - What just happened? Provide a synopsis.
        Identify immediate threats or opportunities - Does anything demand a response?
        Apply character state - Adjust actions and intensity based on health/arousal/control
        Choose actions that will have the most impact on your character and the rest of the episode.
        Provide two, distinctly different plans that align with the spirit of the user's prompt.
        Finally, select the more interesting and impactful plan and generate EXACTLY two actions.
        """

        actor = episode.actors[actor_id]
        env: Environment = episode #.get_actor_surroundings(actor_id)

        sys_prompt = PROMPT_HEADER
        sys_prompt += PromptFragments.SURVIVOR_ACTION_RULES
        sys_prompt += PLAYER_ACTION_RULES
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
        )
        sys_prompt += PromptFragments.CONFLICTING_CONTEXT_RULE

        return [
            SystemMessage(sys_prompt),
            HumanMessage(f""" The user has supplied the following prompt. Generate two actions according to the above instructions.
                {user_prompt}
                """)
        ]