import os
import time
import sys

fim = "fim\n"

os.system("make run &")
time.sleep(200)
os.system("echo " + fim)