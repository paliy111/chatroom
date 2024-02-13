import logging
import socket
import argparse
import json

def main(host, port, nickname):
    sock = socket.socket()
    sock.connect((host, port))

    sock_hello_message = {"code": "hello", "name": nickname}
    json_sock_hello_message = json.dumps(sock_hello_message)
    sock.send(json_sock_hello_message.encode())
    response = sock.recv(1024)
    print(f'< {response.decode()}')

    while True:
        message = input('client> ')
        if message == 'quit':
            sock.close()
            return
        if message == 'who':
            sock_message_send = {"code": "who"}
        else:
            user, text_content = message.split('|', 1)
            if user == '*':
                sock_message_send = {"code": "outgoing_broadcast", "content": text_content}
            else:
                sock_message_send = {"code": "send_message", "to": user, "content": text_content}

        json_sock_message_send = json.dumps(sock_message_send)
        sock.send(json_sock_message_send.encode())
        response = sock.recv(1024)
        print(f'server> {response.decode()}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument('server_ip')
    parser.add_argument('server_port', type=int)
    parser.add_argument('my_nickname', type=str)
    #TODO check that the nickname is not *
    arguments = parser.parse_args()
    main(arguments.server_ip, arguments.server_port, arguments.my_nickname)
