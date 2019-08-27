import threading
import time


class MyThread(threading.Thread):
    def __init__(self, name, delay):
        threading.Thread.__init__(self)
        self.name = name
        self.delay = delay

    def run(self):
        print("Starting " + self.name)
        print_time(self.name, self.delay)
        print("Exiting " + self.name)


def print_time(threadName, delay):
    count = 0
    while count < 3:
        time.sleep(delay)
        print(threadName, time.ctime())
        count += 1


threads = []

##create new thread
thread1 = MyThread("Thread-1", 1)
thread2 = MyThread("Thread-2", 2)

##start new thread
thread1.start()
thread2.start()

##add thread to threads list
threads.append(thread1)
threads.append(thread2)

##wait for all the threads finished
for t in threads:
    t.join()
print("Exiting Main Thread.")
