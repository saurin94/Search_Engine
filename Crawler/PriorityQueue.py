import heapq
# Create a priority queue abstract base class
class priority_queue:
    # Initialize the instance
    def __init__(self):
        # Create a list to use as the queue
        self._queue = []
        # Create an index to use as ordering
        self._index = 0

    # Create a function to add a task to the queue
    def enqueue(self, item, priority):
        # Push the arguments to the _queue using a heap
        heapq.heappush(self._queue, (-priority, self._index, item))
        # Add one to the index
        self._index += 1

    # Create a function to get the next item from the queue
    def dequeue(self):
        # Return the next item in the queue
        return heapq.heappop(self._queue)[-1]

    def size(self):
        return len(self._queue)
