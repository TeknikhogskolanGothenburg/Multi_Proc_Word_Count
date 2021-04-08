from prime import is_prime
import time


def main():
    start = time.time()
    primes = [i for i in range(2, 5_000_000) if is_prime(i)]
    end = time.time()
    print(f'It took {round(end-start, 2)} second(s). Found {len(primes)} primes.')
    # It took 74.18 second(s). Found 348513 primes.

if __name__ == '__main__':
    main()
