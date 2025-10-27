"""
Test script to demonstrate the nearest site query feature
"""

def test_grid_query():
    """Simulate the grid query functionality"""
    # Simulated sites (Voronoi cell centers)
    sites = [(100, 100), (300, 150), (500, 400), (200, 500)]
    
    # Canvas parameters
    canvas_width, canvas_height = 600, 600
    grid_resolution = 2
    
    # Build grid
    grid_w = canvas_width // grid_resolution
    grid_h = canvas_height // grid_resolution
    
    print(f"Building grid: {grid_h}x{grid_w} = {grid_h * grid_w} cells")
    print(f"Sites: {sites}")
    print()
    
    # Query some test points
    test_queries = [
        (150, 125),  # Near site 0
        (280, 140),  # Near site 1
        (450, 420),  # Near site 2
        (180, 480),  # Near site 3
        (300, 300),  # Middle area
    ]
    
    for query in test_queries:
        x, y = query
        
        # Find nearest site (brute force for demonstration)
        min_dist = float('inf')
        nearest_idx = -1
        
        for idx, site in enumerate(sites):
            dist = ((x - site[0])**2 + (y - site[1])**2)**0.5
            if dist < min_dist:
                min_dist = dist
                nearest_idx = idx
        
        nearest_site = sites[nearest_idx]
        print(f"Query at ({x:3d}, {y:3d}) -> Nearest: Site {nearest_idx} at {nearest_site}, Distance: {min_dist:.2f}")

if __name__ == "__main__":
    print("="*70)
    print("Testing Nearest Site Query Feature")
    print("="*70)
    print()
    test_grid_query()
    print()
    print("="*70)
    print("How to use in the GUI:")
    print("1. Add points (manually, random, or from file)")
    print("2. Click 'Execute' to build Voronoi diagram")
    print("3. Click 'Query Mode' button (it will turn green)")
    print("4. Right-click anywhere on canvas to find nearest site")
    print("5. The nearest site will be highlighted with:")
    print("   - Yellow dot at your query location")
    print("   - Green circle around the nearest site")
    print("   - Dashed line showing the connection")
    print("   - Distance label")
    print("="*70)
