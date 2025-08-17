from typing import Optional
from agents import RunContextWrapper
from .data import BOOK_DB, REGISTERD_MEMBER
from pydantic import BaseModel

class UserContext(BaseModel):
    name: str= "Reader"
    member_id: str | None = None

def is_member(ctx: RunContextWrapper[UserContext]) -> bool:
    mid =ctx.context.member_id
    return bool(mid) and mid in REGISTERD_MEMBER

def search_book_title(query:str) -> Optional[str]:
    q = query.strip().lower()
    for key in BOOK_DB:
        if q == key.lower():
            return key
    for key in BOOK_DB:
        if q in key.lower():
            return key
    return None

def liabray_related(text:str) -> bool:
    t = text.lower()
    keywords =[
        "book", "books", "library", "timings", "hours", "open", "close",
        "availability", "copies", "catalog", "search", "borrow", "return",
        "reserve", "hold"
    ]
    return any (k in t for k in keywords)