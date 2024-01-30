import select
import socket
import time
import logging


def handle_reads(reads, messages):
    for connection in reads:
        data = connection.recv(1024)
        PRETEND_TO_DO_WORK = 5
        time.sleep(PRETEND_TO_DO_WORK)
        string = data.decode('utf-8')
        message = f'Echo: {string}'
        messages[connection] = message


def handle_writes(writes, messages):
    for connection in writes:
        if connection not in messages:
            continue
        message = messages[connection]
        connection.send(message.encode('utf-8'))
        del messages[connection]


def serve():
    server = socket.socket()
    server.bind(('', 3333))
    server.listen(5)

    connections = []
    messages = {}
    while True:
        read, write, error = select.select(connections + [server], connections, connections)
        if server in read:
            connection, peer_address = server.accept()
            logging.info(f'connection from {peer_address}')
            connections.append(connection)
            read.remove(server)
        handle_reads(read, messages)
        handle_writes(write, messages)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    serve()
