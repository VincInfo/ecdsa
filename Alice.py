import logging
import os
import signal
from MessageHandler import MessageHandler

if __name__ == "__main__":
    host_a = '127.0.0.1'
    port_a = 12345
    alice = MessageHandler('Alice', host_a, port_a)
    signal.signal(signal.SIGINT, alice.signal_handler)
    alice.accept()
    print('done2')

    