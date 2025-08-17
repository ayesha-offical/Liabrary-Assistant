from typing import Any, Dict
from pydantic import Field
from agents import function_tool
from agents import RunContextWrapper, Agent
from .utils import UserContext, is_member, search_book_title
from .data import BOOK_DB, LIBRARY_TIMINGS

@function_tool
def getting_timings() -> Dict[str, Any]:
    """Return library timings."""
    return {"timings":LIBRARY_TIMINGS}

@function_tool
def searching_book(
    title: str =Field(..., description="Exact or partial book title to search" )
) -> Dict[str, Any]:
    """Returns whether a book exists (case-insensitive; fuzzy supported)."""
    key= search_book_title(title)
    return {"exists": key is not None,  "matched_title": key or title}

@function_tool(is_enabled=lambda rc, ag: is_member(rc))
def check_availability(
    title:str =Field(...,description="Book title to check copies for")
) -> Dict[str,Any]:
    """
    Returns number of copies (members only).
    Hidden from the model if user isn't a valid member.
    """

    key = search_book_title(title)
    if key is None:
        return{"found": False, "title": title, "copies": 0}
    return {"found": True, "title": key, "copies": BOOK_DB[key]}
