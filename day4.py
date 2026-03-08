# 定义一个计算PID控制输出的函数
def calculate_PID(error, Kp, Ki, Kd):
    """
    简化版PID控制器计算函数

    参数:
        error: 当前误差值
        Kp: 比例系数
        Ki: 积分系数
        Kd: 微分系数
    返回:
        output: PID控制输出值
    """
    # 这里使用一个简化的PID公式进行计算
    output = Kp * error + Ki * error * 0.1 + Kd * error * 0.01
    return output

# ------------------- 下面测试两种状态 ---------------------

# 1. 大误差启动状态（假设误差较大，系数也较大）
big_error = 15.0     # 假设初始误差为15
Kp1 = 2.0
Ki1 = 0.5
Kd1 = 0.1
output1 = calculate_PID(big_error, Kp1, Ki1, Kd1)
print(f"大误差启动状态的PID控制输出: {output1:.2f}")

# 2. 接近目标状态（误差较小，系数也较小）
small_error = 0.8    # 假设误差仅为0.8
Kp2 = 1.0
Ki2 = 0.2
Kd2 = 0.05
output2 = calculate_PID(small_error, Kp2, Ki2, Kd2)
print(f"接近目标状态的PID控制输出: {output2:.2f}")
