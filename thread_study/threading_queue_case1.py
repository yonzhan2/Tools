import threading
import requests
import time
import queue as Queue
from pprint import pprint

link_list = []
with open('alexa.txt', 'r') as file:
    file_list = file.readlines()
    for eachone in file_list:
        link = eachone.split('\t')[1]
        link = link.replace('\n', '')
        link_list.append(link)

start = time.time()


class MyThread(threading.Thread):
    def __init__(self, name, q):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q

    def run(self):
        print("Starting " + self.name)
        while True:
            try:
                # print("Debug", self.name, self.q)
                crawler(self.name, self.q)
            except Exception as e:
                print("Error is ", e)
                break
        print("Exiting " + self.name)


def crawler(threadName, q):
    url = q.get(timeout=2)
    try:
        r = requests.get(url, timeout=20)
        print(q.qsize(), threadName, r.status_code, url)
    except Exception as e:
        print(q.qsize(), threadName, "Error", e)


threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5", ]
workQueue = Queue.Queue(1000)
threads = []

##create new thread
for tName in threadList:
    thread = MyThread(tName, workQueue)
    thread.start()
    threads.append(thread)

##fill up with queue
for url in link_list:
    workQueue.put(url)

##wait for all of threads finished
for t in threads:
    t.join()

end = time.time()
print("Time of Queue-threading: ", end - start)
print("Exiting Main Thread.")
