from pydantic import BaseModel

class StoryCharacter(BaseModel):
    name: str
    age: int
    outward_appearance: str
    personality_summary: str
    backstory_summary: str

class StoryCharacterKnowledge(BaseModel):
    story_character: StoryCharacter
    knowledge: str