import re
import numpy as np

def calculate_canvas_size(file_path, layer_index):
    layer_end = str(layer_index + 1)
    layer_start = str(layer_index)
    
    coordinate_x = []
    coordinate_y = []

    read_layer = 0

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("layer" + layer_start):
                read_layer = 1
            elif line.startswith("layer" + layer_end):
                read_layer = 0
            if read_layer == 1 and line.startswith("("):
                matches = re.findall(r'\(([^,]+),([^)]+)\)', line)
                for match in matches:
                    x, y = map(float, match)
                    coordinate_x.append(x)
                    coordinate_y.append(y)
    
    if not coordinate_x or not coordinate_y:
        return 0, 0, 0, 0
    
    coords_array = np.array([coordinate_x, coordinate_y])
    x_min, y_min = np.min(coords_array, axis=1)
    x_max, y_max = np.max(coords_array, axis=1)
    
    return x_max, x_min, y_max, y_min

def calculate_marker_size(file_path, pattern_start):
    pattern_end = str(pattern_start + 1)
    pattern_start = str(pattern_start)
    
    coordinate_x = []
    coordinate_y = []
    read_pattern = 0
    read_marker = 0
    
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("pattern" + pattern_start):
                read_pattern = 1
            elif line.startswith("pattern" + pattern_end):
                read_pattern = 0
            if line.startswith("marker"):
                read_marker = 1
            elif not line.strip():  # 空行
                read_marker = 0
            if read_marker == 1 and read_pattern == 1 and line.startswith("("):
                matches = re.findall(r'\(([^,]+),([^)]+)\)', line)
                for match in matches:
                    x, y = map(float, match)
                    coordinate_x.append(x)
                    coordinate_y.append(y)
    
    if not coordinate_x or not coordinate_y:
        return 0, 0, 0, 0
    
    coords_array = np.array([coordinate_x, coordinate_y])
    x_min, y_min = np.min(coords_array, axis=1)
    x_max, y_max = np.max(coords_array, axis=1)
    
    return x_max, x_min, y_max, y_min
    
    
#print(calculate_canvas_size("small_case.txt", 1))
#print(calculate_marker_size("large_pattern.txt", 2))
