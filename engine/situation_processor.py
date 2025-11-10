from agents.agent_context import CharacterBackstoryContext, EnvironmentalContext, EpisodicMemoryContext, ImplicitBiasContext, PhysicalStatusContext, ReflexiveContext, RelevantKnowledgeContext, SituationalContext
from models.game_entities import Environment, ObservableEnvironment
from prompts.story_character_prompts import build_story_character_prompt


class SituationProcessor():
    def __init__(self, environment: ObservableEnvironment, situation_idx: int):
        self.environment = environment
        self.situation = environment.active_situations[situation_idx]

    def process_actor(self, actor_id: str):
        current_actor = self.environment.actors[actor_id]
        current_location = self.environment.locations[current_actor.state_history[-1].location_id]
        unresolved_actions = self.situation.actor_action_queues.pop(actor_id, [])

        reflex_context = ReflexiveContext() #TODO: from unresolved actions
        situation_context = SituationalContext(     self.situation.description, self.situation.event_history)
        env_context = EnvironmentalContext(         current_location.state_history[-1].description)
        biases = ImplicitBiasContext(               current_actor.biases)
        physical_status = PhysicalStatusContext(    current_actor.state_history[-1].description)
        backstory = CharacterBackstoryContext(      current_actor.back_story_summary),

        # use current actor and situation to look up episodic memory
        episodic_memory = EpisodicMemoryContext()

        # use current actor and situation to look up semantic memory
        knowledge = RelevantKnowledgeContext() 

        system_prompt = build_story_character_prompt(
            reflex=None,
            situation=None,
            environment=None,
            biases=None,
            physical_status=None,
            knowledge=None,
            backstory=None,
            episodic_memory=None,
        )

