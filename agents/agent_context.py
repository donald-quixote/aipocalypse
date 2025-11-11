from pydantic import BaseModel

class TargetingActionsContext(BaseModel):
    description: str

class SituationalContext(BaseModel):
    description: str

class EnvironmentalContext(BaseModel):
    description: str

class ImplicitBiasContext(BaseModel):
    description: str

class PhysicalStatusContext(BaseModel):
    description: str

class RelevantKnowledgeContext(BaseModel):
    description: str

class CharacterBackstoryContext(BaseModel):
    description: str

class EpisodicMemoryContext(BaseModel):
    description: str
