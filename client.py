# client.py
import asyncio
import logging
from temporalio.client import Client
from workflow import FiberRepairWorkflow

logging.basicConfig(level=logging.INFO)

async def main():
    # Connect to Temporal
    client = await Client.connect("localhost:7233")

    # Start the workflow with your custom argument
    handle = await client.start_workflow(
        FiberRepairWorkflow.run,
        "iad666",  # pass span_id as a positional argument
        id="fiber_repair_workflow-id",
        task_queue="FIBER_WORKFLOW_QUEUE",
    )

    logging.info(f"Started workflow with ID: {handle.id}")

    # Optionally wait for the result
    await handle.result()
    logging.info("Workflow completed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
