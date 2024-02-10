import threading
import time
'''
Read-Write Locks (RWLocks) allow multiple readers to access a resource simultaneously but require exclusive access for writers, 
ensuring that no other readers or writers can access the resource while a write operation is in progress. 
This optimization is useful for resources that are read frequently but written to infrequently, as it allows higher concurrency than a standard mutex lock.

Python's standard library does not include a direct implementation of read-write locks, but we can easily implement or simulate one using the threading module. 
Below is a simple example of how you might implement a basic Read-Write Lock in Python.
'''
class ReadWriteLock:
    def __init__(self):
        self.readers = 0
        self.lock = threading.Lock()
        self.write_wants_entry = threading.Event()
        self.read_entry = threading.Semaphore(value=1)

    def acquire_read(self):
        self.write_wants_entry.wait()
        self.read_entry.acquire()
        with self.lock:
            self.readers += 1
            if self.readers == 1:
                self.write_wants_entry.clear()
        self.read_entry.release()

    def release_read(self):
        with self.lock:
            self.readers -= 1
            if self.readers == 0:
                self.write_wants_entry.set()

    def acquire_write(self):
        self.write_wants_entry.wait()
        self.write_wants_entry.clear()

    def release_write(self):
        self.write_wants_entry.set()

# Example usage
rwlock = ReadWriteLock()

def reader():
    print(f"{threading.current_thread().name} is trying to read")
    rwlock.acquire_read()
    print(f"{threading.current_thread().name} has started reading")
    time.sleep(1)  # Simulate read operation
    print(f"{threading.current_thread().name} has finished reading")
    rwlock.release_read()

def writer():
    print(f"{threading.current_thread().name} is trying to write")
    rwlock.acquire_write()
    print(f"{threading.current_thread().name} has started writing")
    time.sleep(1)  # Simulate write operation
    print(f"{threading.current_thread().name} has finished writing")
    rwlock.release_write()

if __name__ == "__main__":
    # Creating reader and writer threads
    reader_threads = [threading.Thread(target=reader) for _ in range(5)]
    writer_threads = [threading.Thread(target=writer) for _ in range(2)]

    # Starting the threads
    for t in reader_threads + writer_threads:
        t.start()

    # Waiting for all threads to complete
    for t in reader_threads + writer_threads:
        t.join()

    print("Example completed.")
