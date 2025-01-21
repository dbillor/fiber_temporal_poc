# Fiber Repair Workflow (POC)

This is a simple proof-of-concept (POC) application demonstrating how to run a fiber repair workflow using [Temporal](https://docs.temporal.io/). The workflow includes confirming fiber degradation, running an OTDR trace, creating a ticket, shifting traffic off the damaged fiber, invoking a fiber repair agent, pausing until signaled, then shifting traffic back and closing the ticket.

## Contents

- **`activity.py`** – Defines the individual activities.
- **`workflow.py`** – Orchestrates the activities in sequence.
- **`client.py`** – Starts the workflow.
- **`worker.py`** – Runs the worker to execute workflow tasks and activities.

## Prerequisites

- Python 3.7+  
- [Temporal CLI](https://docs.temporal.io/docs/server/quick-install) or a local Temporal server running on `localhost:7233`.
- Install the required Python dependencies (e.g., `temporalio`) with:
  ```bash
  pip install temporalio
  ```

## Usage

1. **Start Temporal Server**  
   Make sure Temporal is running on `localhost:7233`.

2. **Run the Worker**  
   ```bash
   python worker.py
   ```
   The worker will listen for tasks on `FIBER_WORKFLOW_QUEUE`.

3. **Execute the Workflow**  
   In a separate terminal, start the workflow:
   ```bash
   python client.py
   ```
   This will trigger the `FiberRepairWorkflow` with a sample `span_id`. The workflow activities will log progress.

4. **(Optional) Send a Signal**  
   The workflow is paused until it receives the `resume_signal`. You can signal the workflow (for example via Temporal CLI or code) to simulate manual confirmation in a real scenario.

Once the signal is received, the workflow proceeds to shift traffic back and close the ticket.

## Notes

- All activities are no-ops for simplicity. You can add your own logic in the corresponding activity methods.
- The workflow’s pause uses `wait_condition` until the `resume_signal` is triggered.

Feel free to extend or modify each step to suit your production environment or integrate with real fiber repair processes.


## Example from UI

<img width="1968" alt="image" src="https://github.com/user-attachments/assets/f22c0387-74ea-4154-b8c8-513979ba3177" />
