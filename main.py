import time

from task import Task
from queue import TaskQueue
from worker import Worker
from database import Database


def buy_groceries():
    print("Groceries purchased")

def send_email():
    raise Exception("Email server is down")

def generate_pdf():
    print("PDF generated")

FUNCTION_REGISTRY = {
    "Buy groceries": buy_groceries,
    "Send email": send_email,
    "Generate PDF": generate_pdf,
}

database = Database()
queue = TaskQueue()
worker = Worker("Worker-1")

task1 = Task(1, "Buy groceries", buy_groceries)
task2 = Task(2, "Send email", send_email)
task3 = Task(3, "Generate PDF", generate_pdf)


existing_task_ids = database.load_all_task_ids()
pending_tasks = database.load_pending_tasks()


for saved_task in pending_tasks:
    task_id = saved_task[0]
    name = saved_task[1]
    status = saved_task[2]
    retry_count = saved_task[3]
    max_retries = saved_task[4]

    function = FUNCTION_REGISTRY[name]

    recovered_task = Task(
        task_id,
        name,
        function,
        max_retries,
    )

    recovered_task.status = status
    recovered_task.retry_count = retry_count
    queue.add_task(recovered_task)

fresh_tasks = [task1, task2, task3]

for task in fresh_tasks:
    if task.task_id not in existing_task_ids:
        database.save_task(task)
        queue.add_task(task)

while True:
    task = queue.get_task()

    if task is None:
        break

    success = worker.execute(task)
    database.update_task(task)

    if not success:
        if task.retry_count < task.max_retries:
            task.retry_count += 1
            delay = 2 ** (task.retry_count - 1)
            task.status = "PENDING"
            database.update_task(task)

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
