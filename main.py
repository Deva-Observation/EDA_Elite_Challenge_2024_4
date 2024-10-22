import read_pattern
import numpy as np
import plot_polygons
import multiprocess_test
from multiprocessing import freeze_support
import time

# 读取多边形数据
#_, _, coords_source = read_pattern.read_pattern_polygon("small_pattern.txt", "pattern1", "pattern2", "layer4", "layer5")
#_, coords_target = read_pattern.read_case_polygon("small_case.txt", "layer1", "layer2")

# 比较多边形
#pattern_match.compare_polygons(coords_source, coords_target)
#plot_polygons.plot_polygons(coords_source)
#plot_polygons.plot_polygons(coords_target)
def main():
    _, _, coords = read_pattern.read_pattern_polygon("./data/small_pattern.txt", "pattern1", "pattern2", "layer1", "layer2")
    _, coords_case = read_pattern.read_case_polygon("./data/small_case.txt", "layer1", "layer2")
    polygons = [np.array(coord) for coord in coords]
    polygons_case = [np.array(coord) for coord in coords_case]
    #multiprocess_test.pattern_encoder("./data/small_pattern.txt", 1, "./data/small_case.txt", 1, polygons_case)
    multiprocess_test.pattern_encoder("./data/small_pattern.txt", 1, "./data/temp", 1, polygons)


if __name__ == '__main__':
    freeze_support()  
    start_time = time.process_time()
    main()  # 调用主程序函数
    end_time = time.process_time()
    print("程序运行时间：", end_time - start_time)