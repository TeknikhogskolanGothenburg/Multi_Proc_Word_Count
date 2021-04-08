import time
from prime import create_lists, is_prime
from multiprocessing import Pool, cpu_count

def worker(sequence):
    return [n for n in sequence if is_prime(n)]


def main():
    work_lists = create_lists(range(2, 5_000_000), 10_000)

    print(f'Finding all primes below 5,000,000 using {cpu_count()} core(s)')
    start = time.time()

    with Pool() as pool:
        result = pool.map(worker, work_lists)
    primes = [value for a_list in result for value in a_list]
    primes.sort()
    end = time.time()
    print(f'It took {round(end-start, 2)} second(s). Found {len(primes)} primes.')
    # It took 11.49 second(s). Found 348513 primes.

if __name__ == '__main__':
    main()
