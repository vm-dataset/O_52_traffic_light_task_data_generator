#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    TRAFFIC LIGHT TASK GENERATION SCRIPT                       ║
║                                                                               ║
║  Run this to generate your dataset.                                           ║
║  Customize TaskConfig and TaskGenerator in src/ for your task.                ║
╚══════════════════════════════════════════════════════════════════════════════╝

Usage:
    python examples/generate.py --num-samples 100
    python examples/generate.py --num-samples 100 --output data/my_task --seed 42
"""

import argparse
from pathlib import Path
import sys
from collections import Counter

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import OutputWriter
from src import TaskGenerator, TaskConfig


def main():
    parser = argparse.ArgumentParser(
        description="Generate Traffic Light Task dataset",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python examples/generate.py --num-samples 10
    python examples/generate.py --num-samples 100 --output data/output --seed 42
    python examples/generate.py --num-samples 100 --no-videos
        """
    )
    
    parser.add_argument(
        "--num-samples",
        type=int,
        required=True,
        help="Number of task samples to generate"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="data/questions",
        help="Output directory (default: data/questions)"
    )
    
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility"
    )
    
    parser.add_argument(
        "--no-videos",
        action="store_true",
        help="Disable video generation (faster, generates only images)"
    )
    
    parser.add_argument(
        "--types",
        type=int,
        nargs="+",
        choices=[1, 2, 3, 4],
        default=None,
        help="Generate only specific task types (e.g., --types 1 3)"
    )
    
    parser.add_argument(
        "--type1-ratio",
        type=float,
        default=None,
        help="Override Type 1 distribution ratio (0.0-1.0)"
    )
    
    parser.add_argument(
        "--type2-ratio",
        type=float,
        default=None,
        help="Override Type 2 distribution ratio (0.0-1.0)"
    )
    
    parser.add_argument(
        "--type3-ratio",
        type=float,
        default=None,
        help="Override Type 3 distribution ratio (0.0-1.0)"
    )
    
    parser.add_argument(
        "--type4-ratio",
        type=float,
        default=None,
        help="Override Type 4 distribution ratio (0.0-1.0)"
    )
    
    parser.add_argument(
        "--image-size",
        type=int,
        nargs=2,
        default=None,
        metavar=("WIDTH", "HEIGHT"),
        help="Custom image size (default: 600 600)"
    )
    
    args = parser.parse_args()
    
    print(f"🎲 Generating {args.num_samples} tasks...")
    
    # Build task type distribution
    task_type_distribution = None
    if args.types:
        # Generate only specified types with equal distribution
        num_types = len(args.types)
        task_type_distribution = {t: 1.0 / num_types for t in args.types}
        print(f"🎯 Task types: {sorted(args.types)} (equal distribution)")
    elif any([args.type1_ratio, args.type2_ratio, args.type3_ratio, args.type4_ratio]):
        # Custom distribution from command line
        ratios = {
            1: args.type1_ratio or 0.35,
            2: args.type2_ratio or 0.30,
            3: args.type3_ratio or 0.20,
            4: args.type4_ratio or 0.15,
        }
        # Normalize ratios
        total = sum(ratios.values())
        task_type_distribution = {k: v / total for k, v in ratios.items()}
        print(f"🎯 Custom distribution: Type 1={task_type_distribution[1]:.2%}, "
              f"Type 2={task_type_distribution[2]:.2%}, "
              f"Type 3={task_type_distribution[3]:.2%}, "
              f"Type 4={task_type_distribution[4]:.2%}")
    
    # Configure task
    config_kwargs = {
        "num_samples": args.num_samples,
        "random_seed": args.seed,
        "output_dir": Path(args.output),
        "generate_videos": not args.no_videos,
    }
    
    if task_type_distribution:
        config_kwargs["task_type_distribution"] = task_type_distribution
    
    if args.image_size:
        config_kwargs["image_size"] = tuple(args.image_size)
    
    # ──────────────────────────────────────────────────────────────────────────
    #  Configure your task here
    #  Add any additional TaskConfig parameters as needed
    # ──────────────────────────────────────────────────────────────────────────
    
    config = TaskConfig(**config_kwargs)
    
    # Generate tasks
    generator = TaskGenerator(config)
    
    # Track progress and statistics
    task_types_generated = []
    
    def infer_task_type(prompt: str) -> int:
        """Infer task type from prompt content."""
        prompt_lower = prompt.lower()
        
        # Type 4: Contains "after X seconds"
        if "after" in prompt_lower and any(char.isdigit() for char in prompt.split("after")[-1].split()[0] if "after" in prompt_lower):
            # Check if there's a number followed by "seconds" after "after"
            parts = prompt_lower.split("after")
            if len(parts) > 1:
                after_part = parts[1]
                if "seconds" in after_part and any(c.isdigit() for c in after_part.split("seconds")[0]):
                    return 4
        
        # Type 3: Contains "both countdown" and "simultaneously"
        if "both countdown" in prompt_lower and "simultaneously" in prompt_lower:
            return 3
        
        # Type 1 or Type 2: Check if only one countdown is mentioned
        # Type 1: countdown 3-7, Type 2: countdown 7-15
        # Look for countdown numbers in the prompt
        import re
        countdown_matches = re.findall(r'countdown (\d+)', prompt_lower)
        if countdown_matches:
            countdown_a = int(countdown_matches[0])
            # If there's only one countdown mentioned, it's Type 1 or 2
            if len(countdown_matches) == 1:
                if 3 <= countdown_a <= 7:
                    return 1
                elif countdown_a > 7:
                    return 2
        
        # Default fallback
        return 2
    
    try:
        tasks = []
        for i, task_pair in enumerate(generator.generate_dataset(), 1):
            tasks.append(task_pair)
            # Extract task type from prompt
            task_type = infer_task_type(task_pair.prompt)
            task_types_generated.append(task_type)
            if i % 10 == 0 or i == args.num_samples:
                print(f"  ✓ Generated {i}/{args.num_samples} tasks", end='\r')
        
        print(f"  ✓ Generated {len(tasks)}/{args.num_samples} tasks")
        
        # Write to disk
        writer = OutputWriter(Path(args.output))
        writer.write_dataset(tasks)
        
        print(f"✅ Done! Generated {len(tasks)} tasks in {args.output}/{config.domain}_task/")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()
