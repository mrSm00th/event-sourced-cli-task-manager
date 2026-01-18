from commands import command_parser, command_handler
from event_io import event_reader
from utils import (
    active_task_printer,
    all_task_printer,
    single_task_printer,
    warning_printer,
    help_printer,
)
from sys import exit


def main():

    task_state, warning_events, curr_task_id = event_reader("tasks.log")


    while True:
        raw_inp = command_parser()
        
        action = raw_inp[0]
        task_title = raw_inp[1] if len(raw_inp) == 2 else None

        if action is None:
            print(task_title)
            continue

        if action in [
            "list_tasks",
            "list_all",
            "show_warnings",
            "help",
            "exit",
            "quit",
        ]:

            # check for - 'list_tasks', 'list_all', 'show_task', 'show_warnings', 'help', 'exit', 'quit'
            command = raw_inp[0]

            if command == "list_tasks":
                active_task_printer(task_state)

            elif command == "list_all":
                all_task_printer(task_state)

            elif command == "show_warnings":
                warning_printer(warning_events)

            elif command in ("exit", "quit"):
                exit("EXITING THE PROGRAM")

            elif command == "help":
                help_printer()

        #check for show_task
        elif action == "show_task":
            
            try:
                task_id = int(raw_inp[1])

            except ValueError:
                print("Task ID must be an integer")
                continue

            if task_id in task_state:
                single_task_printer(task_state, task_id)

            else:
                print("Task does not exist")
                continue 

        # other commands - create, complete, delete
        else:
            try:

                state, new_task_id = command_handler(
                    task_state, action, task_title, curr_task_id
                )

                if state is None:
                    print(new_task_id)
                else:
                    task_state, curr_task_id = state, new_task_id

            except (ValueError, TypeError) as e:
                print("Internal error:", e)


if __name__ == "__main__":
    main()
