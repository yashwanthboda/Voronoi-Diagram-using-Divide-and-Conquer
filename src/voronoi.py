"""
## Group-3 (22114022_22114050_22114082) - Boda Yashwanth, Majji Harsha Vardhan and Sadineni Chaitanya
## Date: Oct 28, 2025
## voronoi.py - GUI implementation and main application logic for Voronoi Diagram visualization
##              Includes interactive features, query mode, and step-by-step execution
"""

from read import readInput
from algo import *
import tkinter as tk
from tkinter import simpledialog
from line import *
import random

r = 3
color_idx = 0
color_list = [
    "#FF0000", "#00FF00", "#0000FF", "#FF00FF", "#00FFFF",  # bright primary accents
    "#800000", "#008000", "#000080", "#808000", "#800080", "#008080",  # darker tones
    "#FFA500", "#A52A2A", "#7FFF00", "#DC143C", "#00CED1", "#FF1493",  # warm and vivid shades
    "#1E90FF", "#B22222", "#228B22", "#DAA520", "#4B0082", "#FF69B4",  # blue, green, gold, indigo, pink
    "#CD5C5C", "#20B2AA", "#90EE90", "#FFD700",  # softer palette
    "#9932CC", "#E9967A", "#F08080", "#66CDAA", "#8FBC8F", "#C71585"   # additional mixed colors
]

def draw_line(canvas, p1, p2):
    canvas.create_line(p1[0], p1[1], p2[0], p2[1], width=2, fill=color_list[color_idx % len(color_list)])
    color_idx += 1


class Voronoi:
    def __init__(self, root):
        self.root = root
        self.root.title("Voronoi Diagram Visualizer")
        self.root.configure(bg='#f0f0f0')
        
        # Set minimum window size and make it responsive
        self.root.minsize(900, 700)
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate appropriate canvas size based on screen
        max_canvas_size = min(screen_height - 300, 800)  # Leave room for buttons and title
        self.canvas_width = max_canvas_size
        self.canvas_height = max_canvas_size
        
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
        self.autoplay = False
        # Nearest site query feature
        self.query_mode = False
        self.voronoi_grid = None
        self.grid_resolution = 2  # pixel size of each grid cell (lower = more accurate)
        self.highlighted_site = None
        self.highlight_objects = []

        self.autoplay_speed = 500  # milliseconds between steps

        # Title Label
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        title_frame.pack(fill='x', pady=(0, 5))
        title_label = tk.Label(title_frame, text="Voronoi Diagram Visualizer", 
                              font=("Arial", 14, "bold"), bg='#2c3e50', fg='white')
        title_label.pack(pady=8)

        # Status/Message frame (above canvas)
        self.message_frame = tk.Frame(self.root, bg='#f0f0f0', height=35)
        self.message_frame.pack(fill='x', padx=10)
        self.message_label = tk.Label(self.message_frame, text="", 
                                      font=("Arial", 11, "bold"), 
                                      bg='#f0f0f0', fg='#2c3e50',
                                      pady=8)
        self.message_label.pack()

        # create canvas with border
        canvas_frame = tk.Frame(self.root, bg='#34495e', bd=2, relief='solid')
        canvas_frame.pack(padx=10, pady=5)
        self.canvas = tk.Canvas(canvas_frame, width=self.canvas_width, height=self.canvas_height, bg="white", 
                               highlightthickness=0)
        self.canvas.pack()

        # Button container frame - centers the buttons
        button_container = tk.Frame(self.root, bg='#f0f0f0')
        button_container.pack(pady=8, fill='x')
        
        # Button frame - holds the actual buttons
        button_frame = tk.Frame(button_container, bg='#f0f0f0')
        button_frame.pack()

        # Button styling - slightly smaller for better fit
        btn_config = {
            'font': ("Arial", 9, "bold"),
            'bd': 0,
            'relief': 'flat',
            'padx': 12,
            'pady': 6,
            'cursor': 'hand2'
        }

        # clear button
        self.clear_button = tk.Button(button_frame, text="🗑️ Clear", 
                                      bg='#e74c3c', fg='white', 
                                      activebackground='#c0392b',
                                      command=self.clear_canvas, **btn_config)
        self.clear_button.pack(side='left', padx=1)

        # read data button
        self.read_data_button = tk.Button(button_frame, text="📂 Read", 
                                          bg='#3498db', fg='white',
                                          activebackground='#2980b9',
                                          command=self.read_data, **btn_config)
        self.read_data_button.pack(side='left', padx=1)

        # random points button
        self.random_button = tk.Button(button_frame, text="🎲 Random", 
                                       bg='#9b59b6', fg='white',
                                       activebackground='#8e44ad',
                                       command=self.generate_random_points, **btn_config)
        self.random_button.pack(side='left', padx=1)

        # execute button - Run complete diagram
        self.execute_button = tk.Button(button_frame, text="▶️ Run", 
                                        bg='#27ae60', fg='white',
                                        activebackground='#229954',
                                        command=self.exeDraw, **btn_config)

        # step button - Step through construction
        self.next_button = tk.Button(button_frame, text="⏩ Step", 
                                     bg='#16a085', fg='white',
                                     activebackground='#138d75',
                                     command=self.stepDraw, **btn_config)

        # auto-play button
        self.autoplay_button = tk.Button(button_frame, text="▶️ Auto", 
                                         bg='#f39c12', fg='white',
                                         activebackground='#d68910',
                                         command=self.toggle_autoplay, **btn_config)

        # read next data button - Load next test case
        self.read_next_data_button = tk.Button(button_frame, text="📄 Next", 
                                              bg='#34495e', fg='white',
                                              activebackground='#2c3e50',
                                              command=self.read_next_data, **btn_config)

        # query nearest site button - Better positioned and styled
        self.query_button = tk.Button(button_frame, text="🔍 Find", 
                                      bg='#e056fd', fg='white',
                                      activebackground='#c44ddb',
                                      command=self.toggle_query_mode, **btn_config)
        
        # Status bar
        status_frame = tk.Frame(self.root, bg='#ecf0f1', relief='sunken', bd=1)
        status_frame.pack(side='bottom', fill='x')
        
        self.position_label = tk.Label(status_frame, text="", 
                                      font=("Consolas", 9), 
                                      bg='#ecf0f1', fg='#2c3e50')
        self.position_label.pack(side='right', padx=10, pady=5)

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
        self.random_button.pack_forget()
        self.execute_button.pack(side='left', padx=1)
        self.next_button.pack(side='left', padx=1)
        self.autoplay_button.pack(side='left', padx=1)
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
        self.execute_button.pack(side='left', padx=1)
        self.next_button.pack(side='left', padx=1)
        self.autoplay_button.pack(side='left', padx=1)
        
        # Generate n random points with some margin from borders
        margin = 30
        for i in range(n):
            x = random.randint(margin, self.canvas_width - margin)
            y = random.randint(margin, self.canvas_height - margin)
            # Check for duplicates
            while (x, y) in self.points:
                x = random.randint(margin, self.canvas_width - margin)
                y = random.randint(margin, self.canvas_height - margin)
            
            self.points.append((x, y))
            self.draw_point(x, y)
            print(f'Generated point {i+1}: ({x},{y})')
        
        print(f'Successfully generated {n} random points')
        
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.points.clear()
        self.autoplay = False
        self.autoplay_button.config(text="▶️ Auto", bg='#f39c12')
        # Clear completion message
        self.message_label.config(text="", bg='#f0f0f0')
        # Reset buttons
        self.execute_button.pack_forget()
        self.next_button.pack_forget()
        self.autoplay_button.pack_forget()
        self.read_next_data_button.pack_forget()
        self.query_button.pack_forget()
        self.read_data_button.pack(side='left', padx=1)
        self.random_button.pack(side='left', padx=1)
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
        self.random_button.pack_forget()
        self.read_next_data_button.pack(side='left', padx=1)
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
        
        # Show control buttons
        self.read_next_data_button.pack(side='left', padx=1)
        self.execute_button.pack(side='left', padx=1)
        self.next_button.pack(side='left', padx=1)
        self.autoplay_button.pack(side='left', padx=1)
        
        n = int(self.data[self.data_index])
        if n == 0:
            print('Zero points read; stopping file test')
            self.read_data_button.pack(side='left', padx=1)
            self.random_button.pack(side='left', padx=1)
            self.read_next_data_button.pack_forget()
            self.execute_button.pack_forget()
            self.next_button.pack_forget()
            self.autoplay_button.pack_forget()
            return

        print(f'Number of points: {n}')
        for j in range(n):
            # print(self.data_index + j + 1)
            # print(self.data[self.data_index + j + 1])
            x, y = map(int, self.data[self.data_index + j + 1].split(' '))
            print(f'Coordinate: ({x},{y})')
            self.points.append((x, y))
            self.draw_point(x, y)
        self.data_index += n + 1

    def execute(self):
        pointNum = len(self.points)
        if pointNum<2:
            print('Fewer than two points; cannot draw Voronoi diagram')
            return [],[]
        if has_duplicates(self.points):
            print('Duplicate points detected; cannot draw Voronoi diagram')
            return [],[]
        lines, convexhull, history, cvh_history= sol(self.points, pointNum, canvas=self.canvas)
        self.cvhLastIdx = len(cvh_history)-1
        print("cvh_history length:",len(cvh_history))
        return history, cvh_history
    
    def exeDraw(self):
        # Clear any previous completion message
        self.message_label.config(text="", bg='#f0f0f0')
        if not self.stepMode:
            self.history, self.cvh_history = self.execute()
            if self.history == []:
                return
            self.stepMode = True
        self.history_t = len(self.history)-1
        self.cvh_history_t = len(self.cvh_history)-1
        self.stepDraw()
        
        # After execution completes, clear canvas and redraw only final Voronoi edges
        # This removes convex hull and tangent lines from the display
        self.clear_lines()
        # Draw only the final Voronoi diagram (last entry in history, which contains final edges)
        if self.history:
            draw_lines(self.history[-1], self.canvas)
        
        # Build grid for query mode after execution
        if self.voronoi_grid is None and len(self.points) >= 2:
            self.build_voronoi_grid()
            # Show query button
            self.query_button.pack(side='left', padx=1)

    def stepDraw(self):
        if not self.stepMode:
            # Clear any previous completion message
            self.message_label.config(text="", bg='#f0f0f0')
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
                self.query_button.pack(side='left', padx=1)
            self.autoplay = False
            self.autoplay_button.config(text="▶️ Auto", bg='#f39c12')
            # Display completion message
            self.show_completion_message()
        elif self.autoplay:
            # Continue auto-playing
            self.root.after(self.autoplay_speed, self.stepDraw)
        
    def toggle_autoplay(self):
        """Toggle auto-play mode"""
        self.autoplay = not self.autoplay
        if self.autoplay:
            self.autoplay_button.config(text="⏸️ Pause", bg='#e67e22')
            # Start auto-play
            if not self.stepMode:
                self.stepDraw()
            else:
                self.root.after(self.autoplay_speed, self.stepDraw)
        else:
            self.autoplay_button.config(text="▶️ Auto", bg='#f39c12')
    
    def clear_lines(self):
        self.canvas.delete("all")
        for p in self.points:
            self.draw_point(p[0], p[1])
    
    def show_completion_message(self):
        """Display completion message above the canvas"""
        message = "✅ Voronoi Diagram Created Successfully!"
        self.message_label.config(text=message, bg='#2ecc71', fg='white')
        print(message)
    
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
            
            self.query_button.config(bg='#2ecc71', text='🔍 Find Site: ON')
            print("Query mode ON: Right-click anywhere to find nearest site")
        else:
            self.query_button.config(bg='#e056fd', text='🔍 Find Site')
            # Clear highlights
            for obj in self.highlight_objects:
                self.canvas.delete(obj)
            self.highlight_objects.clear()
            print("Query mode OFF")
