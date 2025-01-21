import asyncio
import logging
from temporalio.client import Client
from temporalio.worker import Worker

from workflow import FiberRepairWorkflow
from activities import (
    confirm_fiber_degraded,
    run_otdr_trace,
    create_ticket,
    shift_off_traffic,
    invoke_fiber_agent,
    shift_traffic_back,
    close_ticket,
)
# Configure root logger
logging.basicConfig(
    level=logging.INFO,  # Set desired logging level
    format="%(asctime)s %(message)s",  # Log format
    handlers=[logging.StreamHandler()],  # Log to console
    )



async def main():
    # Connect to local Temporal server
    client = await Client.connect("localhost:7233")

    # Create a Worker
    worker = Worker(
        client=client,
        task_queue="FIBER_WORKFLOW_QUEUE",
        workflows=[FiberRepairWorkflow],
        activities=[
            confirm_fiber_degraded,
            run_otdr_trace,
            create_ticket,
            shift_off_traffic,
            invoke_fiber_agent,
            shift_traffic_back,
            close_ticket,
        ],
    )

    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
