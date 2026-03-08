import cv2
import numpy as np

# 打开电脑摄像头
cap = cv2.VideoCapture(0)

while True:
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

    # 寻找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # 查找最大轮廓
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        # 绘制蓝色方框
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # 计算中心点
        cx = x + w // 2
        cy = y + h // 2
        # 显示中心点坐标
        coord_text = f"({cx}, {cy})"
        cv2.putText(frame, coord_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "(N/A, N/A)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # 显示画面
    cv2.imshow('Red Object Tracking', frame)

    # 按q键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()