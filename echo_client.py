import logging
import socket
import argparse

def main(host, port):
    sock = socket.socket()
    sock.connect((host, port))
    while True:
        message = input('> ')
        if message == 'quit':
            sock.close()
            return
        sock.send(message.encode())
        response = sock.recv(1024)
        print(f'< {response.decode()}')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument('host')
    parser.add_argument('port', type=int)
    arguments = parser.parse_args()
    main(arguments.host, arguments.port)
