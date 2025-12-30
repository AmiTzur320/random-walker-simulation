# Random Walker Simulator

A configurable random-walk simulator with an interactive UI for exploring walker behaviors in 2D and 3D environments. Run interactively to visualize paths in real time, or use batch mode for controlled experiments with automated data export.

## Features

### Execution Modes
- **Interactive Mode**: Real-time visualization using Matplotlib (supports 2D and 3D)
- **Batch Mode**: Automated experiments with CSV statistics and PNG charts

### Walker Strategies
- **walker1**: Unit step with uniform random direction (0–360°)
- **walker2**: Variable step size (0.5–1.5 units) with random direction
- **walker3**: Discrete 4-direction grid walk (Up/Down/Left/Right)
- **walker4**: Biased walk with tendency toward origin
- **walker5**: Extended step size variant
- **walker6**: 50% rest probability per step

### Environment Elements
- **Obstacles**: Impassable boundary points
- **Portals**: Teleportation between universe locations
- **Traps**: One-way zones that capture walkers
- **Slow Zones**: Movement speed reduction areas
- **Black Holes** (3D only): Gravitational capture using event horizon physics

### Optional Behaviors
- **Restart-to-origin**: Probabilistic teleportation back to start
- **Ice mode**: Frame-by-frame progression for detailed analysis

---

## Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
```bash
python main.py
```

The UI allows parameter adjustment without code modifications. For reproducible results, set a fixed random seed in the configuration.

---

## Batch Mode Output

When running in batch mode, the simulator generates:

### Statistics
- `stats.csv` — Aggregated metrics across experiments

### Visualizations
- `avg_distance_from_origin.png`
- `avg_distance_from_x_axis.png`
- `avg_distance_from_y_axis.png`
- `avg_num_steps_to_exit_circle.png`
- `avg_total_walker_crosses_y_axis.png`

---

## Physics Model

Black hole gravitational force calculation:
```
F = G × (m₁ × m₂) / r²
```

Where:
- `F` = gravitational force
- `G` = gravitational constant
- `m₁` = walker mass
- `m₂` = black hole mass
- `r` = distance between walker and black hole

---

## Project Structure
```
.
├── main.py
├── requirements.txt
├── README.md
├── src/
└── outputs/            # Generated files (git-ignored)
```

---

## License

[Specify your license here — MIT is common for open-source projects]
