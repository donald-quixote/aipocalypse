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
- Started simple with my first ever LangGraph flow to generate a candidate set of agent personalities. This is more scaffolding right now - setting a model for a story character and loosely considering the kinds of knowledge that a character will have about themself and the kinds of knowledge they will have about others. 

## Where are we going next?
- I was inspired by Adam Lucek's [agentic memory](https://github.com/ALucek/agentic-memory) demonstration and plan to scaffold the basic blocks of episodic and semantic memory and learning. 
  - We'll start with just carrying on coherent conversation with a single survivor agent while managing episodic and semantic memory
  - But then see what the loop looks like to add a second surivor agent into the mix
  - and consider how this scales to a party of five survivors
  - Considering whether to continue using LangGraph or to try OpenAI Agents SDK for the core.
- And then will take this a step further using [GraphRAG](https://microsoft.github.io/graphrag/) to enhance recall
  - None of this is taking latency into account just yet. Just want to wire things up and see if I can find some satisfaction with the agent behaviors

## What other grand ideas are there?
- It's a zombie outbreak simulation... there will be zombies...
  - It's easy to accidentally make agents less coherent... Let's do it on purpose!
- I'd like to explore modeling emotional states. I've never experienced a zombie outbreak, but I would imagine some people... react more poorly than others.
  - Fight/flight/freeze behaviors where agents may form a logical plan but fail to act on it under stress
  - Essentially, can we successfully mimic physiological responses?
- Encounters! I don't want zombie outbreak survivors to plan my tax filing. I want them to plot their actions to stay alive during zombie encounters.
  - We'll need some form of simple game mechanics
  - And a game loop
  - And to consider how agents might exercise their episodic memory and semantic memory in order to reach their goals.
  - while having their emotional state enhance or hinder their planning performance
- And it's not all LLMs!
  - skill checks could be tests of regression model prediction accuracy. Why not!
  - MCP to expose interactive elements in the environment to survivor agents? Sure!
  - Weapons and tools are... wait for it... tools.

## Is this all just naive musings?
Maybe! But, learning is fun!
