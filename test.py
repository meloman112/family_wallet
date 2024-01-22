#import numpy as np

def sum_strings(x, y):
    x = string_to_int(x)
    y = string_to_int(y)
    result = x + y
    return str(result)


def string_int(st):
    ls = [c for c in st]
    ls.reverse()
    num = 0
    nal = 1
    for i in ls:
        #if i in ['0', '1', '2']:
        if i == "0":
            i = 0
        elif i == "1":
            i = 1
        elif i == '2':
             i = 2
        #elif i in ['3', '4', '5']:
        elif i == "3":
            i = 3
        elif i == '4':
            i = 4
        elif i == '5':
            i = 5
        #else:
        elif i == "6":
            i = 6
        elif i == "7":
            i = 7
        elif i == "8":
            i = 8
        else:
            i = 9
        num += nal * i
        nal *= 10
    return num

def string_to_int(s):
    result = 0


    # Преобразование строки в число
    # Преобразование строки в число
    for char in s:
        char_code = ord(char)
        if 48 <= char_code <= 57:  # Диапазон кодов ASCII для цифр '0'-'9'
            result = result * 10 + (char_code - 48)
        else:
            break


    return  result

import timeit

ls =[]
for i in range(1000):
    start = timeit.default_timer()
    suma = sum_strings('5648941', '45668465')
    stop = timeit.default_timer()
    timelimit = (stop - start)*10000000
    #print(f'time: {(stop - start)*10000000} mln seconds')
    ls.append(timelimit)
print(sum(ls)/1000)
