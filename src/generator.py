"""
Traffic Light Task Generator

Generates traffic light reasoning tasks for video model evaluation.
"""

import random
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any
from PIL import Image, ImageDraw, ImageFont

from core import BaseGenerator, TaskPair, ImageRenderer
from core.video_utils import VideoGenerator
from .config import TaskConfig
from .prompts import get_prompt


class TaskGenerator(BaseGenerator):
    """
    Traffic light task generator.
    
    Generates tasks that test temporal reasoning, rule application, and
    coordination understanding in video models.
    """
    
    def __init__(self, config: TaskConfig):
        super().__init__(config)
        self.renderer = ImageRenderer(image_size=config.image_size)
        
        # Initialize video generator if enabled
        self.video_generator = None
        if config.generate_videos and VideoGenerator.is_available():
            self.video_generator = VideoGenerator(fps=config.video_fps, output_format="mp4")
    
    def generate_task_pair(self, task_id: str) -> TaskPair:
        """Generate one task pair."""
        
        # Select task type based on distribution
        task_type = self._select_task_type()
        
        # Generate task data based on type
        task_data = self._generate_task_data(task_type)
        
        # Render initial state image
        first_image = self._render_traffic_light(
            light_a_state=task_data["light_a_state"],
            light_a_countdown=task_data["light_a_countdown"],
            light_b_state=task_data["light_b_state"],
            light_b_countdown=task_data["light_b_countdown"]
        )
        
        # Calculate final state
        final_state = self._calculate_final_state(
            light_a_state=task_data["light_a_state"],
            light_a_countdown=task_data["light_a_countdown"],
            light_b_state=task_data["light_b_state"],
            light_b_countdown=task_data["light_b_countdown"],
            time_elapsed=task_data.get("time_elapsed", None)
        )
        
        # Render final state image
        final_image = self._render_traffic_light(
            light_a_state=final_state["light_a_state"],
            light_a_countdown=final_state["light_a_countdown"],
            light_b_state=final_state["light_b_state"],
            light_b_countdown=final_state["light_b_countdown"]
        )
        
        # Generate video (optional)
        video_path = None
        if self.config.generate_videos and self.video_generator:
            video_path = self._generate_video(
                first_image, final_image, task_id, task_data, final_state
            )
        
        # Format prompt
        prompt = get_prompt(
            task_type=task_type,
            countdown_a=task_data["light_a_countdown"],
            countdown_b=task_data["light_b_countdown"],
            time_elapsed=task_data.get("time_elapsed", None)
        )
        
        return TaskPair(
            task_id=task_id,
            domain=self.config.domain,
            prompt=prompt,
            first_image=first_image,
            final_image=final_image,
            ground_truth_video=video_path
        )
    
    # ══════════════════════════════════════════════════════════════════════════
    #  TASK GENERATION HELPERS
    # ══════════════════════════════════════════════════════════════════════════
    
    def _select_task_type(self) -> int:
        """Select task type based on distribution."""
        r = random.random()
        cumulative = 0.0
        for task_type, prob in sorted(self.config.task_type_distribution.items()):
            cumulative += prob
            if r <= cumulative:
                return task_type
        return 1  # Fallback to type 1
    
    def _generate_task_data(self, task_type: int) -> Dict[str, Any]:
        """Generate task data for the specified type."""
        if task_type == 1:
            # Type 1: Basic countdown decrement
            # Light A: Red with countdown 3-7, Light B: Green (no countdown)
            countdown_a = random.randint(*self.config.countdown_range_type1)
            return {
                "light_a_state": "red",
                "light_a_countdown": countdown_a,
                "light_b_state": "green",
                "light_b_countdown": 0,
                "task_type": 1
            }
        
        elif task_type == 2:
            # Type 2: Larger countdown numbers
            # Light A: Red with countdown 7-15, Light B: Green (no countdown)
            countdown_a = random.randint(*self.config.countdown_range_type2)
            return {
                "light_a_state": "red",
                "light_a_countdown": countdown_a,
                "light_b_state": "green",
                "light_b_countdown": 0,
                "task_type": 2
            }
        
        elif task_type == 3:
            # Type 3: Dual countdown coordination
            # Light A: Red with larger countdown, Light B: Green with smaller countdown
            countdown_a = random.randint(8, 15)
            countdown_b = random.randint(3, min(7, countdown_a - 1))
            return {
                "light_a_state": "red",
                "light_a_countdown": countdown_a,
                "light_b_state": "green",
                "light_b_countdown": countdown_b,
                "task_type": 3
            }
        
        elif task_type == 4:
            # Type 4: Complex time calculation
            # Two countdowns with time_elapsed > both
            countdown_a = random.randint(5, 10)
            countdown_b = random.randint(3, 7)
            time_elapsed = random.randint(
                max(countdown_a, countdown_b) + 2,
                max(countdown_a, countdown_b) + 8
            )
            return {
                "light_a_state": "red",
                "light_a_countdown": countdown_a,
                "light_b_state": "green",
                "light_b_countdown": countdown_b,
                "time_elapsed": time_elapsed,
                "task_type": 4
            }
        
        else:
            # Fallback to type 1
            return self._generate_task_data(1)
    
    def _calculate_final_state(
        self,
        light_a_state: str,
        light_a_countdown: int,
        light_b_state: str,
        light_b_countdown: int,
        time_elapsed: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Calculate final state based on countdown timers and relative rules.
        
        Rules:
        - When countdown reaches 0, the light switches state (red <-> green)
        - When one light switches, the other also switches (relative rule)
        - Countdowns decrement simultaneously
        """
        current_a_state = light_a_state
        current_a_countdown = light_a_countdown
        current_b_state = light_b_state
        current_b_countdown = light_b_countdown
        
        # Determine time to simulate
        if time_elapsed is None:
            # Simulate until first countdown reaches 0 (or both if both are counting)
            if current_a_countdown > 0 and current_b_countdown > 0:
                # Both counting: simulate until the smaller one reaches 0
                time_elapsed = min(current_a_countdown, current_b_countdown)
            elif current_a_countdown > 0:
                time_elapsed = current_a_countdown
            elif current_b_countdown > 0:
                time_elapsed = current_b_countdown
            else:
                time_elapsed = 0
        
        # Simulate time progression
        time_remaining = time_elapsed
        
        while time_remaining > 0:
            # Determine which countdown will reach 0 first
            if current_a_countdown > 0 and current_b_countdown > 0:
                # Both counting
                if current_a_countdown <= current_b_countdown:
                    # A reaches 0 first (or simultaneously)
                    steps = current_a_countdown
                else:
                    # B reaches 0 first
                    steps = current_b_countdown
            elif current_a_countdown > 0:
                steps = current_a_countdown
            elif current_b_countdown > 0:
                steps = current_b_countdown
            else:
                # Both at 0, no more changes
                break
            
            # Take the minimum of steps needed and time remaining
            steps = min(steps, time_remaining)
            
            # Decrement countdowns
            if current_a_countdown > 0:
                current_a_countdown -= steps
            if current_b_countdown > 0:
                current_b_countdown -= steps
            time_remaining -= steps
            
            # Check if any countdown reached 0
            if current_a_countdown == 0 and current_a_state == "red":
                # A switches from red to green, B switches from green to red
                current_a_state = "green"
                current_b_state = "red"
                # If B was counting, stop it
                if current_b_countdown > 0:
                    current_b_countdown = 0
            elif current_b_countdown == 0 and current_b_state == "green":
                # B switches from green to red, A switches from red to green
                current_b_state = "red"
                current_a_state = "green"
                # If A was counting, stop it
                if current_a_countdown > 0:
                    current_a_countdown = 0
        
        return {
            "light_a_state": current_a_state,
            "light_a_countdown": current_a_countdown,
            "light_b_state": current_b_state,
            "light_b_countdown": current_b_countdown
        }
    
    # ══════════════════════════════════════════════════════════════════════════
    #  RENDERING
    # ══════════════════════════════════════════════════════════════════════════
    
    def _render_traffic_light(
        self,
        light_a_state: str,
        light_a_countdown: int,
        light_b_state: str,
        light_b_countdown: int
    ) -> Image.Image:
        """
        Render a traffic light scene with two traffic lights.
        
        Args:
            light_a_state: "red" or "green"
            light_a_countdown: Countdown number (0 means no countdown shown)
            light_b_state: "red" or "green"
            light_b_countdown: Countdown number (0 means no countdown shown)
        """
        width, height = self.config.image_size
        img = Image.new('RGB', (width, height), color=(240, 240, 235))  # Light gray background
        draw = ImageDraw.Draw(img)
        
        # Draw crossroad background (simple intersection)
        road_width = width // 4
        road_color = (60, 60, 60)  # Dark gray
        
        # Horizontal road
        draw.rectangle(
            [0, height // 2 - road_width // 2, width, height // 2 + road_width // 2],
            fill=road_color
        )
        
        # Vertical road
        draw.rectangle(
            [width // 2 - road_width // 2, 0, width // 2 + road_width // 2, height],
            fill=road_color
        )
        
        # Road markings (center lines)
        line_color = (255, 255, 255)
        line_width = 2
        dash_length = 20
        dash_gap = 10
        
        # Horizontal dashed line
        for x in range(0, width, dash_length + dash_gap):
            draw.line([(x, height // 2), (x + dash_length, height // 2)], 
                     fill=line_color, width=line_width)
        
        # Vertical dashed line
        for y in range(0, height, dash_length + dash_gap):
            draw.line([(width // 2, y), (width // 2, y + dash_length)], 
                     fill=line_color, width=line_width)
        
        # Traffic light parameters
        light_radius = width // 12
        margin = width // 8
        
        # Traffic Light A (left side)
        light_a_x = margin + light_radius
        light_a_y = height // 2
        
        # Traffic Light B (right side)
        light_b_x = width - margin - light_radius
        light_b_y = height // 2
        
        # Draw Traffic Light A
        self._draw_single_traffic_light(
            draw, light_a_x, light_a_y, light_a_state, 
            light_a_countdown, light_radius, "A"
        )
        
        # Draw Traffic Light B
        self._draw_single_traffic_light(
            draw, light_b_x, light_b_y, light_b_state,
            light_b_countdown, light_radius, "B"
        )
        
        return img
    
    def _draw_single_traffic_light(
        self,
        draw: ImageDraw.Draw,
        center_x: int,
        center_y: int,
        state: str,
        countdown: int,
        radius: int,
        label: str
    ):
        """Draw a single traffic light with state and countdown."""
        # Draw light circle
        color = (255, 0, 0) if state == "red" else (0, 200, 0)  # Red or green
        outline_color = (0, 0, 0)
        outline_width = 3
        
        # Draw circle (with outline)
        bbox = [
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius
        ]
        draw.ellipse(bbox, fill=color, outline=outline_color, width=outline_width)
        
        # Draw label (A or B) above the light
        try:
            font_size = radius // 2
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        label_bbox = draw.textbbox((0, 0), label, font=font)
        label_width = label_bbox[2] - label_bbox[0]
        label_height = label_bbox[3] - label_bbox[1]
        label_x = center_x - label_width // 2
        label_y = center_y - radius - label_height - 10
        draw.text((label_x, label_y), f"Traffic {label}", fill=(0, 0, 0), font=font)
        
        # Draw countdown number below the light
        if countdown > 0 or (countdown == 0 and self.config.show_countdown_at_zero):
            countdown_text = str(countdown)
            try:
                countdown_font_size = radius
                countdown_font = ImageFont.truetype(
                    "/System/Library/Fonts/Supplemental/Arial.ttf", countdown_font_size
                )
            except:
                countdown_font = ImageFont.load_default()
            
            countdown_bbox = draw.textbbox((0, 0), countdown_text, font=countdown_font)
            countdown_width = countdown_bbox[2] - countdown_bbox[0]
            countdown_height = countdown_bbox[3] - countdown_bbox[1]
            countdown_x = center_x - countdown_width // 2
            countdown_y = center_y + radius + 15
            
            # Draw countdown with white background for visibility
            padding = 5
            draw.rectangle(
                [countdown_x - padding, countdown_y - padding,
                 countdown_x + countdown_width + padding, countdown_y + countdown_height + padding],
                fill=(255, 255, 255), outline=(0, 0, 0), width=2
            )
            draw.text((countdown_x, countdown_y), countdown_text, fill=(0, 0, 0), font=countdown_font)
    
    # ══════════════════════════════════════════════════════════════════════════
    #  VIDEO GENERATION
    # ══════════════════════════════════════════════════════════════════════════
    
    def _generate_video(
        self,
        first_image: Image.Image,
        final_image: Image.Image,
        task_id: str,
        task_data: Dict[str, Any],
        final_state: Dict[str, Any]
    ) -> Optional[str]:
        """Generate ground truth video showing countdown decrement."""
        temp_dir = Path(tempfile.gettempdir()) / f"{self.config.domain}_videos"
        temp_dir.mkdir(parents=True, exist_ok=True)
        video_path = temp_dir / f"{task_id}_ground_truth.mp4"
        
        # Generate frames showing countdown decrement
        frames = self._create_countdown_animation_frames(
            task_data, final_state
        )
        
        if frames:
            result = self.video_generator.create_video_from_frames(
                frames, video_path
            )
            return str(result) if result else None
        
        return None
    
    def _create_countdown_animation_frames(
        self,
        task_data: Dict[str, Any],
        final_state: Dict[str, Any],
        hold_frames: int = 5,
        frames_per_countdown: int = 2
    ) -> list:
        """
        Create animation frames showing countdown decrement.
        
        Video structure:
        1. Hold first_frame (initial state) for hold_frames
        2. Animate countdown decrement step by step
        3. Hold final_frame (final state) for hold_frames
        
        Args:
            task_data: Initial task data
            final_state: Calculated final state
            hold_frames: Frames to hold at start and end (default: 5 frames = 2.5 seconds at 2 fps)
            frames_per_countdown: Frames per countdown number (at 2 fps, this means 1 second per countdown)
        """
        frames = []
        
        light_a_state = task_data["light_a_state"]
        light_a_countdown = task_data["light_a_countdown"]
        light_b_state = task_data["light_b_state"]
        light_b_countdown = task_data["light_b_countdown"]
        
        # Determine max countdown to know how many seconds to animate
        max_countdown = max(light_a_countdown, light_b_countdown)
        
        # Render first frame (initial state) - this must match first_frame.png
        first_frame = self._render_traffic_light(
            light_a_state, light_a_countdown,
            light_b_state, light_b_countdown
        )
        
        # Render final frame (target state) - this must match final_frame.png
        final_frame = self._render_traffic_light(
            final_state["light_a_state"], final_state["light_a_countdown"],
            final_state["light_b_state"], final_state["light_b_countdown"]
        )
        
        if max_countdown == 0:
            # No countdown to animate, just show first and final frames
            for _ in range(hold_frames):
                frames.append(first_frame)
            for _ in range(hold_frames):
                frames.append(final_frame)
            return frames
        
        # Current state tracking
        current_a_countdown = light_a_countdown
        current_b_countdown = light_b_countdown
        current_a_state = light_a_state
        current_b_state = light_b_state
        
        # Hold initial position (first frame)
        for _ in range(hold_frames):
            frames.append(first_frame)
        
        # Animate countdown decrement step by step
        # We simulate time passing, second by second, up to the point where we reach final state
        time_elapsed = 0
        prev_a_countdown = current_a_countdown
        prev_b_countdown = current_b_countdown
        
        # Calculate total time needed
        total_time = max_countdown + 1  # Default: show until max countdown reaches 0
        
        while time_elapsed <= total_time:
            # Determine what the countdowns should be at this time
            new_a_countdown = max(0, light_a_countdown - time_elapsed) if light_a_countdown > 0 else 0
            new_b_countdown = max(0, light_b_countdown - time_elapsed) if light_b_countdown > 0 else 0
            
            # Check if countdown just reached 0 (transition from >0 to 0)
            a_just_reached_zero = (prev_a_countdown > 0 and new_a_countdown == 0)
            b_just_reached_zero = (prev_b_countdown > 0 and new_b_countdown == 0)
            
            # Determine new states (default: keep current)
            new_a_state = current_a_state
            new_b_state = current_b_state
            
            # Handle state switches when countdowns reach 0
            # Priority: if both reach 0 at same time, or if one reaches 0 first
            if a_just_reached_zero and b_just_reached_zero:
                # Both reach 0 simultaneously - A (red) should switch to green
                if current_a_state == "red":
                    new_a_state = "green"
                    new_b_state = "red"
                    new_b_countdown = 0  # B stops counting
                elif current_b_state == "green":
                    new_b_state = "red"
                    new_a_state = "green"
                    new_a_countdown = 0  # A stops counting
            elif a_just_reached_zero and current_a_state == "red":
                # A reaches 0 first, switch states
                new_a_state = "green"
                new_b_state = "red"
                new_b_countdown = 0  # B stops counting
            elif b_just_reached_zero and current_b_state == "green":
                # B reaches 0 first, switch states
                new_b_state = "red"
                new_a_state = "green"
                new_a_countdown = 0  # A stops counting
            
            # Update current state
            prev_a_countdown = current_a_countdown
            prev_b_countdown = current_b_countdown
            current_a_countdown = new_a_countdown
            current_b_countdown = new_b_countdown
            current_a_state = new_a_state
            current_b_state = new_b_state
            
            # Render frame for this state
            frame = self._render_traffic_light(
                current_a_state, current_a_countdown,
                current_b_state, current_b_countdown
            )
            
            # Add frames for this countdown value
            for _ in range(frames_per_countdown):
                frames.append(frame)
            
            time_elapsed += 1
            
            # Check if we've reached the final state
            if (current_a_state == final_state["light_a_state"] and 
                current_a_countdown == final_state["light_a_countdown"] and
                current_b_state == final_state["light_b_state"] and
                current_b_countdown == final_state["light_b_countdown"]):
                # We've reached the final state
                break
            
            # Safety check to avoid infinite loops
            if time_elapsed > 30:
                break
        
        # Remove duplicate frames added after reaching final state
        # Keep only frames up to but not including the final state
        if len(frames) > hold_frames + frames_per_countdown:
            # Remove the last set of frames that were added for final state
            frames = frames[:-frames_per_countdown]
        
        # Hold final position (final frame) - must be the same as final_frame.png
        for _ in range(hold_frames):
            frames.append(final_frame)
        
        return frames
