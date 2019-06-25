""" Geocode 1000 batches of addresses at a time. """

import time
import threading
import sys
import random
import censusgeocode as cg

from queue import Queue
from queue import Empty


"""
Directions: 
Input_queue := pre-called address
output_queue = tuple(address, geocode)


worker:
    1. call address from the input_queue
    2. api call and get geocodes using the address in the input_queue
    3. input (address, geocode) into the output_queue
master:
    1. put addresses to the input_queue
    2. extract (address, geocode) from the output_queue and add it to the row of the pandas dataframe


Tasks needed to be programmed:
    1. Worker & functions
    2. Master & functions
    3. Master inputs the addresses to the input_queue
    4. Workers deployed in threads
    5. Master aggregates the information from various workers
     

parameters: n_thread, batchsize, timeout_specification

"""


def import_data(size=100):
    return list(range(0, size))


def calculate(number):
    time.sleep(random.randint(0, 100) / 400)  # simulate
    return number * number


def main(n_thread=1):
    print("Get dummy data, a python list.")
    data = import_data()

    # We run differently depending on the number of threads.
    if n_thread < 1:
        raise ValueError("There must be a non-zero number of threads.")
    elif n_thread == 1:
        print("Running single thread.")
        process_single(data)
    else:
        print("Running multiple threads.")
        process(data, n_thread)


def process_single(data):
    """
    Single thread processing.
    """
    start = time.time()
    result = []
    for index, number in enumerate(data):
        print("Processing {} of {}...".format(index + 1, len(data)))
        result.append(calculate(number))
    print("Done - " + str(time.time() - start))
    print(result)


def work(thread_id, input_queue, output_queue, event):
    # Until we have a "done" signal AND the input queue is empty, we run.
    while not event.is_set() or not input_queue.empty():
        try:  # Try to get the input
            index, number = input_queue.get(timeout=0.5)
        except Empty:  # If we get an empty exception, we loop
            continue
        else:  # success, we calculate and put
            print("[W-" + str(thread_id) + "] Calculating: " + str(index) + ", " + str(number))
            result = calculate(number)
            output_queue.put((index, result))  # add to the output queue.


def process(data, n_thread):
    start = time.time()
    input_queue = Queue()  # Inpue queue, e.g. for addresses
    output_queue = Queue()  # Output queue, e.g. for geopoints
    event = threading.Event()  # flag set IFF all inputs have been enqueued.

    left = len(data)  # How many data points left?
    data_index = 0  # index of the processing input.

    result = [None for _ in data]  # None as the placeholder for results.

    # Step 1 - spawn worker threads to wait for the queue and output results.
    for i in range(n_thread):  # spawn n threads.
        t = threading.Thread(target=work, args=(i, input_queue, output_queue, event))
        t.start()  # start off!

    # Step 2 - While not done, input the data (if available), and process the results.
    while left > 0:  # We do "something" while we have work to do.
        if not event.is_set():  # If we are NOT done enqueuing all the input data.
            if data_index < len(data):  # If we have more to enqueue
                number = data[data_index]
                print("[Main] Putting: " + str(data_index) + ", " + str(number))
                input_queue.put((data_index, number))
                data_index += 1
            else:  # We are done enqueueing the input.
                print("[Main] Done enqueueing.")
                event.set()  # workers can quit the while loop as the queue empties.

        while not output_queue.empty():  # While we have output data to process,
            index, number = output_queue.get()
            result[index] = number  # Put the numbers in the correct spot
            left -= 1

    print("Done - " + str(time.time() - start))
    print(result)


if __name__ == "__main__":
    main(n_thread=int(sys.argv[1]))
