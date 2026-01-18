def state_updater(task_state, action, task_id, task_title=None):

    if action == "complete":  # allowed actions - create, complete, delete

        task_state[task_id]["status"] = "completed"

    elif action == "create":
        task_state[task_id] = {"task_name": task_title, "status": "created"}

    elif action == "delete":
        del task_state[task_id]

    return task_state
