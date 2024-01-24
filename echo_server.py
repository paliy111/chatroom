import socket
import time
import logging
import threading


def main():
    def _handle_client(connection):
        PRETEND_TO_DO_WORK = 5
        time.sleep(PRETEND_TO_DO_WORK)
        data = connection.recv(1024)
        string = data.decode('utf-8')
        answer = f'Echo: {string}'
        connection.send(answer.encode('utf-8'))
        connection.close()

    server = socket.socket()
    server.bind(('', 3333))
    server.listen(5)

    while True:
        connection, peer_address = server.accept()
        logging.info(f'Connection from {peer_address}')
        thread = threading.Thread(target=_handle_client, args=(connection,))
        thread.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    main()
