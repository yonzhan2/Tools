from multiprocessing import Process, Queue, cpu_count
import time
import requests

"""
    def qsize(self):
        # Raises NotImplementedError on Mac OSX because of broken sem_getvalue()
        return self._maxsize - self._sem._semlock._get_value()
        
    Process + Queue is suitable for operation items is small. porcesses <100.    
"""

link_list = []
with open('alexa.txt', 'r') as file:
    file_list = file.readlines()
    for eachone in file_list:
        link = eachone.split('\t')[1]
        link = link.replace('\n', '')
        link_list.append(link)

start = time.time()


class MyProcess(Process):
    def __init__(self, q):
        Process.__init__(self)
        self.q = q

    def run(self) -> None:
        print("Starting", self.pid)
        while not self.q.empty():
            crawler(self.q)
        print("Exiting ", self.pid)


def crawler(q):
    url = q.get(timeout=2)
    try:
        r = requests.get(url, timeout=20)
        print(q.qsize(), r.status_code, url)
    except Exception as e:
        print(q.qsize(), url, "Error", e)


if __name__ == '__main__':
    ProcessNames = ["Process-1", "Process-2", "Process-3"]
    workQueue = Queue(1000)

    print(cpu_count())

    ##fill up with queue
    for url in link_list:
        workQueue.put(url)

    for i in range(0, 3):
        p = MyProcess(workQueue)
        p.daemon = True
        p.start()
        p.join()

    end = time.time()
    print("Time of Process Queue is ", end - start)
    print("Main process Ended!")
