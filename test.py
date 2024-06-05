import cv2
import numpy as np
import socket
from PIL import ImageGrab

# 设置服务器地址和端口
SERVER_ADDRESS = ('172.23.114.97', 8888)

# 创建一个TCP套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(SERVER_ADDRESS)

while True:
    # 捕获屏幕
    screen = ImageGrab.grab()
    frame = np.array(screen)

    # 将图像转换为字节流
    _, buffer = cv2.imencode('.jpg', frame)
    data = buffer.tobytes()

    # 发送数据大小
    data_size = len(data)
    client_socket.sendall(data_size.to_bytes(4, byteorder='big'))

    # 发送图像数据
    client_socket.sendall(data)

    # 添加一些延迟以控制传输速率
    cv2.waitKey(30)

# 关闭套接字
client_socket.close()
