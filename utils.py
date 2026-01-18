from datetime import datetime, timezone


# returns current time in UTC ISO format used for time_stamp in event logging
def now_utc_iso():
    return datetime.now(timezone.utc).isoformat()


# prints the details for a single task
def single_task_printer(task_state, task_id):

    if task_id not in task_state:
        print("Invalid task")
        return

    task = task_state[task_id]
    print(f"Task ID: {task_id}")
    print(f'Task Name: {task["task_name"]}')
    print(f'Task Status: {task["status"].upper()}')


# prints all the tasks in the task_state
def all_task_printer(task_state):

    for task_id, task in task_state.items():
        print(f'[{task_id}] {task["task_name"]} - ({task["status"].upper()})')


# prints only the active tasks in the task_state i,e tasks with status 'created'
def active_task_printer(task_state):

    for task_id, task in task_state.items():
        if task["status"] == "created":
            print(f'[{task_id}] {task["task_name"]} - ({task["status"].upper()})')


# prints the warning events
def warning_printer(warning_events):

    for warning_id, warning in warning_events.items():
        print(f"Line {warning_id}: {warning}")


def help_printer():

    print("\nAvailable Commands:\n")

    print("create <task_name>")
    print("  - Creates a new task with status CREATED")
    print("  - Example: create learn_docker\n")

    print("complete <task_id>")
    print("  - Marks an existing task as COMPLETED")
    print("  - Example: complete 101\n")

    print("delete <task_id>")
    print("  - Deletes an existing task")
    print("  - Example: delete 103\n")

    print("list_all")
    print("  - Lists all tasks (CREATED + COMPLETED)\n")

    print("list_tasks")
    print("  - Lists only active tasks (CREATED)\n")

    print("show <task_id>")
    print("  - Shows details of a single task")
    print("  - Example: show 102\n")

    print("help")
    print("  - Displays this help menu\n")

    print("exit")
    print("  - Exits the program\n")
