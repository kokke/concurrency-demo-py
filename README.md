# ThreadPoolExecutor vs ProcessPoolExecutor

100 lines of code showcasing the trade-offs between process-based vs thread-based concurrency in Python.

ThreadPoolExecutor is limited by Python's GIL (Global Interpreter Lock) and can only utilize a single CPU-core at a time.

ProcessPoolExecutor spawns a new process, and can effectively use all cores concurrently, but there is an initial overhead.

---

TL;DR:

- ThreadPoolExecutor  works best for I/O-bound tasks

- ProcessPoolExecutor works best for CPU-bound tasks

Options:

    # run a CPU-bound workload using thread-concurrency
    python demo.py cpu threads 

    # run a I/O-bound workload using thread-concurrency
    python demo.py io threads 

    # run a CPU-bound workload using thread-concurrency
    python demo.py cpu procs 

    # run a I/O-bound workload using thread-concurrency
    python demo.py io procs 
