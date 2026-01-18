import json
from utils import now_utc_iso


def event_reader(file_name):

    curr_task_id = 0
    task_state = {}
    warning_events = {}
    events_read = 0
    corrupted_lines = []
    try:
        with open(file_name) as file:

            for i, line in enumerate(file, start=1):

                if not line.strip():
                    continue

                try:
                    event = json.loads(line)

                    events_read += 1

                    event_type = event["event_type"]
                    task_id = event["task_id"]


                    if event_type == "task_created":

                        if task_id not in task_state:
                            task_state[task_id] = {
                                "task_name": event["task_name"],
                                "status": "created",
                            }
                            curr_task_id = max(curr_task_id, task_id)
                        else:
                            warning_events[i] = "Creating an already created task"
                            continue

                    elif event_type == "task_completed":

                        if (
                            task_id in task_state
                            and task_state[task_id]["status"] != "completed"
                        ):
                            task_state[task_id]["status"] = "completed"
                        elif (
                            task_id in task_state
                            and task_state[task_id]["status"] == "completed"
                        ):
                            warning_events[i] = "completing an already completed  task"
                            continue
                        else:
                            warning_events[i] = "completing a non existing task"
                            continue

                    elif event_type == "task_deleted":

                        if task_id in task_state:
                            del task_state[task_id]
                        else:
                            warning_events[i] = "deleting and non existing task"
                            continue

                except (json.JSONDecodeError, KeyError):
                    corrupted_lines.append(i)
                    continue

    except FileNotFoundError:
        print("File not found")

    print(f"INFO: Replayed {events_read} events")
    for line in corrupted_lines:
        print(f"WARN: Skipped corrupted event at line {line}")

    print("INFO: System ready")

    return task_state, warning_events, curr_task_id + 1


def event_writer_create(action, curr_task_id, task_title, file_name="tasks.log"):

    time_stamp = now_utc_iso()
    event = {
        "time_stamp": time_stamp,
        "task_id": curr_task_id,
        "event_type": action,
        "task_name": task_title,
    }

    with open(file_name, "a") as file:
        row = json.dumps(event)
        file.write(row + "\n")


def event_writer_others(action, task_id, file_name="tasks.log"):

    time_stamp = now_utc_iso()
    event = {"time_stamp": time_stamp, "task_id": task_id, "event_type": action}

    with open(file_name, "a") as file:
        row = json.dumps(event)
        file.write(row + "\n")

        
