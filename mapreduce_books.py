import os
import time
from multiprocessing import Pool
import re
import pickle

def mapper(filename):
    print(f'Mapping {filename}')
    word_map = []
    for line in open(f'./books_to_process/{filename}', encoding='ISO-8859-1'):
        line = line.lower()
        words = [word for word in re.split("[^a-z']+", line) if word]
        for word in words:
            word_map.append(f'({word},1)')
    return word_map


def reducer(mapped_words):
    last_word = None
    word_count = 0
    counted_words = []
    for line in mapped_words:
        line = line[1:-1]
        word, count = line.split(',')
        try:
            count = int(count)
        except:
            print()

        if word == last_word:
            word_count += count
        else:
            if last_word:
                counted_words.append(f'{last_word} - {word_count}')
            last_word = word
            word_count = count

    counted_words.append(f'{last_word} - {word_count}')
    return counted_words

def prepare_mapped_words(mapped_words):
    split_pos = 100_000
    pos = 0
    num_words = len(mapped_words)
    prepared_words = []

    while True:
        current_pos = pos + split_pos
        if current_pos + 1 > num_words:
            yield mapped_words[pos:]
            break
        #chunk = mapped_words[pos:current_pos]
        last_word = mapped_words[current_pos]
        word = mapped_words[current_pos + 1]
        while word == last_word:
            current_pos += 1
            last_word = mapped_words[current_pos]
            word = mapped_words[current_pos + 1]
        yield mapped_words[pos:current_pos]
        pos = current_pos + 1



def main():
    start = time.time()
    # Hämta alla filnamn från books_to_process
    filenames = [filename for filename in os.listdir('./books_to_process')]

    # Skapa en multiproc pool och mappa till listan med filnamn och mapper

    with Pool() as pool:
        result = pool.imap(mapper, filenames)
        print('Mapping done')


        # Resultatet kommer vara en lista med listor. Varje lista kommer att vara mapper-resultatet
        # från en bok
        print('Processing result')
        # Platta till resultatlistan
        mapped_words = [mapped_word for mapped_list in result for mapped_word in mapped_list]
        # Sortera resultatlistan
        print(f'Sorting {len(mapped_words)} words') # Sorting 96 704 482 words
        mapped_words.sort()
        print('Done')
    # Skapa listor för reducern
    prepared_words = prepare_mapped_words(mapped_words)
    # Skapa en multiproc pool och mappa till listorna med mapper resultat och reducer

    print(f'Reducing data with some words')
    with Pool() as pool:
        result = pool.imap(reducer, prepared_words)
        # Platta till resultatlistan
        counted_words = {value.split(' - ')[0]: int(value.split(' - ')[1]) for count_list in result for value in count_list}
        print('To Dict')
        # Sortera resultatlistan
    counted_words = {k: v for k, v in sorted(counted_words.items(), key=lambda item: item[1], reverse=True)}
    print('Sorted')
    end = time.time()

    # Skriv de 100 vanligaste orden
    cnt = 0
    for word, count in counted_words.items():
        print(f'{cnt+1}. {word} - {count}')
        cnt += 1
        if cnt == 100:
            break

    print(f'We counted the words in 200 books in {round(end-start, 2)} second(s)')

if __name__ == '__main__':
    main()


"""
1. the - 1319873
2. of - 799142
3. and - 632405
4. to - 514621
5. a - 380580
6. in - 377080
7. that - 244820
8. is - 205789
9. it - 183491
10. i - 176077
"""