import threading
'''
A Lock is a threading synchronization primitive that can be used to ensure that only one thread executes a particular section of code at a time. 
This is particularly useful when multiple threads need to interact with shared data or resources.
'''
# Shared variable
counter = 0

# Lock object
lock = threading.Lock()

# Target function for threads
def update_counter(amount):
    global counter
    # Acquire the lock before accessing the shared data
    # with lock: block to ensure that the operation is atomic from the perspective of other threads.
    with lock:
        print(f"Thread {threading.current_thread().name} updating counter.")
        start_val = counter
        counter += amount
        end_val = counter
        print(f"Thread {threading.current_thread().name} finished updating: {start_val} -> {end_val}")

if __name__ == "__main__":
    # Create threads that modify the shared counter
    thread1 = threading.Thread(target=update_counter, args=(5,), name='Thread-1')
    thread2 = threading.Thread(target=update_counter, args=(-3,), name='Thread-2')

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for both threads to complete
    thread1.join()
    thread2.join()

    print(f"Final counter value: {counter}")
