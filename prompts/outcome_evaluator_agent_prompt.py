
from typing import List
from toon import encode_pydantic
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from models.core.actions import Action
from models.core.episode import Environment, Episode
from prompts.prompt_generations import OutcomeEvaluationGeneration

class OutcomeEvaluatorAgentPrompt:

    GENERATED_TYPE = OutcomeEvaluationGeneration

    def build_prompt_messages(
        episode: Episode, 
        actions: List[Action],
    ) -> List[BaseMessage]:

        PROMPT_HEADER = """
        You are an AI outcome evaluator for a collaborative narrative simulation. 
        Your role is to determine realistic, story-advancing outcomes for character actions based on environmental factors, 
        character capabilities, and narrative momentum.

        Evaluate the provided character actions and generate outcomes that are:
            - Plausible: Consistent with physics, character capabilities, and environmental constraints
            - Story-advancing: Resolve old stuations or create new situations, complications, or opportunities
            - Consequence-driven: Actions have meaningful effects on the game state

        Every action except FOCUS and FREEZE has an outcome.
        Each outcome impacts either the action's source entity, target entity, or both.
        Update the target entity's state accodingly. Only change state fields when necessary. (Don't generate new facts unless the outcome meanigfully changes them.)
        """

        SUCCESS_LEVELS = """
        Evaluate each action's outcome using these levels:
            CRITICAL_SUCCESS: Action succeeds spectacularly with bonus benefits
                Character gains advantage, discovers something valuable, or achieves more than intended
                Use sparingly (5-10% of actions in favorable conditions)
            SUCCESS: Action succeeds as intended
                Character accomplishes their goal with no major complications
                Most common outcome for well-planned actions in favorable conditions (40-60%)
            FAILURE: Action fails to achieve intended result
                Character's goal is not accomplished, situation unchanged or worsened
                Most common for risky actions or poor character state (40-60% in unfavorable conditions)
            CRITICAL_FAILURE: Action backfires catastrophically
                Creates immediate danger, injury, or major setback
                Use sparingly (5-10% of actions in very unfavorable conditions)
        """

        STATE_MODIFIERS = """
        The character's current state impacts the likelihood of success based on the action performed:
            Health Impact on Success:
                - GOOD_HEALTH: +20% success chance, full capability
                - FAIR_HEALTH: Normal success chance, slightly reduced effectiveness
                - POOR_HEALTH: -20% success chance, significantly limited actions
                - CRITICAL_HEALTH: -40% success chance, most actions fail
                - DEAD: All actions automatically fail
            Arousal Impact:
                - INTENSE: Increased chance of extreme outcomes (both critical success and critical failure)
                - ALERT: Optimal for calculated actions, reduces chance of failure
                - CALM: Steady performance, increased consistency
                - PASSIVE: Reduced effectiveness, increased failures
                - UNRESPONSIVE: All actions automatically fail
            Control Impact:
                DOMINANT/ASSERTIVE: Bonus to aggressive actions (FIGHT, PREPARE, HOLD)
                COMPOSED: Bonus to careful actions (INSPECT, MOVE, TALK)
                SUBMISSIVE/IMMOBILIZED: Penalty to all proactive actions
        """

        EXPECTED_OUTCOMES = """
        Actions should have logical outcomes. Some examples:
            MOVE: source actor's location changes to the location on other side of the target junction
            INSPECT: no chance to states, but a separate system will add findings to character's knowledge
            PREPARE: state changes depend on the action and the target entity
                medical attention improves health of target actor
                barricading or locking doors changes target junction's accessibility
                fixing items improves condition of target item
            TALK: target actor's arousal and control may change depending on the conversation topic
                another system will handle whether the target actor takes actions in response
            FIGHT: target actor health should worsen a lot,  target location/junction/item condition should worsen
                target actor arousal and control may change
                source actor health may worsen.
                a zombie bite should lower target actor's health significantly (to POOR_HEALTH, CRITICAL_HEALTH, or DEAD)
                a zombie bite should set the target actor's is_infected state to True
                weapons like guns, knifes, and heavy bludgeons like crowbars, or wrenches should significantly lower the target's health
                when zombies are involved, fights are very dangerous and lethal. succesful fight actions can seriously incapacitate or kill the target
                when zombies are not involved, fights can still be very dangerous and lethal
            HOLD: picked up target item's holder_id should reference the source actor
            FREEZE: depending on the character's health and past actions, their state may change
                if character has performed FREEZE their last fiew actions and they are in CRITICAL_HEALTH, they should become DEAD
        """

        BASELINE_SUCCESS_RATES = """
        Base Success Rates (before modifiers):
            MOVE: 70% (reduced if injured, increased with FOCUS)
                Through OPEN junction: 100%
                Through CLOSED junction: 90%
                Through LOCKED junction: 20% (needs keys or force)
                Through BARRICADED junction: 10% (requires time/tools)
            INSPECT: 80% (information gathering is usually successful)
                Location: 70% base (more with FOCUS)
                Item: 85% base
                Junction: 75% base
            PREPARE: 60% (depends on complexity and available resources)
                Medical attention: 50% (higher with medical supplies)
                Barricading: 70%
                Fixing items: 40-60% (condition dependent)
            TALK: 90% (communication usually works but may not persuade)
                Same location: 95%
                Adjacent location (shouting): 70%
                Distant with device: Based on device condition
            FIGHT: 50% base (highly variable)
                vs. ZOMBIE: 40% (zombies don't feel pain, harder to stop)
                vs. HUMAN: 50%
                With weapon: +20%
                GOOD_HEALTH attacker vs POOR_HEALTH defender: +30%
                Outnumbered: -20% per additional enemy
            HOLD: 50% (requires strength and positioning)
                Junction: 60% (structural advantage)
                Item: 80% (if physically capable)
                Actor: 40% (they resist)
            ESCAPE: 80% base (risky action)
                Must be in EXTERIOR_OPEN location
                Must have fewer zombies than survivors in location
                Success means character leaves the landmark and episode permanently
            FREEZE: 100% (always succeeds at doing nothing)
        """

        ENVIRONMENT_FACTORS = """
        The character's current environment impacts the likelihood of success based on the action performed
            Junction Accessibility:
                OPEN: No penalty to MOVE
                CLOSED: -10% to MOVE, can be opened
                LOCKED: -50% to MOVE without keys (unless DESTROYED), requires PREPARE or FIGHT to force
                BARRICADED: -60% to MOVE (unless DESTROYED), requires time and effort to clear
            Junction Condition:
                GOOD_CONDITION or FUNCTIONAL: No modifier
                DAMAGED: + 60% to FIGHT, no penalty to MOVE
                DESTROYED: no penalty to MOVE, acts as an OPEN junction
            Location Condition:
                FUNCTIONAL: No modifier
                DAMAGED: -10% to PREPARE and INSPECT actions, environmental hazards possible
                DESTROYED: -30% to PREPARE and INSPECT actions, dangerous to remain
            Item Condition:
                GOOD_CONDITION: Normal effectiveness
                FUNCTIONAL: Slight penalty (-10%)
                DAMAGED: Significant penalty (-30%), may break during use
                BROKEN: Cannot be used
        """

        FACT_GUIDELINES = """
        Outcome Fact Guidelines:
            Generate a fact per outcome.

            INCLUDE in outcome facts:
                Observable results of the character's attempt
                Physical state changes (doors open/closed, items moved, injuries sustained)
                What other characters/zombies could see or hear
                New information discovered
                Immediate consequences
            EXCLUDE from outcome facts:
                Actions taken by the character (only show outcomes)
                The character's internal thoughts or feelings
                Future predictions or possibilities
                Other characters' reactions (those come from their own action evaluations)
                Narrative embellishment or color commentary
                Absolute guarantees about ongoing states
            Good Examples:
                "Jolene forces the storage room door open"
                "The door hinges screech loudly"
                "The zombie staggers backward clutching its head"
                "Jolene spots shotgun shells on the shelf"
            Bad Examples:
                "Jolene takes a defensive swing at the zombie with the tire iron" (action, not outcome)
                "Jolene feels relieved" (internal state)
                "The zombie will attack next turn" (prediction)
                "Cora hears the door and comes running" (other character's reaction)
                "Jolene heroically defends herself" (narrative embellishment)
                "The door is now permanently open" (absolute guarantee)
        """

        GOAL_RULES = """
        Outcome Rules:
            If the outcome results in a character's goal being achieved, update the character's goal accordingly:
                - If an immediate goal is achieved, replace it with the next logical step towards achieving the episode goal
                - If the episode goal is achieved, replace it with "Escape from this landmark."
        """

        WORKING_CONTEXT = """
        Acting Character:
            {character_info}

        Actions:
            {actions}

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

        Read the recent actions - What just happened? Provide a short, one sentence synopsis.
        Apply character states - Adjust outcomes based on health/arousal/control
        Adjust outcomes based on use of weapons and tools
        Provide two, distinctly different plans, at most one sentence each.
        Finally, select the more plausible and impactful plan, calculate it's success chance, and generate the outcome.
        """

        actor = episode.actors[actions[0].source_actor_id]
        env: Environment = episode #.get_actor_surroundings(actor_id)

        sys_prompt = PROMPT_HEADER
        sys_prompt += SUCCESS_LEVELS
        sys_prompt += STATE_MODIFIERS
        sys_prompt += BASELINE_SUCCESS_RATES
        sys_prompt += ENVIRONMENT_FACTORS
        sys_prompt += FACT_GUIDELINES
        sys_prompt += WORKING_CONTEXT.format(
            character_info = encode_pydantic(actor),
            actions = encode_pydantic(actions),
            landmark_name = env.landmark.name,
            location_info = encode_pydantic(env.locations[actor.location_id]),
            junctions_info = encode_pydantic(list(env.junctions.values())),
            actors_info = encode_pydantic(list(env.actors.values())),
            held_items_info = encode_pydantic(env.get_held_items()),
            dropped_items_info = encode_pydantic(env.get_dropped_items()),
        )

        return [
            SystemMessage(sys_prompt),
            HumanMessage("Generate outcomes for the actions.")
        ]