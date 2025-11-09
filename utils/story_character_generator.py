import asyncio
import pickle
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import List, Dict
from dotenv import load_dotenv

from models.story_character import StoryCharacter, StoryCharacterKnowledge

load_dotenv(override=True)

class CharacterOutputs(BaseModel):
    story_characters: List[StoryCharacter] = []

class State(TypedDict):
    story_concept: str = ""
    story_characters: CharacterOutputs = CharacterOutputs()
    knowledge: List[StoryCharacterKnowledge] = []

class StoryCharacterGenrator():
    def __generate_characters(state: State) -> State:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)
        llm = llm.with_structured_output(CharacterOutputs)
        prompt = f"""
        You are creating a story cast for the concept: "{state["story_concept"]}".
        Generate exactly 5 unique characters. 
        For each character, include:
        - Name
        - Age
        - Outward appearance
        - Personality summary
        - Backstory summary

        Describe each character's personality completely independent of the other characters. 
        Assume no prior relationships between the characters.

        Outward appearance should be a detailed physical description that would be noticeable to someone meeting the character for the first time.
        Personality summary should capture key traits, behaviors, attitudes, and motivators.
        Backstory summary should provide context on the character's history, experiences, and defining moments that shaped who they are.

        Do not include any proposed plot or story points; focus solely on the character analysis.
        """
        state["story_characters"] = llm.invoke(prompt)
        return state

    async def __expand_character_knowledge_single(story_concept: str, story_character: StoryCharacter) -> tuple[StoryCharacter, str]:
        llm = ChatOpenAI(model="gpt-4o", temperature=0.8)
        prompt = f"""
        Generate a minimum 5000 word, detailed collection of facts for the following character.
        Character Name: {story_character.name}
        Character Age: {story_character.age}
        Outward Appearance: {story_character.outward_appearance}
        Personality Summary: {story_character.personality_summary}
        Backstory Summary: {story_character.backstory_summary}
        Story Concept: {story_concept}

        This should be a comprehensive collection of facts about the character's 
        life, motivations, fears, desires, and any other relevant facts that the character inwardly knows.
        Write in simple statements. Minimize prose. Avoid judgment statements or thematic interpretation. Only provide facts.
        Focus and quantity, consistency, and coherence of the facts. Do not elaborate beyond simple fact statements.
        Do not provide any summaries, bullet points, headers, or sections - only write in continuous text.
        Do not include any proposed plot or story points; focus solely on generating interesting and coherent facts about the character.

        Good example fact statements:
        - "She has a scar above her left eyebrow from a childhood accident."
        - "He dreams of traveling the world but is held back by his fear of flying."
        - "Her favorite food is sushi, which she discovered during a trip to Japan."
        """
        response = llm.invoke(prompt)
        return (story_character, response.content)

    async def __expand_character_knowledge(state: State) -> State:
        tasks = [
            StoryCharacterGenrator.__expand_character_knowledge_single(state["story_concept"], story_character)
            for story_character in state["story_characters"].story_characters
        ]
        results = await asyncio.gather(*tasks)
        state["knowledge"] = [StoryCharacterKnowledge(story_character=story_character,knowledge=knowledge) for story_character, knowledge in results]
        return state

    def __build_graph():
        graph = StateGraph(State)
        graph.add_node("generate_characters", StoryCharacterGenrator.__generate_characters)
        graph.add_node("expand_knowledge", StoryCharacterGenrator.__expand_character_knowledge)

        graph.set_entry_point("generate_characters")
        graph.add_edge("generate_characters", "expand_knowledge")
        graph.add_edge("expand_knowledge", END)

        return graph.compile()
    
    def __init__(self):
        self.flow = StoryCharacterGenrator.__build_graph()

    async def run(self, story_concept: str):
        initial_state: State = {
            "story_concept": story_concept,
            "story_characters": [],
            "knowledge": [],
        }

        final_state = await self.flow.ainvoke(initial_state)

        with open("story_characters.pkl", "wb") as f:
            pickle.dump(final_state["knowledge"], f)

# ----- Run -----
if __name__ == "__main__":
    generator = StoryCharacterGenrator()
    asyncio.run(generator.run("A dystopian zombie survival narrative"))
