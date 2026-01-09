"""
Traffic Light Task Configuration

Task-specific configuration for traffic light reasoning tasks.
"""

from pydantic import Field
from core import GenerationConfig


class TaskConfig(GenerationConfig):
    """
    Traffic light task-specific configuration.
    
    Inherited from GenerationConfig:
        - num_samples: int          # Number of samples to generate
        - domain: str               # Task domain name
        - difficulty: Optional[str] # Difficulty level
        - random_seed: Optional[int] # For reproducibility
        - output_dir: Path          # Where to save outputs
        - image_size: tuple[int, int] # Image dimensions
    """
    
    # ══════════════════════════════════════════════════════════════════════════
    #  OVERRIDE DEFAULTS
    # ══════════════════════════════════════════════════════════════════════════
    
    domain: str = Field(default="traffic_light")
    image_size: tuple[int, int] = Field(default=(600, 600))
    
    # ══════════════════════════════════════════════════════════════════════════
    #  VIDEO SETTINGS
    # ══════════════════════════════════════════════════════════════════════════
    
    generate_videos: bool = Field(
        default=True,
        description="Whether to generate ground truth videos"
    )
    
    video_fps: int = Field(
        default=2,
        description="Video frame rate (2 fps = 1 frame per countdown second)"
    )
    
    # ══════════════════════════════════════════════════════════════════════════
    #  TRAFFIC LIGHT TASK SETTINGS
    # ══════════════════════════════════════════════════════════════════════════
    
    task_type_distribution: dict[int, float] = Field(
        default={
            1: 0.35,  # Type 1: Basic (35%)
            2: 0.30,  # Type 2: Medium (30%)
            3: 0.20,  # Type 3: Dual countdown (20%)
            4: 0.15,  # Type 4: Complex (15%)
        },
        description="Distribution of task types"
    )
    
    countdown_range_type1: tuple[int, int] = Field(
        default=(2, 10),
        description="Countdown range for Type 1 tasks (expanded for more variety)"
    )
    
    countdown_range_type2: tuple[int, int] = Field(
        default=(8, 20),
        description="Countdown range for Type 2 tasks (expanded for more variety)"
    )
    
    show_countdown_at_zero: bool = Field(
        default=False,
        description="Whether to show countdown number 0 or hide it"
    )
