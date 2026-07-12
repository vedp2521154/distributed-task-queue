from task import Task
from queue import TaskQueue
from worker import Worker

queue = TaskQueue()
worker = Worker("Worker-1")

task1 = Task(1, "Buy groceries")
task2 = Task(2, "Send email")
task3 = Task(3, "Generate PDF")

queue.add_task(task1)
queue.add_task(task2)
queue.add_task(task3)

while True:
    task = queue.get_task()

    if task is None:
        break

    worker.execute(task)

