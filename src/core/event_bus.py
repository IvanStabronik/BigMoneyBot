import queue

class EventBus:
    """
    Simple thread-safe queue wrapper for passing events between components.
    """
    def __init__(self):
        self.queue = queue.Queue()

    def put(self, event):
        self.queue.put(event)

    def get(self, block=True, timeout=None):
        return self.queue.get(block, timeout)

    def empty(self):
        return self.queue.empty()
