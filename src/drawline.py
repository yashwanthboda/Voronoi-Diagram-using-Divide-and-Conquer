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
    # Skip drawing convex hull lines
    if line.isConvexHull:
        return
    # global color_idx
    w =  2
    color = "#DC143C" if line.Lpart else "#1E90FF"
    color = "black" if line.isHyper else color#color_list[color_idx % len(color_list)]
    color = "#ADD8E6" if line.afterMerge else color
    color = "#00FF00" if line.isTengent else color
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
