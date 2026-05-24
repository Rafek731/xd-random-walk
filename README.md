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
python3 -m venv .venv      # On Windows use: python -m venv .venv
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

--- 
The secondary window in this simulation plots the exact distances of all particles and calculates the theoretical coefficient $a$ in real-time. Depending on whether you chose `discrete`, `uniform`, or `normal` coefficients converge to different values:

* 

General idea of **regression** is that we take some function $f$ and measure the difference between our model and desired output. This gives us feedback how should we change our function $f$ to get better results.

To measure how good is our model we use ***error function***. This is a function that takes output from our model $y_i$ as well as empirical value $\hat{y_i}$ and spits out some number which encodes our model performance. Our goal is to tweak $f$'s parameters in such a way that this error is as low as possible. In this project **MSE** (mean sqared error) is used as an error function. MSE is defined as following:

$$\text{MSE}(\mathbf{\hat{y}}, \mathbf{y})=\frac{1}{n}\sum_{i=1}^n(\hat{y_i} - y_i)^2$$

where $\mathbf{y}, \mathbf{\hat{y}}$ are n-dimensional vectors and $y_i = f(x_i)$ we take derivative of **MSE** and set it equal to 0. Since we cannot have highes value of error (we can always perform worse) given solution of the equation gives us either stationary point or local minimum (as we will se in the project it is actually a local minimum).
Our function $f$ is defined as $f(x)=a\sqrt{x}$ and we remember that $y_i = f(x_i)$, then what we've got is following:

$$
\begin{align*}
&\frac{\text d}{\text{d}a}\text{MSE}(\mathbf{\hat{y}}, \mathbf{y})=0\\
&\frac{\text d}{\text{d}a}\frac{1}{n}\sum_{i=1}^n(\hat{y_i} - y_i)^2 =0\\
&\sum_{i=1}^n\frac{\text d}{\text{d}a}(\hat{y_i} - f(x_i))^2=0\\
&\sum_{i=1}^n\frac{\text d}{\text{d}a}(\hat{y_i} - a\sqrt{x_i})^2=0\\
&\sum_{i=1}^n2(\hat{y_i} - a\sqrt{x_i})\sqrt{x_i} = 0\\
&\sum_{i=1}^n(\hat{y_i}\sqrt{x_i} - ax_i) = 0\\
&\sum_{i=1}^n(\hat{y_i}\sqrt{x_i})=a\sum_{i=1}^nx_i\\
&a = \frac{\displaystyle\sum_{i=1}^n(\hat{y_i}\sqrt{x_i})}{\displaystyle\sum_{i=1}^nx_i}
\end{align*}
$$

We got such an $a$ that the **MSE** has minimum or stationary point. Algorithm inside the project allows to calculate $a$ in $O(1)$ time every step.
