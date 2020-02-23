from __future__ import print_function
import os
import shutil
import threading
import datetime

try:
    import queue as Queue
except Exception as e:
    import Queue

current_year = str(datetime.date.today().year)
current_month = str(format(datetime.date.today().month, '0>2d'))
base_dir = [os.path.join('/export/primary', current_year, current_month),
            os.path.join('/export/second', current_year, current_month)]
remove_dirs = []
for entry in base_dir:
    remove_dirs.extend(
        [os.path.join(entry, item) for item in os.listdir(entry) if len(item) <= 12])
print(remove_dirs)


def remove_dir(thread_name, q):
    while not q.empty():
        dir_name = q.get()
        print("%s remove dir %s" % (thread_name, dir_name))
        shutil.rmtree(dir_name)


threadList = []
for i in range(20):
    threadList.append("Thread-%s" % str(i))

workQueue = Queue.Queue()
threads = []

##fill up with queue
for url in remove_dirs:
    workQueue.put(url)

##create new thread
for tName in threadList:
    thread = threading.Thread(target=remove_dir, args=(tName, workQueue,))
    thread.start()
    threads.append(thread)

##wait for all of threads finished
for t in threads:
    t.join()

print("Exiting Main Thread.")
