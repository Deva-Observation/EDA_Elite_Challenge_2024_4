import numpy as np

def point_in_polygon(x, y, polygon):
    polygon = np.array(polygon)
    n = len(polygon)
    inside = False
    
    # 将多边形的最后一个点添加到开头，以简化循环
    extended_polygon = np.vstack((polygon, polygon[0]))
    
    for i in range(n):
        p1, p2 = extended_polygon[i:i+2]
        
        if ((p1[1] > y) != (p2[1] > y)) and (x < (p2[0] - p1[0]) * (y - p1[1]) / (p2[1] - p1[1]) + p1[0]):
            inside = not inside
    
    return inside

def point_in_polygon_vectorized(points, polygons):
    x, y = points[:, 0], points[:, 1]
    inside = np.zeros(len(x), dtype=bool)
    
    for polygon in polygons:
        polygon = np.array(polygon)
        n = len(polygon)
        polygon_inside = np.zeros(len(x), dtype=bool)
        
        for i in range(n):
            j = (i + 1) % n
            xi, yi = polygon[i]
            xj, yj = polygon[j]
              
                
            # 处理水平边的情况
            if np.isclose(yi, yj):
                mask = (y >= min(yi, yj)) & (y <= max(yi, yj)) & (x <= max(xi, xj)) & (x >= min(xi, xj))
                polygon_inside ^= mask
                continue
                
            # 非水平边的情况
            mask = (y > min(yi, yj)) & (y <= max(yi, yj))
            x_intersect = (xj - xi) * (y - yi) / (yj - yi) + xi
            final_mask = mask & (x <= x_intersect)
            polygon_inside ^= final_mask
            
        inside |= polygon_inside
    
    return inside
