# Voronoi Diagram using Divide and Conquer

A Python implementation of Voronoi diagram generation using the divide-and-conquer algorithm with an interactive GUI.

## Features

- **Interactive Point Input**: Click on the canvas to manually add points
- **Random Point Generation**: Generate n random points automatically
- **File Input**: Read test cases from input files
- **Step-by-step Visualization**: Watch the algorithm execute step by step
- **Convex Hull Display**: Visualize the convex hull during merge operations

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
