from read import readInput
from algo import *
import tkinter as tk
from tkinter import simpledialog
from line import *
import random

r = 3
color_idx = 0
color_list = [
    "#FF0000", "#00FF00", "#0000FF", "#FF00FF", "#00FFFF",  # 紅綠藍黃紫青
    "#800000", "#008000", "#000080", "#808000", "#800080", "#008080",  # 深色系
    "#FFA500", "#A52A2A", "#7FFF00", "#DC143C", "#00CED1", "#FF1493",  # 橙褐草紅青粉
    "#1E90FF", "#B22222", "#228B22", "#DAA520", "#4B0082", "#FF69B4",  # 藍綠金靛粉紅
    "#CD5C5C", "#20B2AA", "#90EE90", "#FFD700",  # 柔色
    "#9932CC", "#E9967A", "#F08080", "#66CDAA", "#8FBC8F", "#C71585"   # 更多混色
]

def draw_line(canvas, p1, p2):
    canvas.create_line(p1[0], p1[1], p2[0], p2[1], width=2, fill=color_list[color_idx % len(color_list)])
    color_idx += 1


class Voronoi:
    def __init__(self, root):
        self.root = root
        self.root.title("Voronoi")
        self.points = []
        self.data = []
        self.data_index = 0
        self.waiting = False
        self.cvh_history = []
        self.cvh_history_t = False
        self.history = []
        self.history_t = None
        self.stepMode = False
        self.merge_history = []
        self.mergeidx = 0
        
        # Nearest site query feature
        self.query_mode = False
        self.voronoi_grid = None
        self.grid_resolution = 2  # pixel size of each grid cell (lower = more accurate)
        self.canvas_width = 600
        self.canvas_height = 600
        self.highlighted_site = None
        self.highlight_objects = []

        # create canvas
        self.canvas = tk.Canvas(self.root, width=600, height=600, bg="white")
        self.canvas.pack()

        # clear button
        self.clear_button = tk.Button(self.root, text="Clear", font=("consolas"), command=self.clear_canvas)
        self.clear_button.pack(side='left', padx=3, pady=3)

        # read data button
        self.read_data_button = tk.Button(self.root, text="Read Data", font=("consolas"), command = self.read_data)
        self.read_data_button.pack(side='left', padx=3, pady=3)

        # random points button
        self.random_button = tk.Button(self.root, text="Random Points", font=("consolas"), command=self.generate_random_points)
        self.random_button.pack(side='left', padx=3, pady=3)

        # execute button
        self.execute_button = tk.Button(self.root, text="Execute", font=("consolas"), command=self.exeDraw)

        # execute button
        self.next_button = tk.Button(self.root, text="Step", font=("consolas"), command=self.stepDraw)

        # read next data button
        self.read_next_data_button = tk.Button(self.root, text="Next Data", font=("consolas"), command=self.read_next_data)

        # query nearest site button
        self.query_button = tk.Button(self.root, text="Query Mode", font=("consolas"), command=self.toggle_query_mode, bg='lightgray')
        
        self.position_label = tk.Label(text="", font=("consolas"))
        self.position_label.pack(side='right', pady=3)

        # binding mouse click to draw points
        self.canvas.bind("<Motion>", self.update_position)
        self.canvas.bind("<Button-1>", self.draw_point_event)
        self.canvas.bind("<Button-3>", self.query_nearest_site)  # Right-click for query

    def draw_point_event(self, event):
        # If in query mode, don't add points
        if self.query_mode:
            return
            
        self.read_data_button.pack_forget()
        self.read_next_data_button.pack_forget()
        self.execute_button.pack(side='left')
        self.next_button.pack(side='left')
        self.points.append((event.x, event.y))
        self.draw_point(event.x, event.y)
        print(f'({event.x},{event.y})')

    def draw_point(self, x, y, color='red'):
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color)
        bx,by = 15,15
        if y < 300 and x>300:
            bx = -60
        elif y > 300 and x<300:
            by = -15
        elif y > 300 and x>300:
            bx,by = -60,-15
        self.canvas.create_text(x+bx, y+by, text=f"({int(x)},{int(y)})", anchor="w", font=("consolas", 8))
    
    def generate_random_points(self):
        """Generate n random points on the canvas"""
        # Ask user for number of points
        n = simpledialog.askinteger("Random Points", "Enter number of vertices (n):", 
                                     minvalue=1, maxvalue=100)
        if n is None:  # User cancelled
            return
        
        # Clear existing points
        self.clear_canvas()
        self.points.clear()
        
        # Hide read data buttons and show execute buttons
        self.read_data_button.pack_forget()
        self.read_next_data_button.pack_forget()
        self.random_button.pack_forget()
        self.execute_button.pack(side='left', padx=3)
        self.next_button.pack(side='left', padx=3, pady=3)
        
        # Generate n random points with some margin from borders
        margin = 30
        for i in range(n):
            x = random.randint(margin, 600 - margin)
            y = random.randint(margin, 600 - margin)
            # Check for duplicates
            while (x, y) in self.points:
                x = random.randint(margin, 600 - margin)
                y = random.randint(margin, 600 - margin)
            
            self.points.append((x, y))
            self.draw_point(x, y)
            print(f'Generated point {i+1}: ({x},{y})')
        
        print(f'Successfully generated {n} random points')
        
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.points.clear()
        # Reset buttons
        self.execute_button.pack_forget()
        self.next_button.pack_forget()
        self.read_next_data_button.pack_forget()
        self.query_button.pack_forget()
        self.read_data_button.pack(side='left', padx=3, pady=3)
        self.random_button.pack(side='left', padx=3, pady=3)
        # Reset query mode state
        self.query_mode = False
        self.voronoi_grid = None
        self.highlighted_site = None
        self.highlight_objects.clear()

    def read_data(self):
        self.data = readInput()
        print(self.data)
        self.data_index = 0
        self.read_data_button.pack_forget()
        self.read_next_data_button.pack(side='left', padx=3, pady=3)
        self.read_next_data()
        

    def read_next_data(self):
        self.clear_canvas()
        self.points.clear()
        self.history.clear()
        self.merge_history.clear()
        self.mergeidx = 0
        self.cvh_history.clear()
        self.cvh_history_t = 0
        self.stepMode = False
        self.execute_button.pack(side='left', padx=3)
        self.next_button.pack(side='left', padx=3, pady=3)
        n = int(self.data[self.data_index])
        if n == 0:
            print('讀入點數為零，檔案測試停止')
            self.read_data_button.pack(side='left', padx=3, pady=3)
            self.read_next_data_button.pack_forget()
            self.execute_button.pack_forget()
            self.next_button.pack_forget()
            return

        print(f'點數：{n}')
        for j in range(n):
            # print(self.data_index + j + 1)
            # print(self.data[self.data_index + j + 1])
            x, y = map(int, self.data[self.data_index + j + 1].split(' '))
            print(f'座標：({x},{y})')
            self.points.append((x, y))
            self.draw_point(x, y)
        self.data_index += n + 1

    def execute(self):
        pointNum = len(self.points)
        if pointNum<2:
            print('少於兩點，無法繪製Voronoi圖')
            return [],[]
        if has_duplicates(self.points):
            print('有兩個點重複，無法繪製Voronoi圖')
            return [],[]
        lines, convexhull, history, cvh_history= sol(self.points, pointNum, canvas=self.canvas)
        self.cvhLastIdx = len(cvh_history)-1
        print("cvh_history length:",len(cvh_history))
        return history, cvh_history
    
    def exeDraw(self):
        if not self.stepMode:
            self.history, self.cvh_history = self.execute()
            if self.history == []:
                return
            self.stepMode = True
        self.history_t = len(self.history)-1
        self.cvh_history_t = len(self.cvh_history)-1
        self.stepDraw()
        
        # Build grid for query mode after execution
        if self.voronoi_grid is None and len(self.points) >= 2:
            self.build_voronoi_grid()
            # Show query button
            self.query_button.pack(side='left', padx=3, pady=3)

    def stepDraw(self):
        if not self.stepMode:
            self.clear_lines()
            self.history.clear()
            self.cvh_history.clear()
            self.cvh_history_t = 0
            self.merge_history.clear()
            self.mergeidx = 0
            self.history, self.cvh_history = self.execute()
            if self.history == []:
                return
            self.stepMode = True
            self.history_t = 0
            print(len(self.history))
        else:
            for line in self.history[self.history_t]: # clear the old lines if hyperplane exist or it has been merged
                if line.afterMerge:
                    self.merge_history.append((self.merge_history[-1] if self.merge_history else []) + self.history[self.history_t]) # backup merge subgraph
                if line.isHyper:
                    self.clear_lines()
                    if len(self.merge_history) and (not self.cvh_history_t >= self.cvhLastIdx):
                        draw_lines(self.merge_history[-1], self.canvas)
                    break
        
        if (self.cvh_history_t+1) % 3 == 0:
            self.clear_lines()
            if len(self.merge_history) and (not self.cvh_history_t >= self.cvhLastIdx):
                draw_lines(self.merge_history[-1], self.canvas)

        if len(self.points)>3 and (self.cvh_history_t+1) %3 == 0 or len(self.history[self.history_t]) == 0:
            draw_lines(self.cvh_history[self.cvh_history_t], self.canvas)
            self.cvh_history_t += 1

        draw_lines(self.history[self.history_t], self.canvas)

        self.history_t +=1
        if self.history_t >= len(self.history):
            self.stepMode = False
            # Build grid when step execution completes
            if self.voronoi_grid is None and len(self.points) >= 2:
                self.build_voronoi_grid()
                # Show query button
                self.query_button.pack(side='left', padx=3, pady=3)
        
    def clear_lines(self):
        self.canvas.delete("all")
        for p in self.points:
            self.draw_point(p[0], p[1])
    
    def update_position(self, event):
        x, y = event.x, event.y
        status = f"Cursor : ({x}, {y})"
        
        # If in query mode and grid is built, show nearest site
        if self.query_mode and self.voronoi_grid is not None:
            nearest_idx = self.query_grid(x, y)
            if nearest_idx is not None:
                nearest_site = self.points[nearest_idx]
                dist = ((x - nearest_site[0])**2 + (y - nearest_site[1])**2)**0.5
                status += f" | Nearest: Site {nearest_idx} ({int(nearest_site[0])},{int(nearest_site[1])}) - Dist: {dist:.1f}"
        
        self.position_label.config(text=status)
    
    def build_voronoi_grid(self):
        """Build a 2D grid storing the nearest site index for each cell (O(1) query)"""
        print("Building Voronoi query grid...")
        
        grid_w = self.canvas_width // self.grid_resolution
        grid_h = self.canvas_height // self.grid_resolution
        
        # Initialize grid
        self.voronoi_grid = [[None for _ in range(grid_w)] for _ in range(grid_h)]
        
        # For each grid cell, find the nearest site
        for row in range(grid_h):
            for col in range(grid_w):
                # Convert grid coordinates to canvas coordinates (center of cell)
                x = col * self.grid_resolution + self.grid_resolution / 2
                y = row * self.grid_resolution + self.grid_resolution / 2
                
                # Find nearest site by brute force distance check
                min_dist = float('inf')
                nearest_idx = 0
                
                for idx, site in enumerate(self.points):
                    dist = (x - site[0])**2 + (y - site[1])**2
                    if dist < min_dist:
                        min_dist = dist
                        nearest_idx = idx
                
                self.voronoi_grid[row][col] = nearest_idx
        
        print(f"Grid built: {grid_h}x{grid_w} cells ({grid_h * grid_w} total)")
        return self.voronoi_grid
    
    def query_grid(self, x, y):
        """Query which site is nearest to point (x, y) in O(1) time"""
        if self.voronoi_grid is None:
            return None
        
        # Convert canvas coordinates to grid coordinates
        col = int(x / self.grid_resolution)
        row = int(y / self.grid_resolution)
        
        # Bounds check
        grid_h = len(self.voronoi_grid)
        grid_w = len(self.voronoi_grid[0]) if grid_h > 0 else 0
        
        if 0 <= row < grid_h and 0 <= col < grid_w:
            return self.voronoi_grid[row][col]
        return None
    
    def query_nearest_site(self, event):
        """Handle right-click to query and highlight nearest site"""
        if not self.query_mode:
            return
        
        if self.voronoi_grid is None:
            print("Please execute the Voronoi diagram first!")
            return
        
        x, y = event.x, event.y
        nearest_idx = self.query_grid(x, y)
        
        if nearest_idx is not None:
            self.highlight_site(nearest_idx, (x, y))
    
    def highlight_site(self, site_idx, query_point):
        """Highlight the nearest site and show visual feedback"""
        # Clear previous highlights
        for obj in self.highlight_objects:
            self.canvas.delete(obj)
        self.highlight_objects.clear()
        
        site = self.points[site_idx]
        
        # Draw query point
        query_marker = self.canvas.create_oval(
            query_point[0] - 5, query_point[1] - 5,
            query_point[0] + 5, query_point[1] + 5,
            fill='yellow', outline='orange', width=2
        )
        self.highlight_objects.append(query_marker)
        
        # Highlight the nearest site with a larger circle
        highlight_circle = self.canvas.create_oval(
            site[0] - 10, site[1] - 10,
            site[0] + 10, site[1] + 10,
            outline='green', width=3, fill=''
        )
        self.highlight_objects.append(highlight_circle)
        
        # Draw line from query to nearest site
        line = self.canvas.create_line(
            query_point[0], query_point[1],
            site[0], site[1],
            fill='green', width=2, dash=(4, 4)
        )
        self.highlight_objects.append(line)
        
        # Show distance label
        dist = ((query_point[0] - site[0])**2 + (query_point[1] - site[1])**2)**0.5
        label = self.canvas.create_text(
            (query_point[0] + site[0]) / 2,
            (query_point[1] + site[1]) / 2 - 10,
            text=f"Site {site_idx}\nDist: {dist:.1f}",
            font=("consolas", 10, "bold"),
            fill='green'
        )
        self.highlight_objects.append(label)
        
        print(f"Query at ({query_point[0]:.0f}, {query_point[1]:.0f}) -> Nearest: Site {site_idx} at {site}, Distance: {dist:.2f}")
    
    def toggle_query_mode(self):
        """Toggle between normal mode and query mode"""
        if len(self.points) < 2:
            print("Please add at least 2 points first!")
            return
        
        self.query_mode = not self.query_mode
        
        if self.query_mode:
            # Build grid if not already built
            if self.voronoi_grid is None:
                self.build_voronoi_grid()
            
            self.query_button.config(bg='lightgreen', text='Query Mode: ON')
            print("Query mode ON: Right-click anywhere to find nearest site")
        else:
            self.query_button.config(bg='lightgray', text='Query Mode')
            # Clear highlights
            for obj in self.highlight_objects:
                self.canvas.delete(obj)
            self.highlight_objects.clear()
            print("Query mode OFF")