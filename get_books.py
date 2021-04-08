import requests
import threading
from queue import Queue

def get_ids():
    id = None
    lang = None
    ids = []
    for line in open('ignored/catalog.rdf', encoding='utf8'):
        if 'rdf:ID="etext' in line:
            id = line.split('"')[1].replace('etext', '')
        if 'dc:language' in line:
            if not 'rdf:value>' in line:
                continue
            lang = line.split('rdf:value>')[1].replace('</', '')
        if id and lang == 'en':
            ids.append(id)
            id = None
            lang = None
    return ids

def main():
    ids = get_ids()
    base_url = 'https://www.gutenberg.org/files'
    q = Queue()
    for id in ids:
        q.put(id)

    def worker():
        while True:
            id = q.get()
            result = requests.get(f'{base_url}/{id}/{id}-0.txt')
            if result.ok:
                print(result.encoding)
                # with open(f'./books/{id}.txt', 'w', encoding=result.encoding) as outfile:
                #     outfile.write(result.text)
                print(f'Downloaded {id}.txt')
            q.task_done()

    for _ in range(20):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
    q.join()

if __name__ == '__main__':
    main()
