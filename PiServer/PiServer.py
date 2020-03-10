import socket
import get_sock_name

def pi_server():
    # get the hostname
    localaddr = get_sock_name.get_sock_name()
    print("local address resolved to: " + localaddr)
    host = socket.gethostbyname(localaddr)
    port = 5000  # port #

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind
    server_socket.listen(2)          # handles 2 connections
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data. 2048 byte max
        data = conn.recv(2048).decode()
        if not data:
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  # send to client

    conn.close()  # close connection


if __name__ == '__main__':
    pi_server()
