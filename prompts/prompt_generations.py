

from typing import List
from pydantic import BaseModel

from models.core.actions import Action, Outcome


class ActorPlanGeneration(BaseModel):

    """A summary of recent events, in one sentence"""
    synopsis: str

    """A description of one possible plan, in one sentence"""
    plan_1: str
    """A description of another, different, possible plan, in one sentence"""
    plan_2: str

    

class SurivorActionGeneration(ActorPlanGeneration):

    """The decided upon actions. Survivors should generate EXACTLY two actions"""
    actions: List[Action]

class ZombieActionGeneration(ActorPlanGeneration):

    """The decided upon action. Zombies should generate EXACTLY one action"""
    action: Action

class OutcomeEvaluationGeneration(BaseModel):

    """A summary of action performed, in one sentence"""
    synopsis: str

    """A description of one possible plan for evaluation, in one sentence"""
    evaluation_plan_1: str
    """A description of another, different, possible evaluation, in one sentence"""
    evaluation_plan_2: str

    """The decided upon outcomes"""
    outcomes: List[Outcome]
