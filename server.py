import socket
import argparse
import select
import logging
import safe_connection
import json


def message_decoder(message, sender, usernames):
    decoded_message = json.loads(message)
    code = decoded_message["code"]
    if code == "hello":
        pass  # TODO
    elif code == "who":
        pass  # TODO
    elif code == "outgoing_broadcast":
        pass  # TODO
    elif code == "outgoing":
        pass  # TODO
    elif code == "quit":
        pass  # TODO
    else:
        pass  # TODO


def handle_reads(read_ready, messages: dict[safe_connection.SafeConnection, str]):
    for connection in read_ready:
        logging.info(f'Connection ready to read: {connection}')
        message = connection.recv(1024).decode()
        logging.info(f'Received message: {message} {len(message)}')

        messages[connection] = message


def handle_writes(write_ready, messages):
    for connection in write_ready:
        if connection not in messages:
            continue
        message = messages[connection]
        logging.info(f'Connection ready to write: {connection}: {message}')
        connection.send(f'Echo: {message}'.encode())
        del messages[connection]


def accept_connection(server, connections):
    connection, peer_address = server.accept()
    connection = safe_connection.SafeConnection(connection)
    logging.info(f'Connection from {peer_address}')
    connections.append(connection)


def serve(port):
    server = socket.socket()
    server.bind(('', port))
    server.listen(5)

    connections = []
    user_names = {}
    messages = {}

    while True:
        read_ready, write_ready, errors = select.select(connections + [server], connections, [])
        logging.info(f'Ready to read: {len(read_ready)} Ready to write: {len(write_ready)}')
        logging.info(f'errors: {len(errors)}')
        if server in read_ready:
            accept_connection(server, connections)
            read_ready.remove(server)

        handle_reads(read_ready, messages)
        handle_writes(write_ready, messages)
        connections = [connection for connection in connections if not connection.done()]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int)
    arguments = parser.parse_args()
    serve(arguments.port)
