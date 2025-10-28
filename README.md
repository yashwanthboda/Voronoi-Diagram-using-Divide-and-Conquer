# 🔷 Voronoi Diagram using Divide and Conquer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)
[![GitHub stars](https://img.shields.io/github/stars/yashwanthboda/Voronoi-Diagram-using-Divide-and-Conquer)](https://github.com/yashwanthboda/Voronoi-Diagram-using-Divide-and-Conquer/stargazers)

**An elegant Python implementation of Voronoi diagram generation using the divide-and-conquer algorithm**

*Interactive visualization • Step-by-step execution • Real-time nearest site queries*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Algorithm](#-algorithm) • [Demo](#-demo)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Algorithm Explanation](#-algorithm-explanation)
- [Nearest Site Query](#-nearest-site-query-feature)
- [File Structure](#-file-structure)
- [Examples](#-examples)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🌟 Overview

This project implements the **Voronoi diagram** construction algorithm using the **divide-and-conquer** approach. A Voronoi diagram partitions a plane into regions based on distance to a specified set of points (sites). Each region consists of all points closer to one particular site than to any other.

**Key Highlights:**
- ✨ Clean, modern GUI with intuitive controls
- 🎯 Real-time visualization of algorithm execution
- ⚡ O(1) nearest site queries using raster grid optimization
- 📊 Step-by-step animation mode
- 🎲 Random point generation for quick testing
- 📁 File input support for batch testing

---

## ✨ Features

### Core Functionality
- **🖱️ Interactive Point Input**: Click directly on canvas to add points
- **🎲 Random Point Generation**: Generate n random points automatically with validation
- **📂 File Input Support**: Load test cases from formatted input files
- **▶️ Auto-play Mode**: Watch the algorithm execute automatically with adjustable speed
- **⏭️ Step-by-step Visualization**: Execute one step at a time to understand the algorithm
- **🎨 Color-coded Display**: Different colors for left/right partitions and merge operations

### Advanced Features
- **🔍 Nearest Site Query (O(1))**: Find the closest Voronoi cell to any query point instantly
- **🔄 Convex Hull Visualization**: See the convex hull during merge operations
- **📊 Real-time Status Bar**: Display cursor position and query information
- **🎯 Visual Highlighting**: Interactive feedback for queries and operations
- **🧹 Clear & Reset**: Easy cleanup and restart functionality

- **🧹 Clear & Reset**: Easy cleanup and restart functionality

---

## 🚀 Installation

### Prerequisites
- **Python 3.x** (3.6 or higher recommended)
- **tkinter** (usually included with Python)

### Clone the Repository
```bash
git clone https://github.com/yashwanthboda/Voronoi-Diagram-using-Divide-and-Conquer.git
cd Voronoi-Diagram-using-Divide-and-Conquer
```

### Verify Installation
```bash
# Check Python version
python --version

# Run the application
cd src
python main.py
```

> **Note:** On some systems, you may need to use `python3` instead of `python`.

---

## ⚡ Quick Start

```bash
# Navigate to source directory
cd src

# Launch the application
python main.py
```

**First-time usage:**
1. Click **"🎲 Random Points"**
2. Enter number of points (try 10)
3. Click **"▶️ Execute"**
4. Watch the Voronoi diagram being created!
5. Click **"Query Mode"** and right-click anywhere to find nearest site

---

## 📖 Usage Guide

### Method 1: Manual Point Input
1. **Launch** the application
2. **Click** on the canvas to add points manually
3. **Click** "▶️ Execute" to generate the diagram
4. Use "⏭️ Step" for step-by-step visualization

### Method 2: Random Point Generation
1. **Click** "🎲 Random Points" button
2. **Enter** the number of vertices (1-100)
3. Points are generated with validation (no duplicates)
4. **Click** "▶️ Execute" or "▶️ Auto Play"

### Method 3: File Input
1. Create a test file: `testcase/test.in`
   ```
   5
   100 150
   300 200
   450 180
   200 400
   350 350
   ```
   Format: First line = number of points, followed by x y coordinates

2. **Click** "📂 Read Data"
3. **Click** "⏩ Next Data" to load test case
4. **Click** "▶️ Execute"

### Controls Reference

| Button | Function |
|--------|----------|
| 🗑️ **Clear** | Reset canvas and remove all points |
| 📂 **Read Data** | Load points from input file |
| 🎲 **Random Points** | Generate n random points |
| ▶️ **Execute** | Run complete algorithm |
| ⏭️ **Step** | Execute algorithm step-by-step |
| ▶️ **Auto Play** | Automatic step execution |
| **Query Mode** | Enable nearest site queries |
| ⏩ **Next Data** | Load next test case from file |

---

## 🧮 Algorithm Explanation

### Divide and Conquer Approach

The implementation follows the classic divide-and-conquer paradigm:

#### 1. **Divide Phase**
```
- Sort points by x-coordinate
- Recursively split into left and right halves
- Continue until base cases (2 or 3 points)
```

#### 2. **Base Cases**
- **2 Points**: Create perpendicular bisector
- **3 Points**: Compute circumcenter and construct 3 bisectors
  - Handle special case: collinear points

#### 3. **Conquer Phase**
```
- Compute Voronoi diagrams for left and right subsets
- Merge diagrams by finding the hyperplane separator
- Use convex hull tangent lines for merge guidance
```

#### 4. **Merge Process**
- Find upper and lower tangent lines of convex hulls
- Construct hyperplane from upper tangent downward
- Find intersections with existing edges
- Update and trim affected edges

### Time Complexity
- **Average Case**: O(n log n)
- **Worst Case**: O(n log n)
- **Space Complexity**: O(n)

### Visual Color Coding
- 🔴 **Red lines**: Left partition edges
- 🔵 **Blue lines**: Right partition edges
- ⚫ **Black lines**: Hyperplane (merge separator)
- � **Purple lines**: Convex hull edges
- 🟠 **Orange lines**: Upper and lower common tangent lines (thicker)
- 🔷 **Light blue**: Merged edges

---

## 🔍 Nearest Site Query Feature

### Problem
> *"Which site is nearest to an arbitrary query point q?"*

**Real-world applications:**
- 🏥 Find nearest hospital/emergency service
- ⛽ Locate closest gas station
- 🏪 Store location optimization
- 🗺️ Geographic information systems (GIS)
- 🎮 Game AI pathfinding

### Solution: Raster Grid Approach

#### How It Works
1. **Preprocessing** (after Voronoi execution):
   - Build a 2D grid (300×300 cells for 600×600 canvas)
   - Each cell stores the index of its nearest site
   - Grid resolution: 2 pixels per cell

2. **Query** (real-time):
   - Convert query point (x, y) to grid coordinates
   - Lookup nearest site in **O(1)** constant time
   - Display visual feedback

#### Performance
| Metric | Value |
|--------|-------|
| **Query Time** | O(1) - Instant |
| **Memory Usage** | ~360 KB |
| **Accuracy** | ±1 pixel |
| **Grid Size** | 90,000 cells |

#### Usage
1. Generate Voronoi diagram (any method)
2. Click **"Query Mode"** (button turns green)
3. **Right-click** anywhere on canvas
4. See highlighted nearest site with distance

#### Visual Feedback
- 🟡 **Yellow dot**: Your query location
- 🟢 **Green circle**: Nearest site highlighted
- **Dashed line**: Connection showing distance
- **Label**: Site index and distance value

---

## 📁 File Structure

```
Voronoi-Diagram-using-Divide-and-Conquer/
│
├── src/
│   ├── main.py              # Entry point
│   ├── voronoi.py           # Main GUI and application logic
│   ├── algo.py              # Divide-and-conquer algorithm
│   ├── line.py              # Geometric classes (Line, ThreePoints)
│   ├── drawline.py          # Drawing utilities
│   └── read.py              # File input handler
│
├── testcase/
│   └── test.in              # Sample test cases (create as needed)
│
├── README.md                # This file
├── QUERY_FEATURE_GUIDE.md   # Detailed query feature documentation
├── QUICK_REFERENCE.txt      # Quick reference card
├── demo_query_performance.py # Performance benchmark
└── test_query_feature.py    # Feature demonstration
```

---

## 🎨 Examples

### Example 1: Simple Configuration
```
Points: [(100, 100), (300, 150), (500, 400)]
Result: 3 Voronoi regions with perpendicular bisectors
```

### Example 2: Complex Scenario
```
Generate 20 random points → Execute → Step-by-step visualization
Observe: Recursive splitting, convex hulls, merge operations
```

### Example 3: Nearest Site Query
```
20 sites distributed → Execute → Enable Query Mode
Right-click at (250, 300) → Instantly shows nearest site
Use case: "Where is the closest hospital to this location?"
```

---

## 🎯 Technical Highlights

### Algorithm Optimizations
- ✅ Efficient point sorting with stable sort
- ✅ Convex hull computation for merge guidance
- ✅ Intersection detection with numerical stability
- ✅ Edge case handling (collinear points, duplicates)

### Data Structures
- **Line Class**: Perpendicular bisectors with slope and endpoints
- **ThreePoints Class**: Triangle circumcenter computation
- **Grid Structure**: 2D array for O(1) queries
- **History Tracking**: Step-by-step visualization support

### GUI Features
- **Modern Design**: Color-coded buttons with emojis
- **Responsive**: Real-time cursor tracking
- **Intuitive**: Clear visual feedback for all operations
- **Robust**: Input validation and error handling

## 👨‍💻 Author

**Yashwanth Boda**
- GitHub: [@yashwanthboda](https://github.com/yashwanthboda), [@harsha-050](https://github.com/harsha-050), [@Chaitanya1104](https://github.com/Chaitanya1104)
- Repository: [Voronoi-Diagram-using-Divide-and-Conquer](https://github.com/yashwanthboda/Voronoi-Diagram-using-Divide-and-Conquer)
