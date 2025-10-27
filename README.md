# Voronoi Diagram using Divide and Conquer

A Python implementation of Voronoi diagram generation using the divide-and-conquer algorithm with an interactive GUI and real-time nearest site queries.

## Features

- **Interactive Point Input**: Click on the canvas to manually add points
- **Random Point Generation**: Generate n random points automatically
- **File Input**: Read test cases from input files
- **Step-by-step Visualization**: Watch the algorithm execute step by step
- **Convex Hull Display**: Visualize the convex hull during merge operations
- **🆕 Nearest Site Query (NEW!)**: Find the nearest Voronoi cell to any query point in O(1) time using a raster grid approach

## Installation

### Requirements
- Python 3.x
- tkinter (usually comes with Python)

### Setup
```bash
git clone https://github.com/yashwanthboda/Voronoi-Diagram-using-Divide-and-Conquer.git
cd Voronoi-Diagram-using-Divide-and-Conquer/src
python main.py
```

## Usage

### 1. Random Point Generation (New Feature!)
1. Click the **"Random Points"** button
2. Enter the number of vertices (n) you want to generate
3. The application will randomly generate n points on the canvas
4. Click **"Execute"** to generate the Voronoi diagram
5. Click **"Step"** for step-by-step visualization

### 2. Manual Point Input
1. Click on the canvas to add points manually
2. Each click adds a new point
3. Click **"Execute"** to generate the Voronoi diagram

### 3. File Input
1. Create a test file in `testcase/test.in` format:
   ```
   <number_of_points>
   <x1> <y1>
   <x2> <y2>
   ...
   ```
2. Click **"Read Data"** button
3. Click **"Next Data"** to load the test case
4. Click **"Execute"** to generate the Voronoi diagram

### 4. Controls
- **Clear**: Clear all points and reset the canvas
- **Execute**: Run the complete algorithm at once
- **Step**: Execute the algorithm step by step
- **Next Data**: Load the next test case from file
- **Query Mode**: Enable/disable nearest site query mode

### 5. Nearest Site Query (Real-World Application!)

This feature answers the question: **"Which site is nearest to an arbitrary query point q?"**

**Real-world applications:**
- 🏥 Find nearest hospital/emergency service
- 🏪 Locate closest store/facility
- 📍 GPS navigation and location services
- 🗺️ Geographic information systems (GIS)

**How it works:**
1. After executing the Voronoi diagram, the system builds a **raster grid** (2D array)
2. Each grid cell stores the index of its nearest site
3. Grid resolution: 2 pixels (configurable for accuracy vs. memory tradeoff)
4. Query time: **O(1)** - instant lookup!

**Usage:**
1. Generate points and execute the Voronoi diagram
2. Click the **"Query Mode"** button (turns green when active)
3. **Right-click** anywhere on the canvas
4. The system will:
   - Show your query point as a **yellow dot**
   - Highlight the nearest site with a **green circle**
   - Draw a **dashed line** connecting them
   - Display the **site index and distance**
5. Hover your mouse to see real-time nearest site information in the status bar

**Technical Details:**
- **Grid Resolution**: 2px cells = 300×300 grid = 90,000 cells for 600×600 canvas
- **Memory Usage**: ~360KB for grid storage (very efficient!)
- **Build Time**: O(n × grid_cells) one-time preprocessing
- **Query Time**: O(1) constant time lookup
- **Accuracy**: Perfect within grid resolution (±1 pixel)

**Example Use Case:**
```
Scenario: Emergency services optimization
- Red dots: Hospital locations (Voronoi sites)
- User clicks anywhere in the city (query point)
- System instantly shows nearest hospital and distance
- Critical for emergency response time optimization
```

## Algorithm

The implementation uses a divide-and-conquer approach:
1. Sort points by x-coordinate
2. Recursively divide points into left and right subsets
3. Solve base cases (2 or 3 points)
4. Merge left and right Voronoi diagrams by finding the hyperplane
5. Update the diagram based on convex hull tangent lines

## File Structure

```
src/
├── main.py         # Entry point
├── voronoi.py      # GUI and main application logic
├── algo.py         # Divide-and-conquer algorithm
├── line.py         # Geometric classes (Line, ThreePoints)
├── drawline.py     # Drawing utilities
└── read.py         # File input handler
```

## Color Coding

- **Red points**: Voronoi cell centers
- **Red lines**: Left partition edges
- **Blue lines**: Right partition edges  
- **Black lines**: Hyperplane (merge line)
- **Gray lines**: Convex hull edges
- **Green lines**: Tangent lines
- **Light blue**: Merged edges

## Example

```python
# Generate 10 random points and create Voronoi diagram
# 1. Run the application
# 2. Click "Random Points"
# 3. Enter 10
# 4. Click "Execute" or "Step"
```

## License

This project is open source and available for educational purposes.

## Author

yashwanthboda
