from agents import Agent, ModelSettings
from .utils import UserContext
from .tools import getting_timings, searching_book, check_availability
from .guardrails import only_liabrary_guardrials
from .instructions import dynamic_instruction

library_agent =Agent[UserContext](
    name="Library Assistant",
    instructions=dynamic_instruction,
    tools=[getting_timings,searching_book,check_availability],
    input_guardrails=[only_liabrary_guardrials],
    model_settings=ModelSettings(
        temperature=0.2,
        parallel_tool_calls=True,        
        request_timeout=60,
    ),
)