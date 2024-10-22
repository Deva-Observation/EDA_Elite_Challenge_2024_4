import matplotlib.pyplot as plt
import numpy as np

def plot_polygons(coords):
    """根据顶点坐标绘制多边形"""
    
    for polygon in coords:
        # 将多边形的坐标分离为x和y列表
        x, y = zip(*polygon)
        
        # 绘制多边形
        plt.plot(x + (x[0],), y + (y[0],), color='black')  # 添加第一个点以闭合多边形
    
    plt.axis('equal')  # 保持横纵比例一致
    plt.title('Polygon')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.xticks(np.arange(-200000, 200000, 600))
    plt.yticks(np.arange(-200000, 200000, 600))
    plt.grid(True)
    plt.show()
