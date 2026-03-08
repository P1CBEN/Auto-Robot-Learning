distance = 10  # 初始距离（米）
step = 1.5     # 每次前进的距离（米）

while True:
    if distance > 3:
        print(f"安全前进，当前距离：{distance:.2f} 米")
    elif 0 < distance <= 3:
        print("红色预警：减速")
    else:
        print("触发紧急制动")
        break
    distance -= step