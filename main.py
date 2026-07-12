import time

from task import Task
from queue import TaskQueue
from worker import Worker


def buy_groceries():
    print("Groceries purchased")

def send_email():
    raise Exception("Email server is down")

def generate_pdf():
    print("PDF generated")

queue = TaskQueue()
worker = Worker("Worker-1")

task1 = Task(1, "Buy groceries", buy_groceries)
task2 = Task(2, "Send email", send_email)
task3 = Task(3, "Generate PDF", generate_pdf)

queue.add_task(task1)
queue.add_task(task2)
queue.add_task(task3)

while True:
    task = queue.get_task()

    if task is None:
        break

    success = worker.execute(task)

    if not success:
        if task.retry_count < task.max_retries:
            task.retry_count += 1
            delay = 2 ** (task.retry_count - 1)
            task.status = "PENDING"

            print(
                f"Retrying Task {task.task_id}. "
                f"Retry count: {task.retry_count}"
            )

            print(f"Waiting {delay} seconds before retry")

            time.sleep(delay)

            queue.add_task(task)

        else:
            print(
                f"Task {task.task_id} reached maximum retries "
                f"and permanently failed"
            )
