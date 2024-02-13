import logging
import socket
import argparse

def main(host, port, nickname):
    sock = socket.socket()
    sock.connect((host, port))

    sock_hello_message = {"code": "hello", "nickname": nickname}
    sock.send(sock_hello_message.encode())
    response = sock.recv(1024)
    print(f'< {response.decode()}')

    while True:
        message = input('> ')
        if message == 'quit':
            sock.close()
            return
        if message == 'who':
            sock_message_send = {"code": "who"}
        else: #TODO we need to check if the user name is illegal, and if not spam every user with the message
            user, text_content = message.split('|', 1)
            sock_message_send = {"code": "send_message", "to": user, "content": text_content}

        sock.send(sock_message_send.encode())
        response = sock.recv(1024)
        print(f'< {response.decode()}')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument('server_ip')
    parser.add_argument('server_port', type=int)
    parser.add_argument('my_nickname', type=str)

    arguments = parser.parse_args()
    main(arguments.server_ip, arguments.server_port, arguments.my_nickname)
