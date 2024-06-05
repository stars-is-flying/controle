import cv2
import numpy as np
import socket
from PIL import ImageGrab

def recvall(sock, count):
    """接收指定大小的数据"""
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf



def catch_screen_server():
    # 创建一个TCP套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8888))
    server_socket.listen(5)
    while True:
        client_socket, addr = server_socket.accept()
        while True:
            # 接收数据大小
            data_size = recvall(client_socket, 4)
            if not data_size:
                break
            data_size = int.from_bytes(data_size, byteorder='big')

            # 接收图像数据
            data = recvall(client_socket, data_size)
            if not data:
                break

            # 将字节流转换为图像
            frame = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            # 显示图像
            cv2.imshow('Screen', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        client_socket.close()

    cv2.destroyAllWindows()
    server_socket.close()


def screen_catch_client():
    # 设置服务器地址和端口
    SERVER_ADDRESS = ('172.24.127.176', 8888)

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