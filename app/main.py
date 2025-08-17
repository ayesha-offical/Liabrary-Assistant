import os
import asyncio
from typing import Optional

from dotenv import load_dotenv
from agents import Runner, InputGuardrailTripwireTriggered
from .agent import library_agent
from .utils import UserContext, is_member
from .data import REGISTERD_MEMBER


# --- load env ---
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY missing. Set it in .env")

# --- helper: safe async call with retry ---
async def run_with_retry(prompt: str, ctx: UserContext, attempts: int = 3, delay_base: float = 1.0):
    last_err = None
    for i in range(attempts):
        try:
            return await Runner.run(library_agent, prompt, context=ctx)
        except InputGuardrailTripwireTriggered:
            # off-topic guardrail
            raise
        except asyncio.CancelledError as e:
            last_err = e
            if i == attempts - 1:
                raise
            await asyncio.sleep(delay_base * (i + 1))
        except Exception as e:
            last_err = e
            if i == attempts - 1:
                raise
            await asyncio.sleep(delay_base * (i + 1))
    raise last_err

def ask(prompt: str, default: Optional[str] = None) -> str:
    val = input(prompt).strip()
    if not val and default is not None:
        return default
    return val

def show_menu(is_member_flag: bool) -> str:
    print("\n=== Library Assistant ===")
    print("1) Search for a book")
    print("2) Check book availability (members only)")
    print("3) Get library timings")
    print("4) Exit")
    if not is_member_flag:
        print("   (Tip: You are a guest. Availability is for registered members only.)")
    choice = input("Choose an option [1-4]: ").strip()
    return choice

async def handle_search(ctx: UserContext):
    title = ask("Enter book title (partial ok): ")
    if not title:
        print("⚠️  Title is required.")
        return
    # Let the agent do tool-calls (search_book) and answer
    q = f"Search for the book titled '{title}'. Tell me if it exists."
    r = await run_with_retry(q, ctx)
    print("🔎", r.final_output)

async def handle_availability(ctx: UserContext):
    if not is_member_flag(ctx):
        print("⛔ Availability is only for registered members. Please provide a valid member_id.")
        return
    title = ask("Enter book title for availability: ")
    if not title:
        print("⚠️  Title is required.")
        return
    # Agent will call search_book + check_availability (member-only tool)
    q = f"Do you have '{title}'? If yes, how many copies are available?"
    r = await run_with_retry(q, ctx)
    print("📚", r.final_output)

async def handle_timings(ctx: UserContext):
    # Agent will call getting_timings tool
    q = "What are the library timings today?"
    r = await run_with_retry(q, ctx)
    print("🕘", r.final_output)

def is_member_flag(ctx: UserContext) -> bool:
    return bool(ctx.member_id) and ctx.member_id in REGISTERD_MEMBER

def confirm_registered() -> Optional[str]:
    print("\n— Registration Check —")
    print("If you have a member ID, enter it now (e.g., M-123).")
    print("Press Enter to stay a guest.")
    mid = input("Member ID: ").strip()
    return mid or None

async def main_loop():

    print("Welcome to Library Assistant 👋")
    name = ask("Your name: ", default="Reader")
    member_id = confirm_registered()

    ctx = UserContext(name=name, member_id=member_id)
    print(f"\nHi {ctx.name}! Status: {'Member' if is_member_flag(ctx) else 'Guest'}")

    while True:
        choice = show_menu(is_member_flag(ctx))
        if choice == "1":
            try:
                await handle_search(ctx)
            except InputGuardrailTripwireTriggered:
                print("🚧 Please ask library-related questions only.")
        elif choice == "2":
            try:
                await handle_availability(ctx)
            except InputGuardrailTripwireTriggered:
                print("🚧 Please ask library-related questions only.")
        elif choice == "3":
            try:
                await handle_timings(ctx)
            except InputGuardrailTripwireTriggered:
                print("🚧 Please ask library-related questions only.")
        elif choice == "4":
            print("Goodbye! 👋")
            break
        else:
            print("⚠️  Invalid choice. Please pick 1–4.")

def run_sync_smoke_test():
    """
    Optional: run a quick sync test before interactive loop (Windows-friendly).
    """
    from .utils import UserContext
    from .agent import library_agent
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    ctx = UserContext(name="SmokeTest", member_id="M-123")
    q = "Please check availability for Clean Code."
    r = Runner.run_sync(library_agent, q, context=ctx)
    print("✅ Sync smoke:", r.final_output)

if __name__ == "__main__":
    asyncio.run(main_loop())