from vanity_address import *
import multiprocessing
from os import cpu_count

def generator(pattern, count):
    VanityAddress.address_generator(count, pattern)

    return True

def multiple_generators(pattern=''):
    # provide count of available core for generating the addressess
    count = cpu_count()

    # list to store multiprocessing instances
    core = []

    for i in range (count):
        core.append(multiprocessing.Process(target=generator, args=(pattern, i,)))

    # start multiprocessing instances to proceed with the task
    for i in core:
        i.start()
    
    # join multiprocessing instances
    for i in core:
        i.join()

    return True

if __name__ == '__main__':
    print('\nUse Multiple Cores when you want to generate address of specific pattern (else not recommended)')
    if 'Y' == input('\nDo you want the program to use all core of processor for generating address as fast as possible ? (Y/N) : ').upper():
        print('\nThe program will start generating address using multiprocessing...')
        multiple_generators(input('\nPlease enter the pattern you are about to search in BTC address (else leave empty) : '))
    else:
        print('\nThe program will start generating address...')
        generator(input('\nPlease enter the pattern you are about to search in BTC address (else leave empty) : '))