import threading
import time
import random

'''
Condition variables are a synchronization primitive that allows threads to wait for certain conditions to become true. 
Unlike a lock that merely prevents multiple threads from executing the same piece of code simultaneously, 
condition variables allow threads to pause execution and wait, without consuming CPU resources, until some condition is met.

A common use case for condition variables is producer-consumer scenarios, where one or more producer threads generate data and put it into a buffer, 
and one or more consumer threads take data out of the buffer for processing. The condition variable is used to signal between producers and consumers about the state of the buffer.
'''

'''
In the Python code provided, buffer, lock, and condition do not need to be explicitly declared as global within the producer and consumer functions because 
these variables are not being reassigned within those functions. In Python, global variables can be accessed inside a function without declaring 
them as global if they are only being read or modified (e.g., appending to a list or modifying an object that the variable references). 
The global keyword is necessary only when you want to assign a new value to a global variable within a function, which is not the case with buffer, lock, and condition in your program.
'''
# A shared buffer and a lock for synchronizing access to it
buffer = []
buffer_size = 10
lock = threading.Lock()
# Condition variable associated with the lock
condition = threading.Condition(lock)

# Shared variable to signal threads to stop
stop_threads = False

# Producer thread function
def producer():
    global stop_threads
    while not stop_threads:
        with condition:  # Acquire the lock and enter the context
            if len(buffer) < buffer_size:
                item = random.randint(1, 100)
                buffer.append(item)
                print(f"Producer produced {item}, buffer size: {len(buffer)}")
                condition.notify()  # Signal a waiting consumer, if any
            else:
                print("Buffer full, producer is waiting.")
                condition.wait()  # Wait until a consumer notifies
            time.sleep(random.random())

        if stop_threads:
            break
        
# Consumer thread function
def consumer():
    global stop_threads
    while not stop_threads:
        with condition:  # Acquire the lock and enter the context
            if buffer:
                item = buffer.pop(0)
                print(f"Consumer consumed {item}, buffer size: {len(buffer)}")
                condition.notify()  # Signal a waiting producer, if any
            else:
                print("Buffer empty, consumer is waiting.")
                condition.wait()  # Wait until a producer notifies
            time.sleep(random.random())

        if stop_threads:
            break

if __name__ == "__main__":
    # Create and start the producer and consumer threads
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    producer_thread.start()
    consumer_thread.start()

    # Let's run the threads for some time and then stop (for example purposes)
    time.sleep(10)

    stop_threads = True
    condition.acquire()
    condition.notify_all()
    condition.release()

    producer_thread.join()
    consumer_thread.join()
