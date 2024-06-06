import logging
from logging.handlers import QueueHandler, QueueListener
import os
import queue
import subprocess
import time
import loggerConfig

if __name__ == "__main__":
    loggerConfig.queue_listener.start()
    logger = loggerConfig.get_logger()
    logger.info('Starting child processes')
    os.system("start powershell python.exe Alice.py")
    os.system("start powershell python.exe Bob.py")
    os.system("start powershell Get-Content -Path logfile.log -Wait")
    # proc = subprocess.Popen(['powershell', '-NoExit', '-Command', 'Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "Get-Content -Path logfile.log -Wait"'],
    #                     stdout=subprocess.PIPE,
    #                     stderr=subprocess.PIPE,
    #                     stdin=subprocess.PIPE)

    loggerConfig.queue_listener.stop()



