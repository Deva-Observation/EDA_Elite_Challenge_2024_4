import size_calculation
import numpy as np
import os
from point_in_polygon import point_in_polygon_vectorized

def pattern_encoder(pattern_file_path, pattern_index,case_file_path, layer_index, polygons):
    os.makedirs('./result', exist_ok=True)
    x_max, x_min, y_max, y_min = size_calculation.calculate_marker_size(pattern_file_path, pattern_index)
    canvas_x_max, canvas_x_min, canvas_y_max, canvas_y_min = size_calculation.calculate_canvas_size(case_file_path, layer_index)
    grid = 600
    
    x_min, x_max = int(x_min), int(x_max)
    y_min, y_max = int(y_min), int(y_max)

    x_max = x_max - x_min
    y_max = y_max - y_min
    x_min = 0
    y_min = 0

    canvas_x_min, canvas_x_max = int(canvas_x_min), int(canvas_x_max)
    canvas_y_min, canvas_y_max = int(canvas_y_min), int(canvas_y_max)

    for x_window_min in range(canvas_x_min, canvas_x_max - x_max + 1, grid):
        x_window_max = x_window_min + x_max
        for y_window_min in range(canvas_y_min, canvas_y_max - y_max + 1, grid):
            y_window_max = y_window_min + y_max

            x_range = np.arange(x_window_min + 1, x_window_max, grid)
            y_range = np.arange(y_window_min, y_window_max, grid)
            
            X, Y = np.meshgrid(x_range, y_range)
            points = np.column_stack((X.ravel(), Y.ravel()))
            point_status = point_in_polygon_vectorized(points, polygons)
            point_status = point_status.reshape(len(y_range), len(x_range)).T

            np.savetxt(f'./result/layout_{x_window_min}_{x_window_max}_{y_window_min}_{y_window_max}.txt', point_status, fmt='%d', delimiter=',')
            # 编码模式
            pattern_encode = []
            for row in point_status:
                code = 1
                if row[0] == 1:
                    code = code * 2 + 1
                else:
                    code = code * 2
                row = row.astype(int)
                diff_row = np.diff(row).astype(int)
                for i in range(len(diff_row)):
                    if diff_row[i] != 0 and i != 0:
                        code = code * 2 + (diff_row[i] + 1)//2
                pattern_encode.append(code)
            
            np.savetxt(f'./result/encode_result_{x_window_min}_{x_window_max}_{y_window_min}_{y_window_max}.txt', pattern_encode, fmt='%d', delimiter=',')
            
            print(x_window_min, x_window_max, y_window_min, y_window_max)
            y_window_min = y_window_min + grid
            y_window_max = y_window_max + grid

        x_window_min = x_window_min + grid
        x_window_max = x_window_max + grid

    return 0
