# Event-Sourced CLI Task Manager

## Overview

A command-line task manager written in Python that records **all task changes as immutable events** and rebuilds application state by **replaying those events** from an append-only log file.

This project is intentionally **simple and file-based**. Its purpose is not to be production-ready, but to clearly demonstrate how event-sourced systems work at a fundamental level.

---

## Project Purpose

This project was built as a learning exercise to understand:

* How backend systems can manage state using **events instead of mutable records**
* How application state can be **deterministically reconstructed** from history
* Why append-only logs are safer and more debuggable than direct state persistence
* How to handle corrupted data and invalid operations **without crashing the system**

This is a **system design and learning project**, not a production tool.

---

## Design Constraints (Intentional)

To keep the focus on core system concepts, this project intentionally:

* Uses file-based persistence only (no database)
* Has no concurrency or multi-user support
* Does not implement snapshots or log compaction
* Has no authentication, networking, or production hardening

These constraints are deliberate and support learning rather than feature completeness.

---

## Features

* Create, complete, and delete tasks via CLI commands
* Persist all task changes as **append-only JSON Lines (JSONL) events**
* Rebuild task state on startup by replaying the event log
* List active tasks, all tasks, or a single task
* Detect and report corrupted or logically invalid events
* Keep the system running even when encountering bad data
* Simple built-in help menu

---

## How It Works

1. **Startup (Event Replay)**
   The application reads `tasks.log` line-by-line and attempts to parse each line as a JSON event.

2. **Validation & Warnings**

   * Corrupted JSON lines are skipped
   * Logically invalid operations (e.g., completing a non-existent task) are recorded as warnings

3. **State Reconstruction**
   Valid events are replayed in order to rebuild the current in-memory task state.

4. **Command Execution**
   User commands generate new events. These events are:

   1. Written to the log
   2. Then applied to the in-memory state

The log is the **source of truth**. In-memory state is treated as a derived cache.

---

## How to Run

### Requirements

* Python 3.x
### Using the Sample Log

The repository includes a `sample_events.log` file containing both valid and intentionally invalid events.

To start the program using the sample log:

1. Rename `sample_events.log` to `tasks.log`, or
2. Modify the log file path in `event_io.py`

By default, the application creates and appends to `tasks.log` at runtime.


### Steps

1. Clone the repository.
2. Run the program:

```bash
python main.py
```

---

## Supported Commands

| Command               | Description                   | Example                    |
| --------------------- | ----------------------------- | -------------------------- |
| `create_task <title>` | Create a new task             | `create_task learn_docker` |
| `complete_task <id>`  | Mark a task as completed      | `complete_task 5`          |
| `delete_task <id>`    | Delete a task                 | `delete_task 10`           |
| `list_tasks`          | List active (CREATED) tasks   | `list_tasks`               |
| `list_all`            | List all tasks                | `list_all`                 |
| `show_task <id>`      | Show details for one task     | `show_task 3`              |
| `show_warnings`       | Show warnings from log replay | `show_warnings`            |
| `help`                | Show help menu                | `help`                     |
| `exit` / `quit`       | Exit the program              | `exit`                     |

> ⚠️ Command syntax is strict. Invalid formats are rejected.

---

## Project Structure

```
.
├── main.py          # Application entry point and main loop
├── commands.py      # Command parsing and validation
├── event_io.py      # Event reading and writing (JSON Lines)
├── state.py         # In-memory task state updates
├── utils.py         # Printing helpers and time utilities
├── sample_tasks.log # Sample event log demonstrating valid and invalid events
├── tasks.log        # created at runtime (gitignored)
├── README.md
├── LICENSE
```

Each module has a **single responsibility** to keep the system easier to reason about and modify.

---

## Log Format (JSON Lines)

Each line in `tasks.log` represents exactly one event:

```json
{"time_stamp":"2026-01-15T09:00:00+00:00","task_id":1,"event_type":"task_created","task_name":"learn python"}
{"time_stamp":"2026-01-15T10:00:00+00:00","task_id":1,"event_type":"task_completed"}
```

Why JSONL?

* Append-friendly (no file rewrites)
* Partial corruption does not destroy the entire file
* Easy to replay sequentially

---

## Sample Output

### Startup (Event Replay)

```
INFO: Replayed 19 events
WARN: Skipped corrupted event at line 4
WARN: Skipped corrupted event at line 27
INFO: System ready
```

### Listing All Tasks

```
command: list_all
[1] learn python - (COMPLETED)
[2] learn sql - (COMPLETED)
[5] learn fastapi - (CREATED)
```

### Viewing Warnings

```
command: show_warnings
Line 8: completing an already completed task
Line 12: completing a non-existent task
```

---

## Learning Outcomes

Through this project, I learned:

* Fundamentals of **event sourcing** and event replay
* Why events are the immutable source of truth and state is a cache
* How backend systems rebuild state deterministically
* Practical differences between JSON and JSON Lines (JSONL)
* Why JSONL is preferred for append-only backend logs
* How to safely read, write, and validate JSON data in Python
* The difference between `json.dump` and `json.dumps`
* Why commands should produce events instead of mutating state directly
* Why events should be persisted **before** updating in-memory state
* How to work with UTC timestamps using `datetime`
* Designing clear function return contracts
* Separating parsing logic from business logic (ongoing improvement)
* Handling corrupted input and invalid operations without crashing
* Avoiding silent failures in interactive programs
* Python language details such as tuple syntax and subtle edge cases
* The importance of naming, formatting, and code consistency

---

## Design Trade-offs

This project makes several deliberate trade-offs to prioritize **clarity of system behavior** over completeness:

* Uses file-based persistence instead of a database
* Assumes a single-user, single-process environment
* Replays the full event log on startup (no snapshots)
* Keeps error handling simple and mostly centralized
* Defers automated tests to reduce abstraction overhead at this stage

These decisions keep the system easy to inspect, reason about, and debug while learning event-sourced design.

---

## Possible Improvements

If this project were extended further, the next logical steps would be:

* Adding log snapshots to reduce startup replay time
* Introducing automated tests for event replay and state transitions
* Further separating parsing, validation, and business logic
* Improving error reporting structure
* Refining naming and module boundaries as complexity grows

These improvements were intentionally deferred to avoid obscuring the core learning goals.

---

## License

MIT License



