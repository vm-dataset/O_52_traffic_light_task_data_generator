"""
Traffic Light Task Prompts

Prompts for traffic light reasoning tasks (aligned with VMEvalKit).
"""

# ══════════════════════════════════════════════════════════════════════════════
#  SCENE AND RULE DESCRIPTIONS
# ══════════════════════════════════════════════════════════════════════════════

SCENE_PREFIX = "This scene shows a crossroad with two traffic lights. "
RULE_EXPLANATION = "The two traffic lights are opposite to each other: when one is red, the other is green, and vice versa. "


# ══════════════════════════════════════════════════════════════════════════════
#  TASK TYPE PROMPTS
# ══════════════════════════════════════════════════════════════════════════════

# Type 1: Basic Countdown Decrement (Simple)
TYPE_1_PROMPTS = [
    SCENE_PREFIX + RULE_EXPLANATION + 
    "Currently, Traffic Light A shows red with countdown {countdown_a}. Traffic Light B shows green. " +
    "Generate a video showing the countdown number decrementing from {countdown_a} to 0, then show the final state of both traffic lights.",
    
    SCENE_PREFIX + RULE_EXPLANATION + 
    "At the moment, Traffic Light A displays red with a countdown of {countdown_a}. Traffic Light B displays green. " +
    "Create a video that shows the countdown decreasing from {countdown_a} to 0, followed by the final state of both lights.",
    
    SCENE_PREFIX + RULE_EXPLANATION + 
    "Traffic Light A is currently red with countdown {countdown_a}, while Traffic Light B is green. " +
    "Produce a video demonstrating the countdown reducing from {countdown_a} to 0, then reveal the final state of both traffic lights.",
    
    SCENE_PREFIX + RULE_EXPLANATION + 
    "Right now, Traffic Light A shows red with a {countdown_a}-second countdown. Traffic Light B shows green. " +
    "Generate a video where the countdown decrements from {countdown_a} to 0, and then display the final state of both lights.",
    
    SCENE_PREFIX + RULE_EXPLANATION + 
    "The current state: Traffic Light A is red with countdown {countdown_a}, Traffic Light B is green. " +
    "Create a video showing the countdown going from {countdown_a} down to 0, then show what both traffic lights look like at the end."
]

# Type 2: Number Change + Time Understanding (Medium)
TYPE_2_PROMPTS = [
    SCENE_PREFIX + RULE_EXPLANATION + 
    "Currently, Traffic Light A shows red with countdown {countdown_a}. Traffic Light B shows green. " +
    "Generate a video showing the countdown number decrementing from {countdown_a} to 0, then show the final state of both traffic lights.",
    
    SCENE_PREFIX + RULE_EXPLANATION + 
    "At present, Traffic Light A displays red with a countdown timer at {countdown_a}. Traffic Light B displays green. " +
    "Create a video that demonstrates the countdown decreasing from {countdown_a} to 0, followed by the final state.",
    
    SCENE_PREFIX + RULE_EXPLANATION + 
    "Traffic Light A currently shows red with a {countdown_a}-second countdown, while Traffic Light B shows green. " +
    "Produce a video showing the countdown reducing from {countdown_a} to 0, then reveal the final state of both lights.",
    
    SCENE_PREFIX + RULE_EXPLANATION + 
    "The initial state: Traffic Light A is red with countdown {countdown_a}, and Traffic Light B is green. " +
    "Generate a video where the countdown goes from {countdown_a} down to 0, then display the final state of both traffic lights.",
    
    SCENE_PREFIX + RULE_EXPLANATION + 
    "Right now, Traffic Light A has a red signal with countdown {countdown_a}. Traffic Light B has a green signal. " +
    "Create a video showing the countdown timer decrementing from {countdown_a} to 0, and then show the final state."
]

# Type 3: Dual Countdown Coordination (Hard)
TYPE_3_PROMPTS = [
    SCENE_PREFIX + RULE_EXPLANATION + 
    "Currently, Traffic Light A shows red with countdown {countdown_a}. Traffic Light B shows green with countdown {countdown_b}. " +
    "Generate a video showing both countdown numbers decrementing simultaneously. When any countdown reaches 0, apply the relative rule to switch states. Then show the final state of both traffic lights.",
    
    SCENE_PREFIX + RULE_EXPLANATION + 
    "At the moment, Traffic Light A displays red with countdown {countdown_a}, and Traffic Light B displays green with countdown {countdown_b}. " +
    "Create a video where both countdowns decrease at the same time. When either countdown hits 0, the lights switch states according to the rule. Display the final state.",
    
    SCENE_PREFIX + RULE_EXPLANATION + 
    "Traffic Light A is red with a {countdown_a}-second countdown, while Traffic Light B is green with a {countdown_b}-second countdown. " +
    "Produce a video showing both countdowns decrementing together. When one reaches 0, apply the state switch rule. Show the final state of both lights.",
    
    SCENE_PREFIX + RULE_EXPLANATION + 
    "The current state: Traffic Light A shows red (countdown {countdown_a}), Traffic Light B shows green (countdown {countdown_b}). " +
    "Generate a video with both countdowns decreasing simultaneously. When any countdown reaches 0, the lights switch states. Display the final state.",
    
    SCENE_PREFIX + RULE_EXPLANATION + 
    "Right now, Traffic Light A has red with countdown {countdown_a}, and Traffic Light B has green with countdown {countdown_b}. " +
    "Create a video showing both countdowns going down at the same time. When either hits 0, apply the opposite state rule. Show the final state."
]

# Type 4: Complex Time Calculation (Hard)
TYPE_4_PROMPTS = [
    SCENE_PREFIX + RULE_EXPLANATION + 
    "Currently, Traffic Light A shows red with countdown {countdown_a}. Traffic Light B shows green with countdown {countdown_b}. " +
    "Generate a video showing countdown numbers decrementing. When countdown reaches 0, apply the relative rule to switch states. Then show the final state of both traffic lights after {time_elapsed} seconds.",
    
    SCENE_PREFIX + RULE_EXPLANATION + 
    "At the moment, Traffic Light A displays red (countdown {countdown_a}), and Traffic Light B displays green (countdown {countdown_b}). " +
    "Create a video where countdowns decrease. When a countdown hits 0, the lights switch states. Display the final state after {time_elapsed} seconds have passed.",
    
    SCENE_PREFIX + RULE_EXPLANATION + 
    "Traffic Light A is red with countdown {countdown_a}, while Traffic Light B is green with countdown {countdown_b}. " +
    "Produce a video showing the countdowns decrementing. When any countdown reaches 0, apply the state switch rule. Show the final state after {time_elapsed} seconds.",
    
    SCENE_PREFIX + RULE_EXPLANATION + 
    "The initial state: Traffic Light A shows red (countdown {countdown_a}), Traffic Light B shows green (countdown {countdown_b}). " +
    "Generate a video with countdowns decreasing. When a countdown reaches 0, the lights switch according to the rule. Display the state after {time_elapsed} seconds.",
    
    SCENE_PREFIX + RULE_EXPLANATION + 
    "Right now, Traffic Light A has red with countdown {countdown_a}, Traffic Light B has green with countdown {countdown_b}. " +
    "Create a video showing the countdowns going down. When either reaches 0, apply the opposite state rule. Show the final state after {time_elapsed} seconds."
]

# All Type prompts organized by type index (1-4)
TYPE_PROMPTS = {
    1: TYPE_1_PROMPTS,
    2: TYPE_2_PROMPTS,
    3: TYPE_3_PROMPTS,
    4: TYPE_4_PROMPTS
}

def get_prompt(task_type: int, prompt_variant: int = None, **kwargs) -> str:
    """
    Get prompt for the given task type.
    
    Args:
        task_type: Task type (1-4)
        prompt_variant: Which prompt variant to use (0-4). If None, randomly selects one.
        **kwargs: Format parameters (countdown_a, countdown_b, time_elapsed)
        
    Returns:
        Formatted prompt string
    """
    import random
    
    prompts = TYPE_PROMPTS.get(task_type, TYPE_1_PROMPTS)
    
    # Select prompt variant
    if prompt_variant is None:
        prompt_index = random.randint(0, len(prompts) - 1)
    else:
        prompt_index = prompt_variant % len(prompts)
    
    prompt_template = prompts[prompt_index]
    return prompt_template.format(**kwargs)


def get_all_prompts(task_type: int) -> list[str]:
    """Get all prompts for a given task type."""
    return TYPE_PROMPTS.get(task_type, TYPE_1_PROMPTS)
