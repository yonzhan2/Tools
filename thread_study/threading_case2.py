import threading
import requests
import time

link_list = []
with open('alexa.txt', 'r') as file:
    file_list = file.readlines()
    for eachone in file_list:
        link = eachone.split('\t')[1]
        link = link.replace('\n', '')
        link_list.append(link)
print(link_list)

start = time.time()


class MyThread(threading.Thread):
    def __init__(self, name, link_range):
        threading.Thread.__init__(self)
        self.name = name
        self.link_range = link_range

    def run(self):
        print("Starting " + self.name)
        crawler(self.name, self.link_range)
        print("Exiting " + self.name)


def crawler(threadName, link_range):
    for i in range(link_range[0], link_range[1] + 1):
        try:
            r = requests.get(link_list[i], timeout=20)
            print(threadName, r.status_code, link_list[i])
        except Exception as e:
            print(threadName, "Error", e)


thread_list = []
link_range_list = [(0, 200), (201, 400), (401, 600), (601, 800), (801, 1000)]

##create new thread
for i in range(1, 6):
    thread = MyThread("Thread-" + str(i), link_range_list[i - 1])
    thread.start()
    thread_list.append(thread_list)

##wait for all of threads finished
for thread in thread_list:
    thread.join()

end = time.time()
print("Time of Simple multi-threading: ", end - start)
print("Exiting Main Thread.")
