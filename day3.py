import random  # 导入 random 模块用于生成随机数

# 用列表生成式，生成 5 个 0.5 到 5.0 之间的随机小数，代表五个方向的传感器检测距离（单位：米）
sensor_distances = [round(random.uniform(0.5, 5.0), 2) for _ in range(5)]

# 找出五个传感器距离中的最小值，即距离最近的障碍物，也是最危险的障碍物距离
min_distance = min(sensor_distances)

# 打印传感器当前读取到的所有距离
print(f"当前各传感器距离矩阵为：{sensor_distances}")

# 打印最危险（距离最近）目标并标记为最高优先级
print(f"前方最危险距离为：{min_distance} 米，已标记为最高优先级避障目标！")