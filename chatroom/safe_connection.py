import logging
import socket


class SafeConnection:
    def __init__(self, connection):
        self._connection: socket.socket = connection
        self._done = False

    def fileno(self):
        return self._connection.fileno()

    def _safe_call(self, function, default, *args):
        try:
            return function(*args)
        except (BrokenPipeError, socket.error) as e:
            logging.error(f'Connection closed: {e}')
            self._done = True
            logging.info(f'done with {self}')
            return default

    def recv(self, size):
        return self._safe_call(self._connection.recv, b'', size)

    def send(self, data):
        return self._safe_call(self._connection.send, 0, data)

    def close(self):
        self._done = True
        self._connection.close()

    def done(self):
        return self._done
