import socket
import time
import argparse
import select
import logging

def handle_reads(read_ready, messages):
    for connection in read_ready:
        logging.info(f'Connection ready to read: {connection}')
        message = connection.recv(1024).decode()
        logging.info(f'Received message: {message}')
        messages[connection] = message

def handle_writes(write_ready, messages):
    for connection in write_ready:
        if connection not in messages:
            continue
        message = messages[connection]
        logging.info(f'Connection ready to write: {connection}: {message}')
        connection.send(f'Echo: {message}'.encode())
        del messages[connection]

def serve(port):
    server = socket.socket()

    server.bind(('', port))
    server.listen(5)

    connections = []
    messages = {}

    while True:
        read_ready, write_ready, _ = select.select(connections + [server], connections, [])
        logging.info(f'Ready to read: {len(read_ready)} Ready to write: {len(write_ready)}')
        if server in read_ready:
            connection, peer_address = server.accept()
            logging.info(f'Connection from {peer_address}')
            connections.append(connection)
            read_ready.remove(server)

        handle_reads(read_ready, messages)
        handle_writes(write_ready, messages)
        time.sleep(0.1)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int)
    arguments = parser.parse_args()
    serve(arguments.port)
