import threading

# Function that takes multiple arguments
def greet(name, greeting, say):
    message = f"{greeting}, {name}! {say}, {name}"
    print(message)

if __name__ == "__main__":
    # Arguments and keyword arguments for the function
    args = ("Alice",)
    kwargs = {"greeting": "Hi", "say":"Hello"}

    # Create and start the thread
    thread = threading.Thread(target=greet, args=args, kwargs=kwargs)
    thread.start()

    # Wait for the thread to complete
    thread.join()
