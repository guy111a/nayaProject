
import os
import time

fileName='/tmp/bot_log_file.txt'
timeStamp=int(time.time())
if os.path.exists(fileName):
      os.system(f"tar cfz /tmp/bot_log_{timeStamp}.tar.gz /tmp/bot_log_file.txt")
      print("removing old log file ..")
      os.system("rm /tmp/bot_log_file.txt")
      print(f'creating new empty {fileName} ..')
      with open (fileName, 'a') as fd:
          fd.write('telegram bot -> corona4u application')

