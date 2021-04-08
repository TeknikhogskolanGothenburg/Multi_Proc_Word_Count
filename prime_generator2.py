import time

from prime import create_lists, is_prime
from queue import Queue
import threading


def main():
    work_lists = create_lists(range(2, 5_000_000), 10_000)
    q = Queue()
    primes = []
    lock = threading.Lock()

    for l in work_lists:
        q.put(l)

    def worker():
        while True:
            list_to_work_on = q.get()
            for n in list_to_work_on:
                if is_prime(n):
                    with lock:
                        primes.append(n)
            q.task_done()

    start = time.time()
    for _ in range(6):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
    q.join()
    primes.sort()
    end = time.time()
    print(f'It took {round(end-start, 2)} second(s). Found {len(primes)} primes.')
    # It took 78.79 second(s). Found 348513 primes.

if __name__ == '__main__':
    main()
