"""
## Group-3 (22114022_22114050_22114082) - Boda Yashwanth, Majji Harsha Vardhan and Sadineni Chaitanya
## Date: Oct 28, 2025
## read.py - File input handler for reading test cases
##           Reads point coordinates from input files for batch testing
"""

def readInput():
    try:
        with open('../testcase/test.in', 'r',encoding="utf-8") as file:
            data = file.readlines()
            li = [line.strip() for line in data if (line[0] != '#' and line != '\n')]
            return li
    except FileNotFoundError:
        print("Input file not found.")
        return []
    except Exception as e:
        print(f"An error occurred while reading the input file: {e}")
        return []