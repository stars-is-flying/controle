import pickle
import struct
import socket

def pack_number(num) -> bytes:
    return struct.pack('i', num)

def unpack_number(data: bytes):
    return struct.unpack('i', data)[0]

def recv_data(client: socket.socket) -> dict:
    data = client.recv(4, socket.MSG_WAITALL)
    data_length = unpack_number(data)

    return pickle.loads(client.recv(data_length, socket.MSG_WAITALL))

def send_data(client: socket.socket, data: dict):
    byte_data = pickle.dumps(data)
    data_length = len(byte_data)
    client.send(pack_number(data_length), 0)
    client.send(byte_data, 0)