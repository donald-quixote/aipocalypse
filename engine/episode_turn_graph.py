from __future__ import annotations

from typing import Dict, Iterable, List, NotRequired, Sequence, TypedDict

from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from models.core.actions import Action, Outcome
from models.core.entities import (
    ActorEntity,
    ItemEntity,
    JunctionEntity,
    LocationEntity,
)
from models.core.episode import Episode
from models.core.enums import ActorHealth, ActorType
from models.neomodel.queries_neomodel import NeoModelQueries
from prompts.outcome_evaluator_agent_prompt import OutcomeEvaluatorAgentPrompt
from prompts.prompt_generations import (
    OutcomeEvaluationGeneration,
    SurivorActionGeneration,
    ZombieActionGeneration,
)
from prompts.survivor_agent_prompt import SurvivorAgentPrompt
from prompts.zombie_agent_prompt import ZombieAgentPrompt

EpisodeEntity = ActorEntity | LocationEntity | JunctionEntity | ItemEntity


class EpisodeTurnState(TypedDict):
    episode: Episode
    actor_id: str
    actions: NotRequired[List[Action]]
    outcomes: NotRequired[List[Outcome]]


class EpisodeTurnGraph:
    """LangGraph flow that processes a single actor turn."""

    def __init__(
        self
    ) -> None:
        base_model = ChatOpenAI(model="gpt-4.1", temperature=0.9)

        self.survivor_llm = base_model.with_structured_output(SurivorActionGeneration)
        self.zombie_llm = base_model.with_structured_output(ZombieActionGeneration)
        self.evaluator_llm = base_model.with_structured_output(OutcomeEvaluationGeneration)

        builder = StateGraph(EpisodeTurnState)
        builder.add_node("generate_actions", self._generate_actions)
        builder.add_node("evaluate_actions", self._evaluate_actions)
        builder.add_node("apply_outcomes", self._apply_outcomes)

        builder.set_entry_point("generate_actions")
        builder.add_edge("generate_actions", "evaluate_actions")
        builder.add_edge("evaluate_actions", "apply_outcomes")
        builder.add_edge("apply_outcomes", END)

        self.graph = builder.compile()

    def invoke(
        self,
        episode: Episode,
        actor_id: str,
        config: RunnableConfig | None = None,
    ) -> EpisodeTurnState:
        """Runs the compiled LangGraph for the provided actor turn."""
        initial_state: EpisodeTurnState = {
            "episode": episode,
            "actor_id": actor_id,
        }
        return self.graph.invoke(initial_state, config)

    def _generate_actions(
        self,
        state: EpisodeTurnState,
        _: RunnableConfig | None = None,
    ) -> EpisodeTurnState:
        episode = state["episode"]
        actor_id = state["actor_id"]
        actor = episode.actors[actor_id]
        if(actor.health == ActorHealth.DEAD):
            return state

        match actor.type:
            case ActorType.ZOMBIE:
                messages = ZombieAgentPrompt.build_prompt_messages(episode, actor_id)
                generation = self.zombie_llm.invoke(messages)
                actions = [generation.action]
            case ActorType.HUMAN:
                messages = SurvivorAgentPrompt.build_prompt_messages(episode, actor_id)
                generation = self.survivor_llm.invoke(messages)
                actions = list(generation.actions)

        episode.actions.extend(actions)
        return {**state, "episode": episode, "actions": actions}

    def _evaluate_actions(
        self,
        state: EpisodeTurnState,
        _: RunnableConfig | None = None,
    ) -> EpisodeTurnState:
        episode = state["episode"]
        actions = state.get("actions", [])
        if not actions:
            return state

        messages = OutcomeEvaluatorAgentPrompt.build_prompt_messages(episode, actions)
        generation = self.evaluator_llm.invoke(messages)
        outcomes = list(generation.outcomes)
        episode.outcomes.extend(outcomes)

        return {**state, "episode": episode, "outcomes": outcomes}

    def _apply_outcomes(
        self,
        state: EpisodeTurnState,
        _: RunnableConfig | None = None,
    ) -> EpisodeTurnState:
        episode = state["episode"]
        outcomes = state.get("outcomes", [])
        if not outcomes:
            return state

        updated_entities = apply_outcomes_to_episode(episode, outcomes)
        persist_entities(updated_entities.values())
        return {**state, "episode": episode}


def apply_outcomes_to_episode(
    episode: Episode,
    outcomes: Sequence[Outcome],
) -> Dict[str, EpisodeEntity]:
    """Updates episode entities based on the evaluator outcomes."""
    updated_entities: Dict[str, EpisodeEntity] = {}
    for outcome in outcomes:
        for entity in [
            outcome.resulting_source_entity_status,
            outcome.resulting_target_entity_status,
        ]:
            if entity is None:
                continue
            apply_entity_update(episode, entity)
            updated_entities[entity.uid] = entity
    return updated_entities


def apply_entity_update(episode: Episode, entity: EpisodeEntity) -> None:
    """Applies a single entity update to the in-memory episode."""
    match entity:
        case ActorEntity():
            episode.actors[entity.uid] = entity
        case LocationEntity():
            episode.locations[entity.uid] = entity
        case JunctionEntity():
            episode.junctions[entity.uid] = entity
        case ItemEntity():
            episode.items[entity.uid] = entity
        case _:
            raise ValueError(f"Unsupported entity type: {type(entity)}")


def persist_entities(entities: Iterable[EpisodeEntity]) -> None:
    """Persists updated entities into Neo4j."""
    actors: List[ActorEntity] = []
    locations: List[LocationEntity] = []
    junctions: List[JunctionEntity] = []
    items: List[ItemEntity] = []

    for entity in entities:
        match entity:
            case ActorEntity():
                actors.append(entity)
            case LocationEntity():
                locations.append(entity)
            case JunctionEntity():
                junctions.append(entity)
            case ItemEntity():
                items.append(entity)

    if actors:
        NeoModelQueries.create_or_update_actors(*actors)
    if locations:
        NeoModelQueries.create_or_update_locations(*locations)
    if junctions:
        NeoModelQueries.create_or_update_junctions(*junctions)
    if items:
        NeoModelQueries.create_or_update_items(*items)
