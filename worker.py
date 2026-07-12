class Worker:
    def __init__(self, name):
        self.name = name

    def execute(self, task):
        task.status = "RUNNING"

        print(f"{self.name} is executing: {task.name}")

        try:
            task.function()

            task.status = "SUCCESS"

            print(
                f"Task {task.task_id} completed with status: {task.status}"
            )

            return True

        except Exception as error:
            task.status = "FAILED"

            print(
                f"Task {task.task_id} failed with error: {error}"
            )

            return False
