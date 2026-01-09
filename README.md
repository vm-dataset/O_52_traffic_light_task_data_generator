# Traffic Light Task Data Generator 🚦

A data generator for creating Traffic Light reasoning tasks for video model evaluation. This generator creates tasks that test temporal reasoning, rule application, and coordination understanding in video models.

This task is part of [VMEvalKit](https://github.com/Video-Reason/VMEvalKit.git) and follows the format standards from [template-data-generator](https://github.com/vm-dataset/template-data-generator.git).

Repository: [O_52_traffic_light_task_data_generator](https://github.com/vm-dataset/O_52_traffic_light_task_data_generator)

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/vm-dataset/O_52_traffic_light_task_data_generator.git
cd O_52_traffic_light_task_data_generator

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

# 4. Generate tasks
python examples/generate.py --num-samples 50
```

---

## 📁 Structure

```
traffic-light-task-data-generator/
├── core/                    # ✅ KEEP: Standard utilities
│   ├── base_generator.py   # Abstract base class
│   ├── schemas.py          # Pydantic models
│   ├── image_utils.py      # Image helpers
│   ├── video_utils.py      # Video generation
│   └── output_writer.py    # File output
├── src/                     # ⚠️ CUSTOMIZE: Traffic light task logic
│   ├── generator.py        # Traffic light task generator
│   ├── prompts.py          # Prompt templates
│   └── config.py           # Configuration
├── examples/
│   └── generate.py         # Entry point
└── data/questions/         # Generated output
```

---

## 📦 Output Format

Every generator produces:

```
data/questions/traffic_light_task/{task_id}/
├── first_frame.png          # Initial state (REQUIRED)
├── final_frame.png          # Final state (REQUIRED)
├── prompt.txt               # Instructions (REQUIRED)
└── ground_truth.mp4         # Countdown animation video (OPTIONAL)
```

---

## 🎯 Task Types

The generator creates 4 types of traffic light reasoning tasks:

### Type 1: Basic Countdown Decrement (Simple)
- **Description**: Single traffic light with countdown 3-7 seconds
- **Tests**: Number change understanding, time concept, rule application
- **Example**: Traffic Light A shows red with countdown 5, Traffic Light B shows green. Show countdown decrementing from 5 to 0, then final state.

### Type 2: Number Change + Time Understanding (Medium)
- **Description**: Single traffic light with larger countdown 7-15 seconds
- **Tests**: Larger number handling, complete decrement process
- **Example**: Traffic Light A shows red with countdown 10, Traffic Light B shows green. Show countdown decrementing from 10 to 0.

### Type 3: Dual Countdown Coordination (Hard)
- **Description**: Two traffic lights with simultaneous countdowns
- **Tests**: Simultaneous tracking, determining which reaches 0 first, coordination understanding
- **Example**: Traffic Light A shows red with countdown 10, Traffic Light B shows green with countdown 3. Show both countdowns decrementing simultaneously, then final state when first reaches 0.

### Type 4: Complex Time Calculation (Hard)
- **Description**: Two countdowns with specified time elapsed
- **Tests**: Multiple state switches, complex time sequence calculation
- **Example**: Traffic Light A shows red with countdown 8, Traffic Light B shows green with countdown 5. Show final state after 10 seconds.

---

## 🎨 Configuration

### Task Type Distribution

Default distribution in `src/config.py`:

```python
task_type_distribution = {
    1: 0.35,  # Type 1: Basic (35%)
    2: 0.30,  # Type 2: Medium (30%)
    3: 0.20,  # Type 3: Dual countdown (20%)
    4: 0.15,  # Type 4: Complex (15%)
}
```

### Countdown Ranges

- **Type 1**: 3-7 seconds
- **Type 2**: 7-15 seconds
- **Type 3**: A: 8-15, B: 3-7 (B < A)
- **Type 4**: A: 5-10, B: 3-7, time_elapsed: max(A,B)+2 to max(A,B)+8

---

## 📝 Usage Examples

```bash
# Generate 100 tasks (no videos, faster)
python examples/generate.py --num-samples 100 --no-videos

# Generate 50 tasks with videos
python examples/generate.py --num-samples 50

# Generate with custom output directory and seed
python examples/generate.py --num-samples 200 --output data/my_tasks --seed 42
```

---

## 🧠 Task Description

### Input Components
- **First Frame**: Crossroad scene with two traffic lights showing current states and countdown timers
- **Prompt**: Text instruction explaining the relative rule and asking to show countdown decrement and final state
- **Format**: 600×600px PNG image

### Expected Output
- **Video Sequence**: Animation showing countdown numbers decrementing (e.g., 5→4→3→2→1→0)
- **Final Frame**: Traffic lights in correct final state after countdown reaches 0, with relative rule applied
- **Reasoning**: Proper understanding of temporal progression, countdown mechanics, and relative state coordination

### Core Features
- **Two traffic lights**: Traffic Light A and Traffic Light B
- **Relative rule**: When one is red, the other is green, and vice versa
- **Countdown timers**: Numbers displayed on traffic lights that decrement over time
- **State switching**: When countdown reaches 0, the light switches state and triggers relative rule

---

## 🔧 Customization

All task-specific settings are in `src/config.py`:

```python
class TaskConfig(GenerationConfig):
    domain: str = Field(default="traffic_light")
    image_size: tuple[int, int] = Field(default=(600, 600))
    
    task_type_distribution: dict[int, float] = Field(default={...})
    countdown_range_type1: tuple[int, int] = Field(default=(3, 7))
    countdown_range_type2: tuple[int, int] = Field(default=(7, 15))
    show_countdown_at_zero: bool = Field(default=False)
```

---

## 📊 Visual Design

### Traffic Light Representation

**Layout:**
- Two traffic lights positioned on crossroad scene (left and right)
- Simple crossroad background for context

**Traffic Light Structure:**
- Colored circle: Red (🔴) or Green (🟢)
- Countdown number: Displayed below the light
- Clear visual distinction between red and green states

**Countdown Display:**
- Numbers displayed clearly (e.g., "5", "3", "10")
- Position: Below the traffic light
- Font: Large, readable, contrasting with background

---

## 🧪 Cognitive Abilities Tested

1. **Temporal Reasoning**: Countdown understanding, time progression, time calculation
2. **Rule Application**: Relative rule, state switching, rule triggering
3. **Coordination Understanding**: System interdependence, simultaneous tracking, priority determination
4. **Video Generation with Numbers**: Number animation, visual consistency, state synchronization

---

## 📚 Related Resources

- [VMEvalKit](https://github.com/Video-Reason/VMEvalKit.git) - Framework for evaluating reasoning in video models
- [template-data-generator](https://github.com/vm-dataset/template-data-generator.git) - Template for creating reasoning task generators
- This generator follows VMEvalKit task format standards and template-data-generator structure

---

## 📄 License

See LICENSE file for details.
