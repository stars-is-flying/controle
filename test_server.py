from pwn import *

def handle_client(client):
    while True:
        command = input("Shell> ")
        if command.strip() == "exit":
            client.sendline(command)
            break
        client.sendline(command)
        response = client.recv()
        print(response.decode())

def main():
    host = "0.0.0.0"
    port = 4444

    server = listen(port)
    print(f"Listening on {host}:{port}...")

    client = server.wait_for_connection()
    print(f"Connection received from {client.sock.getpeername()}")

    handle_client(client)
    client.close()
    server.close()

if __name__ == "__main__":
    main()
