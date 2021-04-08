from multiprocessing import Pool

def func(value):
    print(f'Working with value {value}')
    return value**2

def main():
    values = [5, 4, 3, 2, 1]

    with Pool() as pool:
        result = pool.imap(func, values)
        for value in result:
            print(value)


if __name__ == '__main__':
    main()
