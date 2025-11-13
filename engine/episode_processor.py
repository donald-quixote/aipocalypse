import copy
import time
from typing import NoReturn
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from models.game_state import GameWorld, GameWorldManager, Episode
from models.generations import ActorAgentGeneration
from prompts.actor_agent_prompts import build_actor_agent_prompt
from prompts.actor_agent_prompts_claude import build_actor_agent_prompt_claude


class EpisodeProcessor():
    def __init__(self, episode_idx: int):
        self.episode_idx = episode_idx
        self.actor_llm = ChatOpenAI(temperature=0.7, model="gpt-4.1").with_structured_output(ActorAgentGeneration)

    def process_actor(self, actor_id: str) -> NoReturn:

        print("deepcopy")
        game_world_copy: GameWorld = copy.deepcopy(GameWorldManager.get())
        episode: Episode = game_world_copy.active_episodes[self.episode_idx]

        # system_prompt = build_actor_agent_prompt(
        system_prompt = build_actor_agent_prompt_claude(
            game_world_copy,
            actor_id
        )
        #     biases=None,              internal state on actor
        #     physical_status=None,     observable state on actor
        #     knowledge=None,           semantic store lookup
        #     backstory=None,           internal state on actor
        #     episodic_memory=None,     episodic store lookup

        messages = [
            SystemMessage(system_prompt),
            HumanMessage("generate facts for your actor according to the above instructions")
        ]
        # print(system_prompt)

        # run actor agent
        print("call llm")
        llm_response = self.actor_llm.invoke(messages)
        actor_response = ActorAgentGeneration.model_validate(llm_response)

        print("update game world")
        # update episode history
        episode.event_history += actor_response.resulting_outcomes + actor_response.resulting_actions + actor_response.resulting_events

        # queue pending actions
        for action in actor_response.resulting_actions:
            for target_actor_id in action.target_actor_ids:
                episode.get_actor_targeting_actions(target_actor_id).append(action)

        # queue pending events
        for event in actor_response.resulting_events:
            for target_actor_id in action.target_actor_ids:
                episode.get_actor_targeting_actions(target_actor_id).append(event)
        
        # update actor states
        for update in actor_response.new_actor_states:
            game_world_copy.get_actor(update.key).state_history.append(update.value)

        # update location states
        for update in actor_response.new_location_states:
            game_world_copy.get_location(update.key).state_history.append(update.value)

        # update item states
        for update in actor_response.new_item_states:
            game_world_copy.get_item(update.key).state_history.append(update.value)

        # pop processed actions off the episode
        episode.remove_processed_actions(actor_id)

        #update the global game world
        print("commit")
        GameWorldManager.set(game_world_copy)

    def process(self, limit: int = 10, delay = 0):
        
        keep_processing = True
        actor_idx = 0
        remaining = limit
        while keep_processing and remaining > 0:
            print(f"{remaining} executions remaining")
            episode: Episode = GameWorldManager.get().active_episodes[self.episode_idx]
            if len(episode.actor_ids) <= 0:
                keep_processing = False
            else:
                actor_id = episode.actor_ids[actor_idx]
                self.process_actor(actor_id)
                actor_idx = (actor_idx + 1) % len(episode.actor_ids)
                remaining -= 1
                if delay > 0:
                    time.sleep(delay)
