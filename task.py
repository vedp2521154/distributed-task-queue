class Task:
    def __init__(self, task_id, name, function, max_retries=3):
        self.task_id = task_id
        self.name = name
        self.function = function
        self.status = "PENDING"
        self.retry_count = 0
        self.max_retries = max_retries
