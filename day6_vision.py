import cv2
import numpy as np
import time

# 打开电脑摄像头
cap = cv2.VideoCapture(0)

# 预先读取一次确定分辨率
ret, frame = cap.read()
if not ret:
    raise RuntimeError("无法打开摄像头")

frame_height, frame_width = frame.shape[:2]
center_x, center_y = frame_width // 2, frame_height // 2  # 画面中心点坐标

# 初始化FPS计算参数
fps = 0
frame_count = 0
fps_time = time.time()
fps_interval = 1  # 每多少秒刷新一次FPS

while True:
    t_start = time.time()
    ret, frame = cap.read()
    if not ret:
        break

    # BGR转HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 红色HSV阈值范围
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])

    # 二值化掩膜
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # ************** 工业级特性1：图像滤波 **************
    # 高斯模糊，去除随机噪声
    mask_blur = cv2.GaussianBlur(mask, (7, 7), 0)
    # 形态学处理：先开运算去小噪声点，再闭运算填补小孔洞
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask_open = cv2.morphologyEx(mask_blur, cv2.MORPH_OPEN, kernel, iterations=1)
    mask_clean = cv2.morphologyEx(mask_open, cv2.MORPH_CLOSE, kernel, iterations=1)

    # 寻找轮廓
    contours, _ = cv2.findContours(mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 变量初始化
    coord_text = "(N/A, N/A)"
    error_text = "error_x: N/A, error_y: N/A"

    # ************** 工业级特性2：控制系统接口 **************
    if contours:
        # 查找最大轮廓
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        # 绘制蓝色方框
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # 计算中心点
        cx = x + w // 2
        cy = y + h // 2
        # error_x, error_y = 目标中心点与画面中心点的差值
        error_x = cx - center_x
        error_y = cy - center_y

        # 显示中心点坐标及偏差
        coord_text = f"({cx}, {cy})"
        error_text = f"error_x: {error_x}, error_y: {error_y}"

        # 在目标中心点画十字
        cv2.drawMarker(frame, (cx, cy), (0, 0, 255), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)
    else:
        cx, cy, error_x, error_y = None, None, None, None  # 用于后续扩展

    # 显示中心点坐标（左上角，绿色）
    cv2.putText(frame, coord_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # 显示error_x, error_y（左上角下方，橙色）
    cv2.putText(frame, error_text, (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
    # 画面中心点用小十字表示（黄色）
    cv2.drawMarker(frame, (center_x, center_y), (0, 255, 255), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)

    # ************** 工业级特性3：性能监控 **************
    frame_count += 1
    now = time.time()
    if now - fps_time >= fps_interval:
        fps = frame_count / (now - fps_time)
        fps_time = now
        frame_count = 0
    # 在画面右上角显示FPS（白色，黑底叠加便于视觉分辨）
    fps_disp = f"FPS: {fps:.2f}"
    (tw, th), _ = cv2.getTextSize(fps_disp, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)
    cv2.rectangle(frame, (frame_width - tw - 20, 10), (frame_width - 10, 10 + th + 10), (0, 0, 0), -1)
    cv2.putText(frame, fps_disp, (frame_width - tw - 15, 10 + th + 2), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    # 显示画面
    cv2.imshow('Red Object Tracking', frame)
    # # 若需要也观察滤波效果，可同时展示mask画面：
    # cv2.imshow('Mask (After Filtering)', mask_clean)

    # 按q键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()