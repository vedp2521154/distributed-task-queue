class Worker:
    def __init__(self, name):
        self.name = name

    def execute(self, task):
        task.status = "RUNNING"

        print(f"{self.name} is executing: {task.name}")

        task.status = "SUCCESS"

        print(f"Task {task.task_id} completed with status: {task.status}")
    