"""
## Group-3 (22114022_22114050_22114082) - Boda Yashwanth, Majji Harsha Vardhan and Sadineni Chaitanya
## Date: Oct 28, 2025
## drawline.py - Drawing utilities and color coding for Voronoi Diagram visualization
##               Handles rendering of Voronoi edges, convex hull, tangent lines, and hyperplanes
"""

import tkinter as tk
from line import Line

color_idx = 0

color_list = [
    "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", # bright primary accents
    "#800000", "#008000", "#000080", "#808000", "#800080", "#008080",  # darker tones
    "#FFA500", "#A52A2A", "#7FFF00", "#DC143C", "#00CED1", "#FF1493",  # warm and vivid shades
    "#1E90FF", "#B22222", "#228B22", "#DAA520", "#4B0082", "#FF69B4",  # blue, green, gold, indigo, pink
    "#CD5C5C", "#20B2AA", "#90EE90", "#ADD8E6", "#D3D3D3", "#FFD700",  # softer palette
    "#9932CC", "#E9967A", "#F08080", "#66CDAA", "#ADD8E6", "#C71585"   # additional mixed colors
]

def draw_line(canvas, p1, p2, line):
    if line.erase:
        return
    
    w = 2
    
    # Priority order for color assignment:
    # 1. Tangent lines (upper/lower common tangent) - BRIGHT ORANGE
    if line.isTengent:
        color = "#FF8C00"  # Dark Orange for tangent lines
        w = 3  # Make tangent lines thicker
    # 2. Convex hull edges - PURPLE
    elif line.isConvexHull:
        color = "#9370DB"  # Medium Purple for convex hull
        w = 2
    # 3. Hyperplane/merge line - BLACK
    elif line.isHyper:
        color = "black"
        w = 2
    # 4. After merge - LIGHT BLUE
    elif line.afterMerge:
        color = "#ADD8E6"
        w = 2
    # 5. Left partition - RED, Right partition - BLUE
    else:
        color = "#DC143C" if line.Lpart else "#1E90FF"
        w = 2
    
    canvas.create_line(p1[0], p1[1], p2[0], p2[1], width=w, fill=color)
    # color_idx += 1

def draw_lines(lines: list[list[Line]], canvas):
    # print("Output lines:", lines)
    # print("Number of segments: ", len(lines))
    # print("drawLINE:",lines)
    for line in lines:
        # if type(line) == list:
        #     line = line[0]
        p1,p2 = line.points if line.isConvexHull else line.canvasLine
        # print("Output segment: ",p1,p2)

        draw_line(canvas, p1, p2, line)
