"""
## Group-3 (22114022_22114050_22114082) - Boda Yashwanth, Majji Harsha Vardhan and Sadineni Chaitanya
## Date: Oct 28, 2025
## main.py - Entry point for Voronoi Diagram visualization application
"""

from voronoi import Voronoi
import tkinter as tk

def main():
    root = tk.Tk()
    app = Voronoi(root)
    root.mainloop()

if __name__ == "__main__":
    main()