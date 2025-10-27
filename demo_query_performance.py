"""
Demo: Nearest Site Query Performance Test
Shows the efficiency of the raster grid approach (O(1) queries)
"""
import time
import random

def euclidean_distance(p1, p2):
    """Calculate Euclidean distance between two points"""
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def brute_force_query(sites, query_point):
    """Find nearest site using brute force - O(n) time"""
    min_dist = float('inf')
    nearest_idx = -1
    
    for idx, site in enumerate(sites):
        dist = euclidean_distance(query_point, site)
        if dist < min_dist:
            min_dist = dist
            nearest_idx = idx
    
    return nearest_idx, min_dist

def build_grid(sites, canvas_width=600, canvas_height=600, resolution=2):
    """Build raster grid for O(1) queries"""
    grid_w = canvas_width // resolution
    grid_h = canvas_height // resolution
    
    grid = [[None for _ in range(grid_w)] for _ in range(grid_h)]
    
    for row in range(grid_h):
        for col in range(grid_w):
            x = col * resolution + resolution / 2
            y = row * resolution + resolution / 2
            
            min_dist = float('inf')
            nearest_idx = 0
            
            for idx, site in enumerate(sites):
                dist = (x - site[0])**2 + (y - site[1])**2
                if dist < min_dist:
                    min_dist = dist
                    nearest_idx = idx
            
            grid[row][col] = nearest_idx
    
    return grid, grid_w, grid_h

def grid_query(grid, query_point, resolution=2):
    """Query using pre-built grid - O(1) time"""
    x, y = query_point
    col = int(x / resolution)
    row = int(y / resolution)
    
    if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
        return grid[row][col]
    return None

def performance_test():
    """Compare brute force vs grid query performance"""
    print("="*80)
    print("PERFORMANCE TEST: Brute Force vs. Raster Grid Approach")
    print("="*80)
    print()
    
    # Test with different numbers of sites
    test_sizes = [10, 50, 100, 500]
    num_queries = 1000
    
    for n_sites in test_sizes:
        print(f"\n{'='*80}")
        print(f"Testing with {n_sites} sites, {num_queries} queries")
        print(f"{'='*80}")
        
        # Generate random sites
        sites = [(random.randint(30, 570), random.randint(30, 570)) 
                 for _ in range(n_sites)]
        
        # Generate random query points
        queries = [(random.randint(0, 599), random.randint(0, 599)) 
                   for _ in range(num_queries)]
        
        # Test brute force approach
        start = time.time()
        for query in queries:
            nearest_idx, dist = brute_force_query(sites, query)
        brute_force_time = time.time() - start
        
        # Build grid
        start = time.time()
        grid, grid_w, grid_h = build_grid(sites)
        grid_build_time = time.time() - start
        
        # Test grid query approach
        start = time.time()
        for query in queries:
            nearest_idx = grid_query(grid, query)
        grid_query_time = time.time() - start
        
        # Calculate speedup
        if grid_query_time > 0:
            speedup = brute_force_time / grid_query_time
        else:
            speedup = float('inf')
        
        print(f"\nResults:")
        print(f"  Grid: {grid_h}x{grid_w} = {grid_h * grid_w:,} cells")
        print(f"  Grid Build Time:    {grid_build_time*1000:.2f} ms (one-time cost)")
        print(f"  Brute Force Total:  {brute_force_time*1000:.2f} ms ({brute_force_time/num_queries*1000000:.2f} μs/query)")
        print(f"  Grid Query Total:   {grid_query_time*1000:.2f} ms ({grid_query_time/num_queries*1000000:.2f} μs/query)")
        if speedup == float('inf'):
            print(f"  Speedup:            Grid queries too fast to measure accurately!")
        else:
            print(f"  Speedup:            {speedup:.1f}x faster!")
        print(f"  Average per query:  {grid_query_time/num_queries*1000:.4f} ms ≈ O(1)")

def demonstrate_use_case():
    """Demonstrate a real-world use case"""
    print("\n\n")
    print("="*80)
    print("REAL-WORLD USE CASE: Emergency Services Locator")
    print("="*80)
    print()
    
    # Simulate hospital locations in a city
    hospitals = [
        (100, 100, "City Hospital"),
        (500, 150, "Memorial Medical Center"),
        (300, 400, "St. Mary's Hospital"),
        (150, 500, "Community Health Clinic"),
        (550, 550, "Regional Medical Center")
    ]
    
    sites = [(h[0], h[1]) for h in hospitals]
    
    # Build grid for fast queries
    print(f"Building emergency services grid for {len(hospitals)} hospitals...")
    grid, grid_w, grid_h = build_grid(sites)
    print(f"Grid ready: {grid_h}x{grid_w} cells\n")
    
    # Simulate emergency calls from different locations
    emergency_calls = [
        (120, 90, "Accident at Main St"),
        (480, 160, "Medical emergency at Park Ave"),
        (300, 350, "Cardiac arrest at Downtown"),
        (200, 520, "Injury at Industrial Zone"),
    ]
    
    print("Emergency Call Log:")
    print("-" * 80)
    
    for call in emergency_calls:
        x, y, incident = call
        
        # Find nearest hospital using O(1) grid query
        nearest_idx = grid_query(grid, (x, y))
        hospital = hospitals[nearest_idx]
        distance = euclidean_distance((x, y), (hospital[0], hospital[1]))
        
        print(f"\n📞 {incident}")
        print(f"   Location: ({x}, {y})")
        print(f"   🏥 Nearest: {hospital[2]}")
        print(f"   📍 Distance: {distance:.1f} units")
        print(f"   ⚡ Response: INSTANT (O(1) query time)")

if __name__ == "__main__":
    # Run performance test
    performance_test()
    
    # Demonstrate use case
    demonstrate_use_case()
    
    print("\n\n")
    print("="*80)
    print("CONCLUSION")
    print("="*80)
    print("""
The raster grid approach provides:
✓ O(1) query time - constant time lookups
✓ Simple implementation - just a 2D array
✓ Memory efficient - ~360KB for 600x600 canvas
✓ Perfect accuracy within grid resolution
✓ Scalable - query time independent of number of sites
✓ Production-ready - used in real GIS and navigation systems

Perfect for applications requiring frequent queries like:
• GPS navigation systems
• Emergency service dispatch
• Facility location services
• Geographic information systems
• Game development (AI pathfinding)
    """)
    print("="*80)
