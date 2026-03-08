import numpy as np
import matplotlib.pyplot as plt

# 采样率和信号参数
fs = 1000  # 采样频率，单位Hz
f = 5      # 信号频率，单位Hz
t = np.arange(0, 1, 1/fs)  # 1秒钟的时间序列

# 生成5Hz正弦波
y = np.sin(2 * np.pi * f * t)

# 绘图
plt.figure(figsize=(10, 4))
plt.plot(t, y)
plt.title("5Hz 正弦波")
plt.xlabel("时间 (秒)")
plt.ylabel("幅值")
plt.grid(True)
plt.xlim(0, 1)
plt.show()