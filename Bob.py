import signal
from MessageHandler import MessageHandler

if __name__ == "__main__":
    host_b = '127.0.0.1'
    Bob = MessageHandler('Bob', host_b)
    signal.signal(signal.SIGINT, Bob.signal_handler)
    Bob.connect(host_b, 12345)

