import size_calculation
import numpy as np
import os
from multiprocessing import Pool, cpu_count
from functools import partial
from point_in_polygon import point_in_polygon_vectorized

'''
对单行进行编码
'''
def encode_row(row):
    code = 1#编码模式以1开头
    if row[0] != 0:
        code = code * 2 + 1
    else:
        code = code * 2
    diff_row = np.diff(row.astype(int))
    print(diff_row)
    for i in range(1, len(diff_row)):
        if diff_row[i] != 0:
            code = code * 2 + (diff_row[i] + 1)//2
    return code

def process_window_row(y_window_min, x_max, y_max, grid, canvas_x_max, polygons, canvas_x_min):
    results = []
    previous_encode = None
    for x_window_min in range(canvas_x_min, canvas_x_max - x_max + 1, grid):
        x_window_max = x_window_min + x_max
        y_window_max = y_window_min + y_max

        x_range = np.arange(x_window_min + 1, x_window_max, grid)
        y_range = np.arange(y_window_min, y_window_max, grid)
        
        X, Y = np.meshgrid(x_range, y_range)
        points = np.column_stack((X.ravel(), Y.ravel()))
        point_status = point_in_polygon_vectorized(points, polygons)
        point_status = point_status.reshape(len(y_range), len(x_range)).T
        np.savetxt(f'./result/point_status_{x_window_min}_{x_window_max}_{y_window_min}_{y_window_max}.txt', point_status, fmt='%d', delimiter=',')

        if previous_encode is None:
            pattern_encode = np.array([encode_row(row) for row in point_status])
        else:
            new_rows = point_status[:, -1]
            pattern_encode = np.concatenate([previous_encode[1:], [encode_row(new_rows)]])

        encode_filename = f'./result/encode_result_{x_window_min}_{x_window_max}_{y_window_min}_{y_window_max}.txt'
        np.savetxt(encode_filename, pattern_encode, fmt='%d', delimiter=',')
        
        print(f"处理完成: {x_window_min}, {x_window_max}, {y_window_min}, {y_window_max}")
        
        results.append(pattern_encode)
        previous_encode = pattern_encode

    return results

def pattern_encoder(pattern_file_path, pattern_index, case_file_path, layer_index, polygons):
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

    # 创建参数列表
    y_params = range(canvas_y_min, canvas_y_max - y_max + 1, grid)

    # 使用进程池并行处理每一行
    with Pool(processes=cpu_count()) as pool:
        process_func = partial(process_window_row, x_max=x_max, y_max=y_max, grid=grid, 
                               canvas_x_max=canvas_x_max, 
                               polygons=polygons, canvas_x_min=canvas_x_min)
        results = pool.map(process_func, y_params)

    print(results)

    return 0
