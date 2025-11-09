# Aipocalypse
Modeling the zombie apocalypse through agentic processes

## What is this all about?
Aipocalypse is a for-funsies personal project where I will throw the AI kitchen sink at building an interactive narrative experience centered around a group of survivors during the zombie apocalypse.

I will learn stuff. Maybe other people will learn stuff. Hopefully the survivor agents will learn stuff (as I do plan to build a system modeling congitive processes for language-based agents).

## Where are we at?
- Started simple with my first ever LangGraph flow to generate a candidate set of agent personalities. This is more scaffolding right now - setting a model for a story character and loosely considering the kinds of knowledge that a character will have about themself and the kinds of knowledge they will have about others. 

## Where are we going next?
- I was inspired by Adam Lucek's [agentic memory](https://github.com/ALucek/agentic-memory) demonstration and plan to scaffold the basic blocks of episodic and semantic memory and learning. 
  - We'll start with just carrying on coherent conversation with a single agent while managing episodic and semantic memory
  - But then see what the game loop looks like to get two agents carrying a conversation while managing episodic and semantic memory
  - Considering whether to continue using LangGraph or to try OpenAI Agents SDK for the core.
- And then will take this a step further using [GraphRAG](https://microsoft.github.io/graphrag/)