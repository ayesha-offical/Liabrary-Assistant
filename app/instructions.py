from agents import RunContextWrapper,Agent
from .utils import UserContext, is_member

def dynamic_instruction(
    ctx: RunContextWrapper[UserContext],
    agent:Agent[UserContext],
) -> str:
    """
    Personalized system prompt built at runtime.
    """
    u = ctx.context
    greet = f"You are a helpful Library Assistant for user: {u.name}."
    membership = (
        "User is a registered member. You may use member-only tools."
        if is_member(ctx)
        else "User is a guest. Member-only tools are not available."
    )
    policy = (
        "Answer only library-related questions. "
        "Use tools when helpful. If user asks both to find a book and check copies, "
        "you may call multiple tools (parallel tool calls enabled). "
        "Be concise and friendly."
    )
    examples = (
        "Examples:\n"
        "- 'Do you have Deep Work? How many copies?' → call search_book then check_availability (if member).\n"
        "- 'What are timings?' → use getting_timings.\n"
    )
    return f"{greet}\n{membership}\n{policy}\n{examples}"
