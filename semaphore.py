import threading
import time
import random

'''
A semaphore is a synchronization primitive that is used to manage access to a common resource by multiple threads. 
Unlike a lock that only allows one thread to access a resource at a time, a semaphore allows a fixed number of threads to access a shared resource simultaneously.
A semaphore can be used to ensure that only a limited number of threads can access these connections at any given time.
'''

# Simulate database operations
def access_database(connection_id):
    print(f"Thread {threading.current_thread().name} is using connection {connection_id}")
    time.sleep(random.randint(1, 3))  # Simulate time taken for database operations
    print(f"Thread {threading.current_thread().name} is releasing connection {connection_id}")

# Function that threads will run
def thread_task(semaphore, connection_id):
    with semaphore:
        access_database(connection_id)

if __name__ == "__main__":
    # Create a semaphore with 3 permits
    max_connections = 3
    semaphore = threading.Semaphore(max_connections)

    # List to hold all the threads
    threads = []

    # Create and start 10 threads to simulate 10 database access requests
    for i in range(10):
        thread = threading.Thread(target=thread_task, args=(semaphore, i))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All database operations completed.")
