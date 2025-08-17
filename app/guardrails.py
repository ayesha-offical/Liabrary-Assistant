from agents import input_guardrail, GuardrailFunctionOutput, Agent, RunContextWrapper
from .utils import UserContext, liabray_related

@input_guardrail
def only_liabrary_guardrials(
    ctx:RunContextWrapper[UserContext],
    agent:Agent,
    user_input:str,
) -> GuardrailFunctionOutput:
     
    if liabray_related(user_input):
        return GuardrailFunctionOutput(
            tripwire_triggered=False,
            output_info={"status": "on_topic"}
        )


    return GuardrailFunctionOutput(
        tripwire_triggered=True,
        output_info={
            "reason": "Please ask library-related questions only (books, timings, availability)."
        },
    )
