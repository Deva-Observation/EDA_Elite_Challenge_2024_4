import re

def read_pattern_polygon(file_path, pattern_start, pattern_end, layer_start, layer_end):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        pattern_name = ""
        layer_name = ""
        read_pattern = 0
        read_layer = 0
        coordinates = []

        for line in lines:
            if line.startswith(pattern_start):
                pattern_name = line.split(":")[0].strip()
                read_pattern = 1
            elif line.startswith(pattern_end):
                read_pattern = 0
            elif line.startswith(layer_start):
                layer_name = line.split(":")[0].strip()
                read_layer = 1
            elif line.startswith(layer_end):
                read_layer = 0
            elif line.startswith("(") and read_pattern == 1 and read_layer == 1:
                matches = re.findall(r'\(([^,]+),([^)]+)\)', line)
                coordinate = []
                for match in matches:
                    x, y = map(float, match)
                    coordinate.append([x,y])

                coordinates.append(coordinate)
    return pattern_name, layer_name, coordinates

#pattern_name, layer_name, coords = read_polygon("test", "pattern1", "pattern2", "layer2", "layer3")
#print(coords)
def read_case_polygon(file_path, layer_start, layer_end):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        layer_name = ""
        read_layer = 0
        coordinates = []

        for line in lines:
            if line.startswith(layer_start):
                layer_name = line.split(":")[0].strip()
                read_layer = 1
            elif line.startswith(layer_end):
                read_layer = 0
            elif line.startswith("(") and read_layer == 1:
                matches = re.findall(r'\(([^,]+),([^)]+)\)', line)
                coordinate = []
                for match in matches:
                    x, y = map(float, match)
                    coordinate.append([x,y])

                coordinates.append(coordinate)
    return layer_name, coordinates