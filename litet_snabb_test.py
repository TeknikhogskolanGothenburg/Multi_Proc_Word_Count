from queue import Queue


def main():
    q = Queue()
    for i in range(100):
        q.put(i)

    result = []
    while item := q.get():
        result.append(item)

    print(result)


if __name__ == '__main__':
    main()
