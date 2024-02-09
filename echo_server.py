import socket
import time
import logging

def serve():
    server = socket.socket()

    server.bind(('', 3333))
    server.listen(5)

    while True:
        connection, peer_address = server.accept()
        logging.info(f'Connection from {peer_address}')
        PRETEND_TO_DO_WORK = 5
        time.sleep(PRETEND_TO_DO_WORK)
        data = connection.recv(1024)
        string = data.decode('utf-8')
        answer = f'Echo: {string}'
        connection.send(answer.encode('utf-8'))
        connection.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    serve()
