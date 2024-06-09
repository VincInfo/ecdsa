import logging
from logging.handlers import QueueHandler, QueueListener
import os
import loggerConfig

if __name__ == "__main__":
    loggerConfig.queue_listener.start()
    logger = loggerConfig.get_logger()
    logger.info('Starting child processes')
    os.system("start powershell python.exe Alice.py")
    os.system("start powershell python.exe Bob.py")
    os.system("start powershell Get-Content -Path logfile.log -Wait")
    loggerConfig.queue_listener.stop()



