from event_io import event_writer_create, event_writer_others
from state import state_updater


def command_parser():

    valid_commands = ["create_task", "complete_task", "delete_task"]
    user_inp = input("command: ").strip().lower()

    # list_tasks - only created tasks(running tasks)
    # list_all - all tasks

    if user_inp in ["list_tasks", "list_all", "show_warnings", "help", "exit", "quit"]:
        return (user_inp,)

    elif user_inp.startswith("show_task"):
        parts = user_inp.split(" ", 1)

        if len(parts) != 2:
            return (None, "invalid command")

        command, task_id = parts
        return (command, task_id)

    else:

        try:

            command, task_title = user_inp.split(" ")
            action, place_hldr = command.split(
                "_", 1
            )  # command in form - : action place_hldr(task)

            if command in valid_commands:

                if action == "create" and not (task_title.isdigit()):
                    return (action, task_title)

                elif action == "complete" and task_title.isdigit():
                    return (action, int(task_title))

                elif action == "delete" and task_title.isdigit():
                    return (action, int(task_title))

                else:
                    return (None, "invalid command")

            else:
                return (None, "invalid command")  # command not in specified command

        except ValueError:
            return (None, "invalid command")  # error while splitting


def command_handler(task_state, action, task_title, curr_task_id):
    # action & task_title from command_parser
    # task_state(dict) and curr_task_id from the main

    if action == "create":  # command - create_task discription
        for task in task_state.values():
            if task["task_name"] == task_title and task["status"] == "created":

                return (None, "Task already exist. cant create duplicate task")

        # call the file writer and write event
        # curr_task_id+=1 ALREADY HANDELED IN FILE-LOGIC
        event_writer_create("task_created", curr_task_id, task_title)

        # create the task in task_state
        task_state = state_updater(task_state, action, curr_task_id, task_title)

        return (task_state, curr_task_id)

    elif action == "complete":
        if task_title in task_state and task_state[task_title]["status"] == "created":

            #  call the file writer and write event
            event_writer_others("task_completed", task_title)
            # complete the task in task_state
            task_state = state_updater(task_state, action, task_title)

        else:

            return (None, "cant complete a non existing task")

    elif action == "delete":
        if task_title in task_state and (
            task_state[task_title]["status"] == "created"
            or task_state[task_title]["status"] == "completed"
        ):
            # call the file writer and write event
            event_writer_others("task_deleted", task_title)
            # delete the task from task_state
            task_state = state_updater(task_state, action, task_title)

        else:
            return (None, "cant delete a non existing task")

    return (task_state, curr_task_id)
