import numpy as np

def read_array_from_file(file_path):
    """
    从文本文件中读取数组
    """
    try:
        # 读取文件
        arr = np.loadtxt(file_path)
        
    except Exception as e:
        print(f"读取文件时发生错误: {str(e)}")
        return None

def compare_array(pattern_path, target_path):
    """
    从文件读取数组并进行比较
    """
    # 读取数组
    arr_pattern = read_array_from_file(pattern_path)
    arr_target = read_array_from_file(target_path)

    if arr_pattern is None or arr_target is None:
        return False
    
    # 比较输入数组与目标模式
    return np.array_equal(arr_pattern[0], arr_target[0])

# 测试函数
if __name__ == "__main__":
    target_path = 'result/encode_result_0_10200_0_13800.txt'
    pattern_path = 'encode_result.txt'

    result = compare_array(pattern_path, target_path)
    print(f"比较结果: {result}")