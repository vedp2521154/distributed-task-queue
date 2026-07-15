from queue import Empty, Queue


class TaskQueue:
    def __init__(self):
        self.tasks = Queue()

    def add_task(self, task):
        self.tasks.put(task)

    def get_task(self, timeout=1):
        try:
            return self.tasks.get(timeout=timeout)
        except Empty:
            return None

    def task_done(self):
        self.tasks.task_done()

    def wait_until_complete(self):
        self.tasks.join()
