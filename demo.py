"""
    Demo of running code in ThreadPoolExecutor vs ProcessPoolExecutor

    ThreadPoolExecutor  works best for I/O-bound tasks
    ProcessPoolExecutor works best for CPU-bound tasks

    ThreadPoolExecutor is limited by Python's GIL (Global Interpreter Lock) and can only utilize a single CPU-core at a time.
    ProcessPoolExecutor spawns a new process, and can effectively use all cores concurrently


    Options:

        # run a CPU-bound workload using thread-concurrency
        python demo.py cpu threads 

        # run a I/O-bound workload using thread-concurrency
        python demo.py io threads 

        # run a CPU-bound workload using thread-concurrency
        python demo.py cpu procs 

        # run a I/O-bound workload using thread-concurrency
        python demo.py io procs 

"""


from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait, ALL_COMPLETED
import sys
import time
import os
import random
import requests
import subprocess


ntasks = 200
nthreads = 32
results = list()



def callback_function(result):
    results.append(result)

def io_bound_task(id):
    time.sleep(1)
    callback_function(id)

def cpu_bound_task(id):
    t0 = time.time()
    iters = 0
    while time.time() - t0 < 1.0:
        iters += 1
    callback_function(iters)

    


if __name__ == "__main__":
    bef = time.time()

    # correct usage?
    if (len(sys.argv) < 3) or (sys.argv[1] not in ["cpu", "io"]) or (sys.argv[2] not in ["threads", "procs"]):
        print("\n\nusage: %s <io|cpu> <threads|procs>\n" % sys.argv[0])
        sys.exit(-1)

    # select workload + concurrency-model
    cpu_bound   = (sys.argv[1] == "cpu")
    use_threads = (sys.argv[2] == "threads")

    # output the choice to the user
    msg1 = "I/O-bound workload"
    msg2 = "process-based concurrency"
    if cpu_bound:
        msg1 = "CPU-bound workload"
    if use_threads:
        msg2 = "thread-based concurrency"
    print(msg1, "with", msg2)


    # thread or process-based concurrency?
    if use_threads:
        executor = ThreadPoolExecutor(max_workers=nthreads)
    else:
        executor = ProcessPoolExecutor(max_workers=nthreads)
    

    # map
    futures = list()
    for num in range(ntasks):
        # CPU or I/O bound workload?
        if cpu_bound:
            fut = executor.submit(cpu_bound_task, num)
        else:
            fut = executor.submit(io_bound_task, num)
        futures.append(fut)


    # reduce
    print("waiting")
    wait(futures, return_when = ALL_COMPLETED)
    aft = time.time()
    print("\ntook", aft-bef, "seconds")

