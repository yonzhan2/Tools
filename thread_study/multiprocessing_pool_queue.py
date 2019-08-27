from multiprocessing import Pool, Manager, cpu_count
import time
import requests

link_list = []
with open('alexa.txt', 'r') as file:
    file_list = file.readlines()
    for eachone in file_list:
        link = eachone.split('\t')[1]
        link = link.replace('\n', '')
        link_list.append(link)

start = time.time()


def crawler(q, index):
    process_id = "Process-" + str(index)
    while not q.empty():
        url = q.get(timeout=2)
        try:
            r = requests.get(url, timeout=20)
            print(process_id, q.qsize(), r.status_code, url)
        except Exception as e:
            print(process_id, q.qsize(), url, "Error", e)


if __name__ == '__main__':
    manager = Manager()
    workQueue = manager.Queue(1000)

    ##fill up with queue
    for url in link_list:
        workQueue.put(url)

    pool = Pool(cpu_count() - 1)
    for i in range(cpu_count() - 1):
        ###async
        pool.apply_async(crawler, args=(workQueue, i))
        ##sync
        # pool.apply(crawler, args=(workQueue, i))
    print("Started processes")
    pool.close()
    pool.join()
    end = time.time()
    print("The time of Pool + Queue is ", end - start)
    print("Main Process Ended!")

    end = time.time()
    print("Time of Process Queue is ", end - start)
    print("Main process Ended!")
