# Random Walker Simulator

A configurable random-walk simulator with an interactive UI for exploring walker behavior in **2D and 3D** environments.  
Run interactively to visualize paths in real time, or use **batch mode** for controlled experiments with automated exports (CSV + charts).

## ✨ Features

### Execution Modes
- **Interactive mode:** real-time visualization using Matplotlib (2D + 3D)
- **Batch mode:** automated experiments with CSV statistics and PNG charts

### Walker Strategies
- **Uniform step:** unit step with random direction (0–360°)
- **Variable step:** step size in [0.5, 1.5] with random direction
- **Grid walk:** discrete 4-direction walk (Up/Down/Left/Right)
- **Biased-to-origin:** tendency toward the origin
- **Extended step:** longer step-size variant
- **Resting walker:** 50% probability to rest each step

### Environment Elements
- **Obstacles:** impassable boundary points  
- **Portals:** teleportation between locations  
- **Traps:** one-way capture zones  
- **Slow zones:** movement speed reduction areas  
- **Black holes (3D only):** gravitational capture within an event horizon  

### Optional Behaviors
- **Restart-to-origin:** probabilistic teleportation back to start
- **Ice mode:** frame-by-frame progression for detailed analysis

---

## 🛠️ Installation

```bash
python -m venv venv
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

pip install -r requirements.txt
```

## ▶️ Usage
```bash
python main.py
```
The UI allows parameter adjustment without code modifications.
For reproducible results, set a fixed random seed in the configuration.

## 📦 Batch Mode Output

When running in batch mode, the simulator generates files under statistics/:

### Statistics

* stats.csv — aggregated metrics across experiments

### Visualizations

* avg_distance_from_origin.png
* avg_distance_from_x_axis.png
* avg_distance_from_y_axis.png
* avg_num_steps_to_exit_circle.png
* avg_total_walker_crosses_y_axis.png

## 🗂️ Project Structure
```txt
.
├── statistics       # outputs
├── README.md
├── src/
└── VIDEO            # YouTube video of me represting the project
```
## 📜 License & Academic Integrity
License

MIT License — see LICENSE.

### Academic Note
Developed as part of HUJI "Introduction to Computer Science" (67101).
Shared for portfolio purposes only — please follow the university’s academic integrity rules.
