from temporalio import workflow
from datetime import timedelta
from typing import Optional

from activities import (
    confirm_fiber_degraded,
    run_otdr_trace,
    create_ticket,
    shift_off_traffic,
    invoke_fiber_agent,
    shift_traffic_back,
    close_ticket,
)

@workflow.defn(sandboxed=False)
class FiberRepairWorkflow:
    def __init__(self) -> None:
        self._paused = False  # State to track if the workflow is paused

    @workflow.signal
    async def resume_signal(self) -> None:
        """Signal to resume the workflow."""
        self._paused = True

    @workflow.run
    async def run(self, span_id: str) -> None:
        # Confirm fiber degraded
        await workflow.execute_activity(
            confirm_fiber_degraded,
            span_id,
            schedule_to_close_timeout=timedelta(seconds=30)
        )
        workflow.logger.info("Fiber is degraded")

        # Run OTDR trace
        await workflow.execute_activity(
            run_otdr_trace,
            span_id,
            schedule_to_close_timeout=timedelta(seconds=30)
        )
        workflow.logger.info("OTDR trace completed")

        # Create ticket
        await workflow.execute_activity(
            create_ticket,
            span_id,
            schedule_to_close_timeout=timedelta(seconds=30)
        )
        workflow.logger.info("Ticket created")

        # Shift traffic off
        await workflow.execute_activity(
            shift_off_traffic,
            span_id,
            schedule_to_close_timeout=timedelta(seconds=30)
        )
        workflow.logger.info("Traffic shifted off")

        # Invoke fiber agent
        await workflow.execute_activity(
            invoke_fiber_agent,
            span_id,
            schedule_to_close_timeout=timedelta(seconds=30)
        )
        workflow.logger.info("Fiber agent invoked")

        # Pause the workflow and wait for a signal
        await workflow.wait_condition(lambda: self._paused)
        workflow.logger.info("Workflow unpaused because fiber provider has repaired fiber")

        # Shift traffic back
        await workflow.execute_activity(
            shift_traffic_back,
            span_id,
            schedule_to_close_timeout=timedelta(seconds=30)
        )
        workflow.logger.info("Traffic shifted back")

        # Close ticket
        await workflow.execute_activity(
            close_ticket,
            span_id,
            schedule_to_close_timeout=timedelta(seconds=30)
        )
        workflow.logger.info("Ticket closed")
