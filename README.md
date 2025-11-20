<div style="text-align: center;">

![](assets/zombie_v_shark.jpg)

<i>
Can language-based agents make the zombie apocalypse more coherent than this?

[Zombi 2 - 1979](https://www.rottentomatoes.com/m/zombi_2)
</i>

</div>

# Aipocalypse
Modeling the zombie apocalypse through language-based agents

## What is this all about?
Aipocalypse is a for-funsies personal project where I will throw the AI kitchen sink at building an interactive narrative experience centered around a group of survivors during the zombie apocalypse.

I will learn stuff. Maybe other people will learn stuff. Hopefully the survivor agents will learn stuff (as I do plan to build a system modeling congitive processes for language-based agents).

## Where are we at?
We can generate an interesting "episode" with locations/actors/items, and then task llm agents with choosing and executing actions for the actors.
Running this in a round-robin fashion, we can watch the scene play out with reasonably plausible activities and reasonably accurate state management.

But... 
- it's sloooow... a single actor turn takes ~14s
  - there are both prompt-engineering techniques and game-loop techniques we can use to improve this.
- it's pure working context, no episodic or semantic memory yet
- there are a few rough edges around accuracy, though we're solid enough we can move off of prompt engineering and into other techniques to address this.

#### Current System
- Modeling simulation entities (locations, actors, items) in both pydantic models and Neo4j graph db
- Using TOON serialization at llm boundaries to reduce token usage
- Agent to generate a "landmark" location (e.g. a gas station, library, or other building you'd find on a map) with entities and save to graph db
- Agent to generate next action for an actor, given a current episode state
- Agent to evaluate the actor's actions and determine a plausible outcome
- Langgraph flow tying it together so we can process in a loop.

## Where are we going next?
- Actors' goals need to change as they achieve them or circumstances change. We'll start with a simple prompt engineering solution and test.
- Then we'll add a player actor in the mix with a simple interface and an agent to convert natural language inputs into concrete actions for the system.
- Once we have a packed experience together, then we'll turn to enriching actor agent behaviors.
  - I was inspired by Adam Lucek's [agentic memory](https://github.com/ALucek/agentic-memory) demonstration and plan to scaffold the basic blocks of episodic and semantic memory and learning. But, before we can model these, we need enough actor experiences to draw on.
    - for semantic memory, we'll need to start with generated backstories for survivors and for the game world and initial zombie outbreak, which we can index in a knowledge graph and expose to actor agents
    - and we'll need to generate multiple episodes so we have something to store in episodic memory :)
    - we'll likely need to break down gameworld generation to create each element in phases (e.g. backstory -> key actors/landmarks/objectives -> individual episodes then generated on-the-fly as needed with this context)

