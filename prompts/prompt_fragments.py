    
class PromptFragments:
    ACTION_PROPERTIES = """
    Properties of Actions:
        - uid: formatted as 'action_xxxxxxx' where xxxxxxx is an integer between 1000000 and 9999999
        - type: there are a fixed set of types of actions that must be chosen from. The list is provided below
        - location_id: the location where the action is performed
        - source_actor_id: the actor performing the action
        - target_entity_id: the identifier of what the action is directed towards
        - target_entity_type: the type of what the action is directed towards. This could be an ACTOR, LOCATION, JUNCTION, or ITEM. It should align with the target entity id prefix.
        - fact: a short, declarative statement describing the observable action. This fact will be used by a separate system to generate narrative prose.
            INCLUDE:
            Physical actions (walk, grab, push, break, run, hide)
            Reactions to the other actors
            Speech content as declarations: "X tells Y that [message]" or "X asks Y about [topic]"
            Attempts to achieve something

            EXCLUDE:
            Direct physical effects: "The door breaks," "The glass shatters"
            Outcomes of the action - these will be handled by another system.
            Internal thoughts, feelings, or motivations
            Figurative language or narrative flourish
            Repetition of prior actions without meaningful change
            Mention of held items not actively being used
            Probabilistic statements ("might," "could")
            Reactions by other characters

            Good Example Facts
                - Mary walks from the living room to the kitchen
                - Mary opens the back door
                - Mary sees three zombies in the yard
                - Mary shouts a warning to the group
                - Mary slams the door shut

            Bad Example Facts
                - Mary feels anxious (internal state)
                - Mary's heart races (not meaningfully observable)
                - Mary tightens her grip on the baseball bat (not meaningfully using the item)
                - Mary courageously decides to act (motivation/judgment)
                - Mary might check the door (probabilistic)
                - The zombies look menacing (narrative color)
    """

    ACTION_MOVE = """
        - MOVE: the character will attempt to move from one LOCATION to a connected LOCATION via a target JUNCTION (door, window, gate, etc)
    """
    ACTION_INSPECT = """
        - INSPECT: the character will look closely at something
            - inspecting a location is searching it
            - inspecting an item is checking its state or determining what it is
            - inspect a junction is checking if a door or window is locked, or peeking through it
    """
    ACTION_PREPARE = """
        - PREPARE: the character will actively work on something to improve their situation
            - the target must be in same location as the source actor, or it must be a junction connected to that location
            - target items must have holder_id equal to the source actor
            - preparing on an actor could be giving medical attention or helping them
            - preparing on an item could be fixing, configuring or using
            - preparing on a location could picking up a mess or clearing space
            - preparing on a junction could be barricading a door or window, removing a barricade, or preparing to act when a door opens
    """
    ACTION_TALK = """
        - TALK: the character will talk to someone either in the same location as them, in a nearby location (by shouting), or in a distant location if using a communication device
    """
    ACTION_FIGHT = """
        - FIGHT: the character will attack or defend in combat
            - the target must be in same location as the source actor, or it must be a junction connected to that location
            - otherwise there are no limits on which actors can fight which
            - fighting a location, item, or junction is actively trying to damage or destroy it
    """
    ACTION_HOLD = """
        - HOLD: the character will physically work to hold or contain a large item or another actor
            - the target must be in same location as the source actor, or it must be a junction connected to that location
            - holding an actor is attempting to prevent them from moving or fighting
            - holding a junction is attempting to keep a door or window shut
            - holding an item is picking it up (if physically able)
    """
    ACTION_FREEZE = """
        - FREEZE: the character will not take any useful action
            - this is only for characters that are panicking or unresponsive.
    """
    ACTION_ESCAPE = """
        - ESCAPE: the character will attempt to leave the landmark
            - escape can only be performed when the character is in an EXTERIOR_OPEN location
            - escape can only be performed when there are less zombies than survivors in the location
    """
    ACTION_FOCUS = """
        - FOCUS: the character will put all of their attention into the other action they selected, increasing their chance for successful outcomes
    """

    SURVIVOR_ACTION_RULES = f"""
    Generate exactly two actions that represent your character's next actions in the story. 
    These actions will be evaluated by a separate system to determine their outcomes.

    {ACTION_PROPERTIES}

    Types of Actions:
    {ACTION_MOVE}
    {ACTION_INSPECT}
    {ACTION_PREPARE}
    {ACTION_TALK}
    {ACTION_FIGHT}
    {ACTION_HOLD}
    {ACTION_FREEZE}
    {ACTION_ESCAPE}
    {ACTION_FOCUS}

    The two actions may compliment or support each other. For example:
        - two MOVE actions could be considered running, attempting to move two locations away
        - performing FOCUS along with another action increases the chance for a desirable outcome
            - FOCUS + FIGHT: fights with more awareness and skill
            - FOCUS + PREPARE: increases the chance they succeed at the action
            - FOCUS + MOVE: move as quietly or carefully as they can to not draw attention
            - FOCUS + TALK: fully engaged and attentive in a conversation
        - two FREEZE actions is taking no action
        - performing FREEZE along with another action is doing the task with less energy or urgency

    The two actions may also be distinct, separate, and done simultaneously. For example:
        - MOVE + INSPECT: pay close attention when cautiously entering a new location
        - MOVE + FIGHT: charge into another location and attack something
        - MOVE + HOLD: carry a large object to another location
        - TALK + FIGHT: ward off an attack while calling for help or shouting instructions
    """

    ZOMBIE_ACTION_RULES = f"""
    Generate exactly one action that represents your character's next actions in the story.
    This action will be evaluated by a separate system to determine its outcome.

    {ACTION_PROPERTIES}

    Types of Actions:
    {ACTION_MOVE}
    {ACTION_FIGHT}
    {ACTION_HOLD}
    {ACTION_FREEZE}

    Zombie actions are basic and aggressive, requiring minimal thought.
        - performing FIGHT on an actor will almost always be an attempt to bite them
        - performing HOLD on an actor is attempting to grab them so they are easier to bite
        - zombies only FREEZE if they are incapacitated and unable to take actions

    """

    STATE_AROUSAL = """
        Arousal Level:
            - INTENSE: Character takes aggressive, reckless actions
            - ALERT: Character takes bold, decisive actions
            - CALM: Character takes cautious, measured actions
            - PASSIVE: Character takes minimal or passive actions
            - UNRESPONSIVE: Character freezes and does not take any actions 
    """
    STATE_CONTROL = """
        Control Level:
            - DOMINANT: Character overpowers, combats others
            - ASSERTIVE: Character initiates actions, makes demands
            - COMPOSED: Character responds deliberately, coordinates with others
            - SUBMISSIVE: Character hesitates, defers to others
            - IMMOBILIZED: Character freezes, flees, or acts erratically
    """
    STATE_HEALTH = """
        Health:
            - GOOD_HEALTH: Actions are competent, strong and energetic
            - FAIR_HEALTH: Actions are controlled and capable
            - POOR_HEALTH: Actions are limited, slower, or constrained by injury
            - CRITICAL_HEALTH: Actions are severly limited, and movement is minimal
            - DEAD: the character freezes and no actions are taken
    """

    HEALTH_IMPACT = """
        Health impacts the character's ability to act on their disposition.
        For example: a character can be INTENSE or DOMINANT, but be limited to minimal if any action if they are in CRITICAL_HEALTH.
        Health impacts the potential for successful outcomes
        For example: a character in POOR_HEALTH will perform a task less effectively than a character in GOOD_HEALTH
    """

    SURVIVOR_ACTOR_STATE = f"""
    {STATE_AROUSAL}
    {STATE_CONTROL}
    {STATE_HEALTH}

        Arousal + Control Combinations:
        The combination of arousal and control dictate the overall disposition of the character.
            Examples:
            - INTENSE + DOMINANT: combative, attacking, overpowering, hyper
            - INTENSE + ASSERTIVE: demanding, pushy, impatient
            - INTENSE + COMPOSED: focused, brave, action-oriented
            - INTENSE + SUBMISSIVE: panicked, anxious, counterproductive
            - CALM + DOMINANT: cold, calculated aggression, ruthless
            - CALM + ASSERTIVE: leader
            - CALM + COMPOSED: collaborative, conversational
            - CALM + SUBMISSIVE: awaits orders, follows orders
            - PASSIVE + DOMINANT: abandons others, deceiving
            - PASSIVE + ASSERTIVE: disgruntled, complaining
            - PASSIVE + COMPOSED: ignores others, focused on their own thing
            - PASSIVE + SUBMISSIVE: cowers from others, fearful

    {HEALTH_IMPACT}
    """

    ZOMBIE_ACTOR_STATE = f"""
    {STATE_HEALTH}

        Arousal Level:
            - INTENSE: Character takes aggressive, reckless actions

        Control Level:
            - DOMINANT: Character overpowers, combats others

    {HEALTH_IMPACT}
    """

    CONFLICTING_CONTEXT_RULE = """
    If information conflicts, favor higher-priority sources but don't entirely discard lower-priority context.
    """

    ACTOR_USER_PROMPT = """
    "Generate exactly two actions that best align to your character and environment, according to all context you have."
    """