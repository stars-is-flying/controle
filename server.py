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
            print(files[i], end='  ')
        else:
            print(colored(files[i], "blue"), end='  ')
    print()
    

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
            work_dir = res["pwd"]












