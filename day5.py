import numpy as np
import matplotlib.pyplot as plt

# 生成1秒采样，采样率1000Hz
fs = 1000  # 采样率 (Hz)
f = 10     # 基础信号频率 (Hz)
t = np.arange(0, 1, 1/fs)  # 时间序列

# 生成10Hz的纯净正弦波
y_pure = np.sin(2 * np.pi * f * t)

# 生成高斯白噪声
np.random.seed(42)  # 固定随机种子便于复现
noise = np.random.normal(0, 0.4, t.shape)

# 得到实际传感器读数（噪声叠加）
y_noisy = y_pure + noise

# 绘图
plt.figure(figsize=(10, 4))
plt.plot(t, y_pure, color='green', linewidth=2.5, label='纯净波形')
plt.plot(t, y_noisy, color='red', linewidth=1.2, alpha=0.6, label='传感器噪声波形')
plt.title("模拟传感器噪声叠加效果对比", fontproperties="SimHei", fontsize=15)
plt.xlabel("时间（秒）", fontproperties="SimHei")
plt.ylabel("信号幅值", fontproperties="SimHei")
plt.legend(prop={'family': 'SimHei', 'size': 12})
plt.grid(True)
plt.tight_layout()
plt.show()