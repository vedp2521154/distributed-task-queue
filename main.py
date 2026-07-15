import time
import threading

from task import Task
from task_queue import TaskQueue
from worker import Worker
from database import Database


def buy_groceries():
    time.sleep(3)
    print("Groceries purchased")


def send_email():
    time.sleep(3)
    raise Exception("Email server is down")


def generate_pdf():
    time.sleep(3)
    print("PDF generated")

FUNCTION_REGISTRY = {
    "Buy groceries": buy_groceries,
    "Send email": send_email,
    "Generate PDF": generate_pdf,
}

database = Database()
queue = TaskQueue()
SHUTDOWN = object()
workers = [
    Worker("Worker-1"),
    Worker("Worker-2"),
    Worker("Worker-3"),
]

task1 = Task(13, "Buy groceries", buy_groceries)
task2 = Task(14, "Send email", send_email)
task3 = Task(15, "Generate PDF", generate_pdf)


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

def worker_loop(worker):
    while True:
        task = queue.get_task()

        if task is None:
            continue

        if task is SHUTDOWN:
            queue.task_done()
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
        queue.task_done()

threads = []

for worker in workers:
    thread = threading.Thread(
        target=worker_loop,
        args=(worker,),
    )

    threads.append(thread)
    thread.start()

queue.wait_until_complete()

for worker in workers:
    queue.add_task(SHUTDOWN)

queue.wait_until_complete()

for thread in threads:
    thread.join()
