from temporalio import activity

@activity.defn
async def confirm_fiber_degraded(span_id: str) -> None:
    pass

@activity.defn
async def run_otdr_trace(span_id: str) -> None:
    pass

@activity.defn
async def create_ticket(span_id: str) -> None:
    pass

@activity.defn
async def shift_off_traffic(span_id: str) -> None:
    pass

@activity.defn
async def invoke_fiber_agent(span_id: str) -> None:
    pass

@activity.defn
async def shift_traffic_back(span_id: str) -> None:
    pass

@activity.defn
async def close_ticket(span_id: str) -> None:
    pass
