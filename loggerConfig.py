import os
import time
import logging
import logging.handlers
import queue

def delete_logfile(logfile):
    if os.path.exists(logfile):
        os.remove(logfile)

logfile = 'logfile.log'
        
log_queue = queue.Queue()

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(logfile)
formatter = logging.Formatter('%(asctime)s - [%(threadName)-20s] - %(levelname)s: %(message)s')
file_handler.setFormatter(formatter)

root_logger.addHandler(file_handler)

queue_handler = logging.handlers.QueueHandler(log_queue)
queue_listener = logging.handlers.QueueListener(log_queue, file_handler)


def start_listener():
    queue_listener.start()
    logger = get_logger()
    logger.info('logger started')

def stop_listener():
    logger = get_logger()
    logger.info('logger stopped')
    queue_listener.stop()

def get_logger():
    return root_logger

# if __name__ == "__main__":
#     with open("logfile.log", 'r') as file:
#         file.seek(0, 2)
#         while True:
#             line = file.readline()
#             if not line:
#                 time.sleep(0.1)
#                 continue
#             print(line.strip())