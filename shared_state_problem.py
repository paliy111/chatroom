import argparse
import logging
import threading
import time

counter = 0

def incrementer():
    global counter
    for _ in range(1000):
        old = counter
        time.sleep(0.0001)
        counter = old + 1

def go(thread_count: int):
    global counter
    logging.info(f'Counter: {counter}')
    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=incrementer, daemon=True)
        threads.append(thread)

    for thread in threads:
        logging.info(f'launch thread: {thread}')
        thread.start()

    for thread in threads:
        thread.join()

    logging.info(f'Counter: {counter}')


parser = argparse.ArgumentParser()
parser.add_argument('--thread-count', type=int, default=1)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
arguments = parser.parse_args()
go(arguments.thread_count)
