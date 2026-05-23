# XD Random Walk Simulator

A high-performance, command-line visualization tool for simulating N-dimensional random walks. Built with Python, NumPy, and Matplotlib.

This project not only visualizes particles moving randomly through space (from 1D up to 100D+ grids), but it also computes real-time mathematical regressions to demonstrate a fundamental statistical law of physics: **Expected distance from the origin grows proportionally to the square root of time ($\sqrt{N}$)**.

## ✨ Features

* **Any Dimension (1D to ND):** Simulate walks in 2D and 3D space, or use the dynamic 16:9 auto-scaling grid for visualizing highly dimensional data (e.g., 10D, 20D).
* **High-Performance Rendering:** Heavily optimized using `numpy` matrix broadcasting and Matplotlib `LineCollection`/`Line3DCollection`. Smoothly renders thousands of particles and deep historical trails without memory leaks or CPU bottlenecks.
* **Multiple Distributions:** Choose exactly how particles take their steps:
  * `discrete`: Standard grid/lattice steps ($\pm 1$).
  * `uniform`: Continuous random floating-point steps.
  * `normal`: Steps drawn from a Gaussian/Normal distribution.
* **Real-time Regression Math:** A secondary live-updating plot uses an $O(1)$ memory algorithm to calculate the least-squares regression of the average particle distance, dynamically fitting the curve $a\sqrt{N}$ perfectly to the data.

## 🚀 Installation

You can set up the project instantly using [uv](https://docs.astral.sh/uv/) (recommended) or standard Python `pip`.

### Option 1: Using `uv` (Recommended)
```bash
git clone https://github.com/Rafek731/xd-random-walk.git
cd xd-random-walk
uv sync
```

### Option 2: Using standard `pip`
```bash
git clone https://github.com/Rafek731/xd-random-walk.git
cd xd-random-walk
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -e .
```

## 🎮 Usage

Once installed, the CLI tool registers the `walk` command globally in your virtual environment.

```bash
# Using uv
uv run walk [OPTIONS]

# Using pip (with environment activated)
walk [OPTIONS]
```

### Command Line Arguments

| Flag | Long Name | Default | Description |
| :--- | :--- | :--- | :--- |
| `-d` | `--dimensions` | `2` | Number of dimensions to simulate (e.g., 2, 3, 10). |
| `-n` | `--num-samples` | `500` | Number of independent particles to spawn. |
| `-p` | `--show-path` | `False` | Displays the trailing paths behind particles (2D/3D only). |
| `-t` | `--tail` | `100` | Length of the visual path history to keep rendered. |
| `-D` | `--distribution` | `discrete` | Step distribution: `discrete`, `uniform`, or `normal`. |
| `-i` | `--interval` | `100` | Animation refresh interval in milliseconds. |

## 💡 Examples

**1. The Classic 2D Walk (1,000 particles)**
```bash
walk -d 2 -n 1000
```

**2. The 3D Trace (5 particles, long visual trails)**
```bash
walk -d 3 -n 5 -p -t 2500
```

**3. High-Dimensional Grid (15 Dimensions)**
*This will automatically generate a 16:9 aspect ratio grid of isolated 1D number lines.*
```bash
walk -d 15 -n 100 -D normal
```

## 📐 The Math Behind the Simulation

In a standard, unbiased random walk, the expected *average position* is always $0$ because positive and negative steps cancel each other out. However, if you measure the *absolute physical distance* (Root Mean Square or Mean Absolute Distance) of the particles from the origin, the variance grows linearly with the number of steps ($N$). 

Taking the square root of that variance reveals the physical distance law:
$$d \propto \sqrt{N}$$

The secondary window in this simulation plots the exact distances of all particles and calculates the theoretical coefficient $a$ in real-time, depending on whether you chose discrete, uniform, or normal steps!
